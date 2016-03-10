
def affiche_liste_files(all_my_files):
	for i,file in enumerate(all_my_files):
		all_my_files[i] = list(all_my_files[i])
		all_my_files[i][2] = convert_size(all_my_files[i][2])
	return all_my_files


def convert_size(size):
	unite = "o"
	table_unite = 'O','k','M','G'
	for p in range(3,-1,-1):
		diviseur = 10**(p*3)
		if int(size) > diviseur:
			unite = table_unite[p]
			""" j'arrondi la variable et j'ajoute une unité en
			fonction du résultat (o/k/m/g)"""
			size = round(int(size) / diviseur,1)
			#Si taille arrondi = la taille non arrondi alors je prend le int
			#if size == int(size):
			#	size = int(size*)
			print(size)
			return "{0} {1} ".format(size,table_unite[p])
	return size

