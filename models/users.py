#!/usr/bin/python3

import psycopg2

def GetAllUsers():
	#renvoie la liste de tout les utilisateur enregistrer dans le site
	with psycopg2.connect("dbname=projet_rd user=postgres host=localhost password=zonarisk") as c:
		r=c.cursor()
		r.execute("SELECT id,login,admin FROM users;")
		return r.fetchall()

def AddUser(identifiant,email,mdp):
 	#	joute un utilisateur dans la bdd
	with psycopg2.connect("dbname=projet_rd user=postgres host=localhost password=zonarisk") as c:
		r=c.cursor()
		r.execute("INSERT INTO USERS (login, email,password) VALUES (%s, %s, %s) RETURNING id;", [identifiant,email.lower(),mdp])
		return r.fetchone()

def GetUserFromLoginAndPassword(login,mdp):
	#récupérer un utilisateur en fonction du mdp et du login (que le login soit un mail ou un identifiant)
	with psycopg2.connect("dbname=projet_rd user=postgres host=localhost password=zonarisk") as c:
		r=c.cursor()
		r.execute("SELECT id,login,email,admin from users where password=%s and (login=%s or email=%s);",  [mdp,login,login.lower()])
		return r.fetchall()

def ExistUserByLoginOrEmail(login,email=None):
	if email is None:
		email=login
	with psycopg2.connect("dbname=projet_rd user=postgres host=localhost password=zonarisk") as c:
		r=c.cursor()
		r.execute("SELECT login,email,admin from users where login=%s or email=%s ;",  [login,email.lower()])
		return r.fetchall()

def ExistUserById(id,email=None):
	with psycopg2.connect("dbname=projet_rd user=postgres host=localhost password=zonarisk") as c:
		r=c.cursor()
		r.execute("SELECT login,email,admin from users where id=%s ;",  [id])
		return r.fetchone()

def UpdateUserLoginById(id,login):
	with psycopg2.connect("dbname=projet_rd user=postgres host=localhost password=zonarisk") as c:
		r=c.cursor()
		r.execute("update users set login=%s where id=%s;",  [login,id])

def UpdateUserPasswordById(id,password):
	with psycopg2.connect("dbname=projet_rd user=postgres host=localhost password=zonarisk") as c:
		r=c.cursor()
		r.execute("update users set password=%s where id=%s;",  [password,id])

def UpdateUserEmailById(id,email):
	with psycopg2.connect("dbname=projet_rd user=postgres host=localhost password=zonarisk") as c:
		r=c.cursor()
		r.execute("update users set email=%s where id=%s;",  [email,id])

def UpdateRoleAdmin(id,admin):
	with psycopg2.connect("dbname=projet_rd user=postgres host=localhost password=zonarisk") as c:
		r=c.cursor()
		r.execute("update users set admin=%s where id=%s;",  [admin,id])

def GetUserById(id):
	with psycopg2.connect("dbname=projet_rd user=postgres host=localhost password=zonarisk") as c:
		r=c.cursor()
		r.execute("SELECT login, email, admin FROM users where id=%s;",[id])
		return r.fetchone()
	
#for i in ExistUser('luigi','wario@nintendo.fr'):
#	print (i[1])
#AddUser("wario","wario@nintendo.fr","test")
#for i in ExistUser("Wade"):
#	print(i)
#add_user("bernardo","b.viveescarmouche@gmail.com","zonarisk")
