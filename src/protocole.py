from random import randrange
import socket
"""
Protocole python


type sur 1 octet (255 type)
length sur 4 octet(size 65335 octets)
data sur 65335>=x+length+typeoctet
- type 1 indique le nombre de paquet q recevoir en fonction d'un ticket
"""
#Variable Globale
size_bytes_trame = 2
max_length = (255 ** size_bytes_trame ) - 1

size_bytes_jeton = 2
max_jeton = (255 ** size_bytes_jeton ) -1

size_bytes_type = 1
def struct_protocole(type_proto,data):
	type_proto = (type_proto).to_bytes(size_bytes_type,byteorder='big')
	length = (size_bytes_type + size_bytes_trame + len(data)).to_bytes(\
			size_bytes_trame, byteorder='big')
	trame = type_proto+length+data
#	print("length ({0})=  champ size({1}) + champs data ({2}) + ")
	return trame

def generate_jeton():
	jeton = randrange(65535)
	return jeton

def connect_to_serveur():
	hote = "localhost"
	port = 3333

	connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connexion_avec_serveur.connect((hote, port))
	print("Connexion établie avec le serveur sur le port {}".format(port))

#	msg_a_envoyer = b""
	msg_recu = connexion_avec_serveur.recv(1024)
	print(msg_recu.decode())
	msg_recu = connexion_avec_serveur.recv(1024)
	print(msg_recu.decode())
	"""while msg_a_envoyer != b"fin":
		msg_a_envoyer = msg_a_envoyer.encode()

		connexion_avec_serveur.send(msg_a_envoyer)
		msg_recu = connexion_avec_serveur.recv(1024)
		print(msg_recu.decode())
	"""
	return connexion_avec_serveur

def close_connection_with_serveur(connexion_avec_serveur):
	print("fermeture de la connexion")
	connexion_avec_serveur.close()

def struct_data(data,type_proto):
	"""
La structure du champ data change en fonction du type
	"""

	if (type_proto == 1):
		""" Si type proto 1 alors data et contituer d'un jeton ainsi que
		du nombre de trame a envoyer"""



"""
1.1. Fonction Get all_file_by_user_id 

Entrer : Id de l’utilisateur
Action : contacte la base sql récupère la liste des fichiers de l’utilisateur.
Sotrie : Liste des fichiers fr l’utilisat

"""
def nbr_trame_needed(size_effective_data):
	"""
	Cette fonction prend en prametre la taille total des donner a envoyer et
	renvoie le nombre de trame a envoyer
	"""
	nbr_trame = size_effective_data / (max_length - (size_bytes_type +  
		size_bytes_trame + size_bytes_jeton))
	if nbr_trame == int(nbr_trame):
		return int(nbr_trame)
	else :
		return int(nbr_trame+1)

def get_all_file_by_user_toEncode(id): 
	""" Get all file by user est contituer d'une seul requetes( il n'y a donc
	pas besoin d'indiquer le nombre de requetes a recevoir qu serveur
		- Un jeton sur 4 octet
		- Un id sur x octet
		- Type:5
		Probleme possibiliter de collision entre les jetons

		1 on genere un jeton
		2 convertie le parametre en byte
		3 on compte le nombre de trame necessaire a l'envoie des info
		(dans ce cas si il es superieur a un y a probleme)
		4 on creer les infos 
	"""
	#1 generation jeton
	jeton = generate_jeton()
	print(">jeton"+str(jeton))
	bytes_jeton = (jeton).to_bytes(size_bytes_jeton, byteorder='big')

	#convertion de la data a en voyer en bytes
	bytes_size = id.bit_length()

	effective_data = (id).to_bytes(bytes_size, byteorder='big')
	if nbr_trame_needed( len(effective_data)) != 1:
		raise ValueError("Error Test nbr_trame_needed by "+ \
				"get_all_file_by_user_toBytes cas n'est pas supposé arriver")
	trame = struct_protocole(5,bytes_jeton+effective_data)
	print(">{}".format(trame))
	connexion_avec_serveur = connect_to_serveur()
	#msg_recu = connexion_avec_serveur.recv(1024)
	#print(msg_recu)
	connexion_avec_serveur.send(trame)
	msg_recu = connexion_avec_serveur.recv(1024)
	print(msg_recu)
	return trame



def trame_decode(trame):
	"""
	Cette fonction completement inutile permet de verifier que je suis bien
	capable de decode la trame en python avant de faire un test d'envoie vers
	mon serveur en C
	1 recupe le type de la requete 
	La type de la trame et sur 1 octet
	2 recuperation de la taille de la trame
	3 recuperation du jeton
	4 je redirige vers la bonne fonction selon
	le resultat
	"""
	#1
	#type_trame = int.from_bytes(trame[0],'big')
	type_protocole = int.from_bytes(trame[0:size_bytes_type],'big')
	print(trame)
	print(type_protocole)
	#2
#	length_trame = trame[1:3]
	length_trame = int.from_bytes(trame[size_bytes_type:size_bytes_type +
		size_bytes_trame],'big')
	print(length_trame)
#	print("size: " +str(length_trame)+ " len(trame)="+ str(len(trame)))
	#3
#	jeton_trame = trame[3:6]
	jeton_trame = int.from_bytes(trame[size_bytes_type + size_bytes_trame:
		size_bytes_type+size_bytes_trame+size_bytes_jeton],'big')
	print(jeton_trame)
	data = trame[size_bytes_type+size_bytes_trame + size_bytes_jeton:]
	print(data)
	if type_protocole == 5 :
		get_all_files_by_user_toDecode(jeton_trame,data)
		




def get_all_files_by_user_toDecode(jeton,id):
	print("L'id des fichier utilisateur demander est :{}"
			.format(int.from_bytes(id,'big')))



trameyolo = get_all_file_by_user_toEncode(1000)


#trame_decode(trameyolo)
