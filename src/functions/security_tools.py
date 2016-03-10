import random

def generate_salt(nbr):
	alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	chaine=""
	for i in range(nbr):
		chaine = chaine + random.choice(alpha)
	return chaine


