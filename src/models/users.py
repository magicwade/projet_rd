
import psycopg2

def GetAllUsers(c):
	"""renvoie la liste de tout les utilisateurs enregistrer dans le site"""
	r=c.cursor()
	r.execute("SELECT id,login,admin FROM users;")
	return r.fetchall()

def AddUser(c,identifiant,email,mdp):
 	"""ajoute un utilisateur dans la bdd"""
	r=c.cursor()
	r.execute("INSERT INTO USERS (login, email,password) VALUES (%s, %s, %s) RETURNING id;", [identifiant,email.lower(),mdp])
	return r.fetchone()

def GetUserFromLoginAndPassword(c,login,mdp):
	"""récupérer un utilisateur en fonction du mdp et du login (que le login soit un mail ou un identifiant)"""
	r=c.cursor()
	r.execute("SELECT id,login,email,admin from users where password=%s and (login=%s or email=%s);",  [mdp,login,login.lower()])
	return r.fetchall()

def ExistUserByLoginOrEmail(c,login,email=None):
	if email is None:
		email=login
	r=c.cursor()
	r.execute("SELECT login,email,admin from users where login=%s or email=%s ;",  [login,email.lower()])
	return r.fetchall()

def ExistUserById(c,id,email=None):
	r=c.cursor()
	r.execute("SELECT login,email,admin from users where id=%s ;",  [id])
	return r.fetchone()

def UpdateUserLoginById(c,id,login):
	r=c.cursor()
	r.execute("update users set login=%s where id=%s;",  [login,id])

def UpdateUserPasswordById(c,id,password):
	r=c.cursor()
	r.execute("update users set password=%s where id=%s;",  [password,id])

def UpdateUserEmailById(c,id,email):
	r=c.cursor()
	r.execute("update users set email=%s where id=%s;",  [email,id])

def UpdateRoleAdmin(c,id,admin):
	r=c.cursor()
	r.execute("update users set admin=%s where id=%s;",  [admin,id])

def GetUserById(c,id):
	r=c.cursor()
	r.execute("SELECT login, email, admin FROM users where id=%s;",[id])
	return r.fetchone()
	
