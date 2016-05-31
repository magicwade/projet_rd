#ifndef STDIO
#define STDIO
#include <stdio.h>
#endif

#ifndef STDLIB
#define STDLIB
#include <stdlib.h>
#endif

#ifndef LIBPQ_FE
#define LIBPQ_FE
#include <libpq-fe.h>
#endif

#ifndef MAIN
#define MAIN
#include "../Headers/main.h"
#endif

#ifndef STRING
#define STRING
#include <string.h>
#endif

#ifndef SYSSOCKET
#define SYSSCOKET
#include <sys/socket.h>
#endif

#ifndef ARPAINET
#define ARPAINET
#include <arpa/inet.h>
#endif

#ifndef UNISTD
#define UNISTD
#include <unistd.h>
#endif


#ifndef NETDB
#define NETDB
#include <netdb.h>
#endif


#ifndef PHTREAD
#define PHTREAD
#include <pthread.h>
#endif

#ifndef DECRYPTTRAME
#define DECRYPTTRAME
#include "decrypt_trame.c"
#endif


#define SIZE_BYTES_TYPE  1
#define SIZE_BYTES_TRAME  2
#define SIZE_BYTES_JETON  2
#define SERVEUR_PORT 3333


void *connection_handler(void *);
void viderBuffer();
int main(int argc ,char *argv[])
{
/*	int socket_desc;
	struct sockaddr_in server;
	char *message,server_reply[2000];
	
	//Create socket
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);

	if (socket_desc == -1)
	{
		printf("Could not create socket");
	}
	
	char *hostname = "www.google.com";
	char  ip[100];
	struct hostent *he;
	struct in_addr **addr_list;
	int i;

	if ( ( he = gethostbyname( hostname) ) == NULL)
	{
		//gethostbyname fqiled
		herror("gethostbyname");
		return 1;
	}

	//Cast the h_qddr_list to in_addr , since h_addr_list also hqs the ip adresse in long formqt only
	addr_list = (struct in_addr **) he->h_addr_list;

	for ( i = 0; addr_list[i] != NULL; i++)
	{
		//Return the first one;
		strcpy(ip,inet_ntoa(*addr_list[i]) );
	}
	printf("%s resolved to : %s",hostname,ip);


	
	server.sin_addr.s_addr = inet_addr(ip);
//	server.sin_addr.s_addr = *addr_list[0];
	server.sin_family  = AF_INET;
	server.sin_port = htons( 80 );
	//CONNECT to remote server
	if ( connect(socket_desc,(struct sockaddr *)&server , sizeof(server)) <0)
	{
		puts("Connect error");
		return 1;
	}
	puts("Connected");
	//Send some data
	message = "GET / HTTP/1.1\r\n\r\n";
	if ( send(socket_desc , message ,strlen(message) , 0) < 0)
	{
		puts("Send failed");
		return 1;
	}

	puts("Data Send\n");

	if (recv(socket_desc, server_reply, 2000, 0) < 0)
	{
		puts("recceived failed");
	}
	puts("reply received\n");
	//puts(server_reply);

	close(socket_desc);
	*/
	int socket_desc, new_socket, c, *new_sock=NULL;
	struct sockaddr_in server ,client;
	char *message;
	//Create socket
	socket_desc = socket(AF_INET,SOCK_STREAM,0);
	if (socket_desc == -1)
	{
		printf("Could not create socket");
	}

	//Prepqre the sockaddr = AF_INET;
	server.sin_family = AF_INET;
	server.sin_addr.s_addr  = INADDR_ANY;
	server.sin_port = htons(SERVEUR_PORT);

	//Bind
	if( bind(socket_desc,(struct sockaddr *)&server,sizeof(server)) < 0)
	{
		puts("bind failed");
	}
	puts("bind done");
	listen(socket_desc , 3);
	//Accept and incoming connection
	puts("Waiting for incoming connections...");
	c = sizeof(struct sockaddr_in);
	while (new_socket = accept(socket_desc, (struct sockaddr *)&client,(socklen_t*)&c)){

		puts("Connection accepted");
		message = "Connected.\n";
		write(new_socket, message, strlen(message));

		pthread_t sniffer_thread;
		new_sock = malloc(sizeof(int));
		*new_sock = new_socket;
		if ( pthread_create( &sniffer_thread, NULL, connection_handler, (void*) new_sock) <0)
		{
			perror("could not create thread");
			return 1;
		}
		//NOW join thread, so 	that we don't terminate before thr thread 
		//pthread_join(sniffer_thread , NULL);
		puts("Handler assigned");
	}

	if (new_socket < 0)
	{
		perror("accept failed");
		return 1;
	}
	

	return 0;
}
// This wwill handle connection for each client
void *connection_handler(void *socket_desc)
{
	// Get the socket descriptor
	int sock = *(int*)socket_desc;
	int read_size;	
	char *message, client_message[2000]={0};

	//Send some messages to the client
	message = "T'es dans le thread.\n";
	write(sock,message, strlen(message));
	PGconn *conn;
	PGconn *conn = PQconnectdb("user=postgres dbname=projet_rd password=zonarisk");
	PGresult *res;
	if (PQstatus(conn) == CONNECTION_BAD){
		fprintf(stderr,"connection to database failed: %s\n",PQerrorMessage(conn));
		exit_nicely(conn);
	}
	//Receive a message  back to the client
	while( ( read_size = recv (sock, client_message , 2000 , 0)) > 0)
	{
		//SEND THE MESSAGE BACK TO THE CLIENT
//		int offset=0;
		int type_proto = 0;
		int size_trame = 0;
		int jeton = 0;
		int start = 0, end = SIZE_BYTES_TYPE;

		//Recuperation de l'entete
		type_proto = bytes_to_int_from_array(start,end,client_message);
		//Recuperation de la taille 
		start = SIZE_BYTES_TYPE;
		end = SIZE_BYTES_TYPE + SIZE_BYTES_TRAME;
		size_trame = bytes_to_int_from_array(start,end,client_message);
		//recuperation JETON
		start = SIZE_BYTES_TYPE + SIZE_BYTES_TRAME;
		end = SIZE_BYTES_TYPE + SIZE_BYTES_TRAME + SIZE_BYTES_JETON;
		jeton = bytes_to_int_from_array(start,end,client_message);
		printf("type du proto: %d\n", type_proto);
		printf("taille de la trame: %d\n", size_trame);
		printf("Jeton: %d\n", jeton);
		//On envoie vers la fonction qui ce chargerra du déchiffrement
		write(sock, client_message, strlen(client_message));
		memset(client_message, 0, sizeof(client_message));

	}
	if (read_size==0)
	{
		puts("Client disconnected");
		fflush(stdout);
	}
	else if (read_size == -1)
	{
		perror("recv failed");
	}
	//ree the socket pointer
	free(socket_desc);
	return 0;
}
//int decode_trame(type_proto,size_trame,jeton,){

//}
/*int bytes_to_int_from_array(int start,int end,char client_message[])
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
}*/
int ipow(int base, int exp){
	int result = 1;
	while (exp)
	{
		if (exp & 1)
			result *= base;
		exp >>= 1;
		base *= base;
	}

	return result;
}
