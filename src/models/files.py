import cherrypy
import psycopg2

#c=cherrypy.thread_data.db
class File:
	"""Class permettant d'intéragir avec table user de la base de donnée"""
	def __init__(self,connection):
		self.connection=connection

	def commit(self):
		self.connection.commit()

	def get_all_files_by_id_user(self,user_id):
		"""renvoie la liste de tout les utilisateurs enregistrés dans le
		site"""
		with self.connection.cursor() as result:
			result.execute("SELECT id, filename, size  FROM files " + \
					"where id_user = %s;",[user_id])
			return result.fetchall()

	def get_meta_data_file_by_id(self,id):
		"""renvoie la liste de tout les utilisateurs enregistré dans le site"""
		with self.connection.cursor() as result:
			result.execute("SELECT filename, size, data, id_user FROM files" +\
					" where id = %s;",[id])
			return result.fetchone()

	def add_meta_data_file(self, filename,id):
		with self.connection.cursor() as result:
			result.execute("INSERT INTO files (filename,size,data,id_user)" + \
					" values (%s, 0, lo_create(0), %s) returning id,data",
					[filename,id])
			return result.fetchone()
	def update_meta_data_size_by_id(self,size,id):
		with self.connection.cursor() as result:
			result.execute("UPDATE files set size=%s where id=%s",[size,id])
	def delete_file_by_id(self,id):
		with self.connection.cursor() as result:
			result.execute("DELETE FROM files where id = %s", [id])

	def delete_file_by_user_id(self,id):
		with self.connection.cursor() as result:
			result.execute("DELETE FROM files where id_user = %s returnin" + \
					"id,filename,size,oid",[user_id])
			return result.fetchall()

#Large object content

	def get_file_handler_by_oid(self, oid, mode):
		"""Renvoie les données de du fichierstocker en bdd"""
		object_data = psycopg2.extensions.lobject(self.connection,oid,mode)
		return object_data



