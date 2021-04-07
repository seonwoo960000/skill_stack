# Chatting Bot application 

## [Flowchart diagram (multiserver.py)](https://github.com/seonwoo960000/skill_stack/blob/main/Chatting%20Bot/scripts/multiserver.py) 
 * Programming language : python 
 * Script for server (multithreading, multiple connections available) 
 * Script for client (multithreading for reading and writing)

## Features(server)
 * Multi-threading and scheduling tasks using queue 
 * Multiple connection from clients available
 * Able to send and receive messages simultaneously 
 * Able to connect clients from different networks 

## Features(client)
 * Able to receive and sent messages concurrently 

## Limitations
 * Confusion in the command line when input message and receiving message come in at the same time
 * Direct communication between client and client isn't available 
*************************************************************************************************************************************
### Server
![Flowchart](diagrams/chatBotServer.png)
*************************************************************************************************************************************
### Client
![Flowchart](diagrams/chatBotClient.png)
