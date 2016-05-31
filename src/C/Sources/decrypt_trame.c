#include "../Headers/decrypt_trame.h"

int bytes_to_int_from_array(int start,int end,char client_message[])
{
	unsigned char buf = 0 ;
	int result = 0;
	int i = start;
	for(i = start ;i < end ;i = i + 1 )
	{
		buf = client_message[i];
		result = result + buf * ( ipow(255, end - (i + 1 )));
	}	
	return result;	
}
