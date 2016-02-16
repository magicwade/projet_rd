import os, os.path
import math
import configparser
import random
import cherrypy
import re
from jinja2 import Environment, FileSystemLoader
import hashlib
import psycopg2
from models.users import User
from models.files import File
from cherrypy.lib import static
env = Environment(loader=FileSystemLoader('templates'))
def connect(thread_index):
	# Create a connection and store it in the current thread
	conn = psycopg2.connect("dbname=projet_rd user=postgres host=localhost " +\
			"password=zonarisk")
	cherrypy.thread_data.users = User(conn)
	cherrypy.thread_data.files = File(conn)

class HomePage():
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	def POST(self,login="",password="",logout=""):
		""" 
		si un login et un mdp sont fournit alors j'authentifie
		si logout alors je supprime les session
		"""
		myuser = cherrypy.thread_data.users.get_user_by_login_or_email_and_password(\
				login,hashlib.sha512(password.encode()).hexdigest())
		tmpl = env.get_template('index.html')
		if logout == "":
			if myuser:
				if len(myuser) == 1:
					cherrypy.session['logged'] = True
					cherrypy.session['login'] = myuser[0][1]
					cherrypy.session['admin'] = myuser[0][3]
					cherrypy.session['id'] = myuser[0][0]
		else:
			cherrypy.session.pop('logged', None)
			cherrypy.session.pop('login', None)
			cherrypy.session.pop('admin', None)
			cherrypy.session.pop('id', None)
		raise (cherrypy.HTTPRedirect("/"))
	
	@cherrypy.tools.accept(media='application/octet-stream')
	def GET(self):
		"""
		Affiche la page home
		"""
		all_files = []
		all_my_files = cherrypy.thread_data.files.get_all_files_by_id_user(\
				cherrypy.session.get("id"))
		for i,file in enumerate(all_my_files):
			unite="o"
			table_unite= 'O','K','M','G'
			"""
			actuellement j'ai une liste contenant des tuple
			information concernant mon fichier), je vais etre
			contraint  de changer ces tuple en liste.
			Jinja ne me permet pas de faire de traitement 
			dans la vue. 
			je suis donc contraint de recréer un nouvelle objet 
			ou de changé celui dont je dispose en liste, 
			si je veux pouvoir changer une des variable contenue 
			dans ce tuple.
			La variable que je veux changer est la taille du fichier
			"1245423203" ce qui est bcp trop moche je préfére avoir 
			1.24G.
			"""
			all_my_files[i]=list(all_my_files[i])
			for p in reversed(range(0,4)):
				if int( all_my_files[i][2]) > math.pow(10,p*3):
					unite = table_unite[p]
					""" j'arrondi la variable et j'ajoute une unité en
					fonction du résultat (o/k/m/g)"""
					all_my_files[i][2]=round(int(all_my_files[i][2]) / \
							int(math.pow(10,p*3)),1)
					if all_my_files[i][2] == int(all_my_files[i][2]):
						all_my_files[i][2] = int(all_my_files[i][2])
					all_my_files[i][2] = str(all_my_files[i][2]) + " " + \
							table_unite[p]
					break
		tmpl = env.get_template('index.html')
		return tmpl.render(home=True,logged=cherrypy.session.get("logged"), 
				login=cherrypy.session.get("login"),
				admin=cherrypy.session.get("admin"),all_my_files=all_my_files)

class Download():
	exposed = True
	""" 
	Page permettant le téléchargement 
	Cette page ne peut etre lu que par les personne autorisé
	(au debut juste loggé).
	Le fichier donnée devra être décrypté a l'aide d'une clé 
	qui sera propre a l'utilisateur (différent du mdp normalement 
	sauf si l'user le décide)
	"""
	@cherrypy.tools.accept(media='application/foo')
	def GET(self,id_file=None):
		if not cherrypy.session.get("logged") or id_file == None:
			raise cherrypy.HTTPRedirect("/")
		myFile = cherrypy.thread_data.files.get_file_by_id(id_file)
		cherrypy.response.headers['Content-Disposition']='attachment; "\
				"filename="{0}"'.format(myFile[0])
		cherrypy.response.headers['Content-Type']='application/octet-stream'
		cherrypy.response.headers['Content-Length']=myFile[1]
		oid_data=myFile[2]
		all_data= cherrypy.thread_data.files.get_file_handler_by_oid(\
				oid_data,'rb')
		def stream():
			while True:
				data = all_data.read(4096)
				yield data
				if not data:
					all_data.close()
					break
		return stream()
	GET._cp_config = {'response.stream':True}


class Register():
	exposed = True
	"""
	Page d'enregistrement
	"""

	@cherrypy.tools.accept(media='text/plain')
	def GET(self):
		if cherrypy.session.get("admin"):
			raise cherrypy.HTTPRedirect("/")
		tmpl = env.get_template('register.html')
		return tmpl.render(register=True,
				logged=cherrypy.session.get("logged"),
				login=cherrypy.session.get("login"),
				admin=cherrypy.session.get("admin"))

class DeleteFileWebService(object):
	"""
	La fonction prend en paramétre un id de fichier
	- 1 select récupére l'oid du large object a supprimer
	- 2 Si je suis propiétaire du fichier ou  admin je passe
	- 3 supprime le large object
	- 4 supprime l'entrée dans la base files
	- 5 commit
	"""
	
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	def POST(self,file_id):
		if not cherrypy.session.get("logged"):
			raise cherrypy.HTTPRedirect("/")

		#1
		print(file_id)
		my_file = cherrypy.thread_data.files.get_meta_data_file_by_id(file_id)
		#2
		if not cherrypy.session.get('admin') and  \
				my_file[3] != cherrypy.session.get("id"):
					raise cherrypy.HTTPRedirect("/")
		#3
		print(my_file[3])
		large_object = cherrypy.thread_data.files.get_file_handler_by_oid(\
				my_file [2],'rb')
		large_object.unlink()
		print(my_file[2])
		#4
		cherrypy.thread_data.files.delete_file_by_id(file_id)
		#5
		cherrypy.thread_data.files.commit()
		raise cherrypy.HTTPRedirect("/")

	def GET(self):
		raise cherrypy.HTTPRedirect("/")



class RegisterWebService(object):
	""" 
	Gestion des enregistrementd utilisateur, Seul la méthode post est
	accepter.
	Si l'utilisateur existe on affiche une page d'erreur. si les mot de
	passe ne sont pas identique pareille.
	"""
	exposed = True

	@cherrypy.tools.accept(media='text/plain')
	def POST(self, identifiant, email, password, retype_password):
		"""
		Prend en paramettre, identifiant, email et passwords
		Créer un nouvelle utilisateur si le login et l'email sont
		unique, sinon renvoie une erreur
		Dans le cas ou un compte est créer. L'utilisateur et
		automatiquement authentifié sur le site avec ce compte.
		"""
		if cherrypy.session.get("logged") and \
				not cherrypy.session.get("admin"):
					raise cherrypy.HTTPRedirect("/")
		tmpl = env.get_template('registerwebservice.html')
		error = ""

		#gestion des erreur de saisie
		if identifiant == "":
			error += "<li>Identifiant non renseigné.</li>"
		if email == "":
			error += "<li>Email non renseigné.</li>"
		if password == "":
			error += "<li>Mot de passe non renseigné.</li>"
		if len(identifiant)<3:
			error += "<li>Votre login doit comporté au moins 3 caractère.</li>"
		if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
				email):
			error += "<li>Revérifiez l'adresse mail.</li>"
		if retype_password != password:
			error +="<li>Les mots de passe ne sont pas identiques</li>"

		if len(error) > 0:
			return tmpl.render(register=True,error="<ul>"+error+"</ul>",
					logged=cherrypy.session.get("logged"), 
					login=cherrypy.session.get("login"),
					admin=cherrypy.session.get("admin"))
		#On regarde si l'utilisatuer n'existepas dej
        
		list_users = cherrypy.thread_data.users.get_user_by_login_or_email(\
				identifiant,email)
		if not list_users:
			new_id_user = cherrypy.thread_data.users.add_user(\
					identifiant, email,
					hashlib.sha512(password.encode()).hexdigest())
			cherrypy.session['login'] = identifiant
			cherrypy.session['logged'] = True
			cherrypy.session['id'] = new_id_user
		else:
			for myuser in list_users:
				if myuser[0] == identifiant:
					error += "L'identifiant est déjà utilisé par un autre \
							utilisateur.<br >"
				if myuser[1] == email:
					error += "L'adresse mail est déjà utilisé par un autre\
							utilisateur.<br >"
				return tmpl.render(register=True,
						logged=cherrypy.session.get("logged"), 
						error=error, admin=cherrypy.session.get("admin"),
						login=cherrypy.session.get("login"))
		cherrypy.thread_data.users.commit()
		return tmpl.render(register=True,logged=cherrypy.session.get("logged"),
				login=cherrypy.session.get("login"),
				admin=cherrypy.session.get("admin"))


class Upload():
	exposed = True
	"""
	Page d'envoie de fichier sur le serveur
	"""

	@cherrypy.config(**{'response.timeout':3600})
	def POST(self,myFile):
		if not cherrypy.session.get("logged") or \
				not cherrypy.session.get("id"):
					raise cherrypy.HTTPRedirect("/")
		full_path = config_server['DEFAULT']['StorageDirectory'] + \
				myFile.filename
		oid_file = cherrypy.thread_data.files.add_meta_data_file(
				myFile.filename,cherrypy.session.get('id'))
		print("wtf")
		large_object = cherrypy.thread_data.files.get_file_handler_by_oid(\
				oid_file[1],'rwb')

		print("ok")
		size=0
		while True:
			data = myFile.file.read(4096)
			size += len(data)
			if not data:
				large_object.close()
				break
			large_object.write(data)
		cherrypy.thread_data.files.update_meta_data_size_by_id(size,
				oid_file[0])
		cherrypy.thread_data.files.commit()

class MyAccount():
	exposed = True
	"""
	Gestion de mon compte utilisateur
	"""

	@cherrypy.tools.accept(media='text/plain')
	def GET(self):
		"""
		J'affiche les infos d'un utilisateurs.
		si un login est fournit alors j'affiche les info de
		l'utilisateur fournit (nécéssite les droit d'admin)
		"""
		if not cherrypy.session.get("logged"):
			raise cherrypy.HTTPRedirect("/")
		tmpl = env.get_template('myaccount.html')
		myuser = cherrypy.thread_data.users.get_user_by_id(\
				cherrypy.session.get("id"))	
		return tmpl.render(myaccount=True,
				logged=cherrypy.session.get("logged"), 
				login=cherrypy.session.get("login"),
				email=myuser[1],admin=cherrypy.session.get("admin"))

	@cherrypy.tools.accept(media='text/plain')
	def POST(self,new_login="",new_email="",new_password="",
			new_retype_password=""):
		"""
		Je modifie uniquement les champs renseigné
		"""
		success = ""
		error = ""
		if not cherrypy.session.get("id"):
			raise cherrypy.HTTPRedirect("/")
		if new_password != "" and new_retype_password == new_password:
			cherrypy.thread_data.users.update_user_password_by_id(\
					cherrypy.session.get("id"), 
					hashlib.sha512(new_password.encode()).hexdigest())

			success += "<li>Mot de passe modifié</li>"
		elif new_password != "" and new_retype_password != new_password:
			error += "<li>Les Mots de passe ne sont pas identiques</li>"
		if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", 
				new_email):
			cherrypy.thread_data.users.update_user_email_by_id(\
					cherrypy.session.get("id"),new_email)

			success += "<li>Adresse mail modifié</li>"
		elif new_email != "" and not re.match(\
				r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
				new_email):
			error += "<li>Veuillez reverifier votre adresse mail.</li>"

		if len(new_login) >= 3:
			cherrypy.thread_data.users.update_user_login_by_id(\
					cherrypy.session.get("id"), new_login)
			cherrypy.session["login"]=new_login
			success += "<li>Login modifié</li>"
		elif new_login != "" and len(new_login)<3:
			error += "<li>Votre Login doit contenir au moins 3 caractères</li>"

		#Commit de toutes les modifications
		cherrypy.thread_data.users.commit()
		myuser= cherrypy.thread_data.users.get_user_by_id(\
				cherrypy.session.get("id"))
		tmpl=env.get_template('myaccount.html')
		return tmpl.render(myaccount=True,
				logged=cherrypy.session.get("logged"),
				login=cherrypy.session.get("login"),
				email=myuser[1], success=success, 
				error=error,admin=cherrypy.session.get("admin"))

class Administration():
	exposed = True
	"""
	Gestion de Tous les compte Utilisateurs
	Liste tous les utilisateur 
	"""

	@cherrypy.tools.accept(media='text/plain')
	def GET(self):
		if not cherrypy.session.get("admin"):
			raise cherrypy.HTTPRedirect("/")
		all_users = cherrypy.thread_data.users.get_all_users()
		tmpl = env.get_template('administration.html')
		return tmpl.render(administration=True,
				logged=cherrypy.session.get("logged"), 
				login=cherrypy.session.get("login"),
				admin=cherrypy.session.get("admin"),all_users=all_users)

class Account():
	exposed = True
	"""
	Gestion de l'utilisateurs passer en paramétres.
	la page n'accessible que par les utilisateurs ayant le droit admin
	"""

	@cherrypy.tools.accept(media='text/plain')
	def GET(self,id_user=False):
		"""
		Page affichant les information de l'utilisateurs a modifié
		si l'utilisateur n'a pas les droits on l'envoie sur la page d'acceuil.
		"""
		error = False
		if not cherrypy.session.get("admin") :
			raise cherrypy.HTTPRedirect("/")
		"""
		si aucun utilisateur n'a était transmis on le renvoie vers 
		la page d'administration
		"""
		if not id_user:
			raise cherrypy.HTTPRedirect("/administration")
		myuser = cherrypy.thread_data.users.get_user_by_id(id_user)
		if not myuser:
			error = "User not found in database"
		tmpl=env.get_template('account.html')
		message=cherrypy.session.get("message")
		cherrypy.session.pop('message',None)
		return tmpl.render(administration=True,
				logged=cherrypy.session.get("logged"), 
				login=cherrypy.session.get("login"), 
				admin=cherrypy.session.get("admin"), 
				myuser=myuser, error=error, id_user=id_user, message=message)


	@cherrypy.tools.accept(media='text/plain')
	def POST(self,id_user,new_login="",new_email="",new_password="",
			new_retype_password="",new_rights=""):
		"""
			Je modifie uniquement les champs renseigné
		gestion des erreurs de saisie
		"""
		logged = cherrypy.session.get("logged")
		login = cherrypy.session.get("login")
		success = ""
		error = ""

		#MOT DE PASS
		if new_password != "" and new_retype_password == new_password:
			cherrypy.thread_data.users.update_user_password_by_id(\
					id_user,hashlib.sha512(new_password.encode()).hexdigest())
			success+="<li>Mot de passe modifié</li>"
		elif new_password != "" and new_retype_password != new_password:
			error+="<li>Les Mots de passe ne sont pas identiques</li>"
		#MAIL
		if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
				new_email):
			cherrypy.thread_data.users.update_user_email_by_id(id_user,
					new_email)
			success += "<li>Adresse mail modifié</li>"
		elif new_email!="" and not re.match(\
				r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
				new_email):
			error += "<li>Veuillez reverifier votre adresse mail.</li>"
        
		#Login
		if len(new_login) >= 3:
			cherrypy.thread_data.users.update_user_login_by_id(id_user,
					new_login)
			login = new_login
			#modification de la variable de session si l'utilisateur ce
			#modifie lui même
			if cherrypy.session['id']==id_user:
				cherrypy.session["login"] = new_login
			success += "<li>Login modifié</li>"
		elif new_login != "" and len(new_login)<3:
			error += "<li>Votre Login doit contenir au moins 3 caractères\
					.</li>"

		#DROITS
		if new_rights != "":
			cherrypy.thread_data.users.update_admin_role(id_user,new_rights)
			success += "<li>Les droits on été changé modifié</li>"
		cherrypy.session['message']=(success,error)
            
		#sauvegarde des modification
		cherrypy.thread_data.users.commit()

		#verifier si l'id transmit et vien un nombre
		try:
			int(id_user)
		except ValueError:
			raise (cherrypy.HTTPRedirect("/administration"))
		else:
			id_user = int(id_user)
			raise (cherrypy.HTTPRedirect("/account/{0}".format(id_user)))

class DeleteUserWebService(object):
	"""
	La fonction prend en paramétre un id de fichier
	- 1 Si je suis  admin je passe
	- 2 je supprime toutes les entrée dans la table file posséder par
	  l'utilisateur a supprimer, en récupérant les info des en entréer
	  supprimer
	- 3 je supprime le contenue des rfichier dans la base de donnée
	- 4 supprime l'utilisateurs
	- 5 commit
	"""
	
	exposed = True
	@cherrypy.tools.accept(media='text/plain')
	def POST(self,user_id):
		#1
		if not cherrypy.session.get('admin'):
					raise cherrypy.HTTPRedirect("/")
		#2
		all_file_to_delete=cherrypy.thread_data.files.delete_files_by_user_id(\
				user_id)
		#3
		for file in all_file_to_delete:
			large_object=cherrypy.thread_data.files.get_file_handler_by_oid(\
					file[3],'rwb')
			large_object.unlink()
		#4
		cherrypy.thread_data.users.delete_user_by_id(user_id)
		#5
		cherrypy.thread_data.files.commit()
		raise cherrypy.HTTPRedirect("/")

	def GET(self):
		raise cherrypy.HTTPRedirect("/")
def ConfigurationCheck(config_server):
	if 'StorageDirectory' not in config_server['DEFAULT']:
		config_server['DEFAULT']['StorageDirectory'] = './public/storage/' 
		print("'StorageDirectory' non trouvé dans le fichier de "+
				"configuration\n Utilisation du repertoire par default "+
				"'./public/storage' ")
	else:
		#permettre l'écriture ./monrep; ./ étant un appele ver le
		#repertoire dans lequele le programme tourne
		if config_server['DEFAULT']['StorageDirectory'][0:1] =="./":
			config_server['DEFAULT']['StorageDirectory'] = \
					config_server['DEFAULT']['StorageDirectory'][1:]
		#si le 1er charactére n'est pas un / il faut ajouter le
		#repertoire dans lequel est installer le programe sinon postgres
		#pete un cable quand j'ajoute l'oid.
		if config_server['DEFAULT']['StorageDirectory'][0] != "/":
			config_server['DEFAULT']['StorageDirectory'] = \
					os.path.abspath(os.path.dirname(__file__)) + "/" +\
					config_server['DEFAULT']['StorageDirectory']
	print(config_server['DEFAULT']['StorageDirectory'])
	return config_server

if __name__ == '__main__':
	cherrypy.engine.subscribe('start_thread',connect)
	#Check serveur config
	config_server = configparser.ConfigParser()
	config_server.read('settings.conf')
	config_server = ConfigurationCheck(config_server)
	conf = {
			'global': {
				'server.socket_host': "0.0.0.0",
				'server.socket_port': 7000,
				'server.thread_pool': 10,
				'server.max_request_body_size': 0 ,
				'server.socket_timeout':60
				},
			'/': {
				'tools.sessions.on': True,
				'tools.staticdir.root': os.path.abspath(os.getcwd()),
				'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
				},
			'/registerwebservice': {
				'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
				'tools.response_headers.on': True,
				},
			'/static': {
				'tools.staticdir.on': True,
				'tools.staticdir.dir': './public'
				}
			}
	webapp = HomePage()
	webapp.registerwebservice = RegisterWebService()
	webapp.deletefilewebservice = DeleteFileWebService()
	webapp.upload = Upload()
	webapp.download = Download()

	webapp.register = Register()
	webapp.registerwebservice = RegisterWebService()

	webapp.myaccount = MyAccount()

	webapp.administration = Administration()
	webapp.account = Account()
	webapp.deleteuserwebservice = DeleteUserWebService()
	cherrypy.quickstart(webapp, '/', conf)
