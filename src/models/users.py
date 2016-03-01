
import cherrypy
import psycopg2

class User:
	"""Class permettant d'intéragir avec table user de la base de donnée"""
	def __init__(self,connection):
		self.connection=connection
	def commit(self):
		self.connection.commit()

	def get_user_by_login_or_email(self,login,email=None):
		if email is None:
			email=login
		with self.connection.cursor() as result:
			result.execute("SELECT login,email,admin,quotas_limit,quotas " + \
			"from users where login=%s or email=%s ;", [login,email.lower()])
			return result.fetchall()
	
	def get_user_by_login(self,login):
		with self.connection.cursor() as result:
			result.execute("SELECT id, login,email,admin,quotas_limit,quotas " + \
			"from users where login=%s;", [login])
			return result.fetchone()

	def get_user_by_login_or_email_and_password(self,login,mdp):
		"""récupérer un utilisateur en fonction du mdp et du login 
		(que le login soit un mail ou un identifiant)"""
		with self.connection.cursor() as result:
			result.execute("SELECT id,login,email,admin,quotas_limit,quotas "+\
					"from users where password=%s and (login=%s or email=%s);",
					[mdp,login,login.lower()])
			return result.fetchall()

	def get_all_users(self):
		"""renvoie la liste de tout les utilisateurs enregistré dans le site"""
		with self.connection.cursor() as result:
			result.execute("SELECT id,login,admin,quotas_limit,quotas " +\
					"FROM users;")
			return result.fetchall()

	def add_user(self,identifiant,email,mdp):
		"""ajoute un utilisateur dans la bdd"""
		with self.connection.cursor() as result:
			result.execute("INSERT INTO USERS (login, email,password) " +
				"VALUES (%s, %s, %s) RETURNING id;",
				[identifiant,email.lower(),mdp])
			return result.fetchone()

	def update_user_login_by_id(self,id,login):
		with self.connection.cursor() as result:
			result.execute("update users set login=%s where id=%s;",
					[login,id])
	
	def update_user_password_by_id(self,id,password):
		with self.connection.cursor() as result:
			result.execute("update users set password=%s where id=%s;", 
				[password,id])

	def update_user_email_by_id(self,id,email):
		with self.connection.cursor() as result:
			result.execute("update users set email=%s where id=%s;",
					[email,id])

	def update_user_quotas_limit_by_id(self,id,quotas_limit):
		with self.connection.cursor() as result:
			result.execute("update users set quotas_limit=%s where id=%s;",
					[quotas_limit,id])

	def update_user_quotas_by_id(self,id,quotas):
		with self.connection.cursor() as result:
			result.execute("update users set quotas=%s where id=%s;",
					[quotas,id])

	def update_user_quotas_by_login(self,login,quotas):
		with self.connection.cursor() as result:
			result.execute("update users set quotas=%s where login=%s;",
					[quotas,login])
	def update_admin_role(self,id,admin):
		with self.connection.cursor() as result:
			result.execute("update users set admin=%s where id=%s;",
					[admin,id])

	def get_user_by_id(self,id):
		with self.connection.cursor() as result:
			result.execute("SELECT login, email, admin ,quotas_limit,quotas "+\
					"FROM users where id=%s;",[id])
			return result.fetchone()

	def delete_user_by_id(self,id):
		with self.connection.cursor() as result:
			result.execute("DELETE FROM users WHERE id = %s;",[id])

