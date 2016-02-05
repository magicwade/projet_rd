
import cherrypy
import psycopg2

#c=cherrypy.thread_data.db
class User:
	"""Class permettant d'intéragir avec table user de la base de donnée"""
	def __init__(self,connection):
		self.connection=connection
	def commit(self):
		self.connection.commit()

	def get_user_by_login_or_email(self,login,email=None):
		if email is None:
			email=login
		result=self.connection.cursor()
		result.execute("SELECT login,email,admin from users where login=%s or email=%s ;",  [login,email.lower()])
		return result.fetchall()

	def get_user_from_login_or_email_and_password(self,login,mdp):
		"""récupérer un utilisateur en fonction du mdp et du login (que le login soit un mail ou un identifiant)"""
		result=self.connection.cursor()
		result.execute("SELECT id,login,email,admin from users where password=%s and (login=%s or email=%s);",  [mdp,login,login.lower()])
		return result.fetchall()

	def get_all_users(self):
		"""renvoie la liste de tout les utilisateurs enregistré dans le site"""
		result=self.connection.cursor()
		result.execute("SELECT id,login,admin FROM users;")
		return result.fetchall()

	def add_user(self,identifiant,email,mdp):
		"""ajoute un utilisateur dans la bdd"""
		result=self.connection.cursor()
		result.execute("INSERT INTO USERS (login, email,password) VALUES (%s, %s, %s) RETURNING id;", [identifiant,email.lower(),mdp])
		return result.fetchone()

	def update_user_login_by_id(self,id,login):
		r=self.connection.cursor()
		r.execute("update users set login=%s where id=%s;",  [login,id])
	
	def update_user_password_by_id(self,id,password):
		result=self.connection.cursor()
		result.execute("update users set password=%s where id=%s;",  [password,id])

	def update_user_email_by_id(self,id,email):
		result=self.connection.cursor()
		result.execute("update users set email=%s where id=%s;",  [email,id])

	def update_admin_role(self,id,admin):
		result=self.connection.cursor()
		result.execute("update users set admin=%s where id=%s;",  [admin,id])

	def get_user_by_id(self,id):
		result=self.connection.cursor()
		result.execute("SELECT login, email, admin FROM users where id=%s;",[id])
		return result.fetchone()
def add_user(connection,identifiant,email,mdp):
	"""ajoute un utilisateur dans la bdd"""
	result=connection.cursor()
	result.execute("INSERT INTO USERS (login, email,password) VALUES (%s, %s, %s) RETURNING id;", [identifiant,email.lower(),mdp])
	return result.fetchone()
#	def ExistUserByLoginOrEmail(login,email=None):
#		if email is None:
#			email=login
#		result=self.connection.cursor()
#		result.execute("SELECT login,email,admin from users where login=%s or email=%s ;",  [login,email.lower()])
#		return result.fetchall()


