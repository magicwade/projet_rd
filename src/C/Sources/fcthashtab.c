#ifndef UTHASH
#define UTHASH
#include "uthash.h"
#endif
#include "../Headers/fcthashtab.h"
struct Jeton
{
	int id;
	int nbr_trame;
	UT_hash_handle hh;
}
struct Jeton *jetons = NULL;

int add_jeton(int jeton_id, int nbr_trame)
{
	struct Jeton *s;
	HASH_FIND_INT(jetons,&jeton_id,s);
	if (s != NULL)
	{
		return 0;
	}
	s = malloc(sizeof(struct Jeton));
	s->id = jeton_id;
	s->nbr_trame = nbr_trame;
	HASH_ASS_INT(jetons, id, s);
	return 1;
}
void delete_jeton()
{
	HASH_DEL(jetons, jeton);
	free(jeton);
}
unsigned int size_hashtab_jeton()
{
	unsigned int size = HASH_COUNT(jetons);
	return size;
}

void delete_all_jeton()
{
	struct Jeton *current_jeton, *tmp;
	HASH_ITER(hh, jetons, current_jeton, tmp)
	{
		HASH_DEL(jetons, current_jeton);
		free(current_jeton);
	}
}
struct Jeton *find_jeton(int jeton_id)
{
	struct Jeton *s =  NULL;
	HASH_FIND_INT(jetons, &jeton_id, s);
	return s;
}
