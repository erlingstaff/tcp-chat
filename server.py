import os
import sys
import time
import socket
import random
import threading
from printer import Printer
from bots import allWords


# Global constants
IP = "0.0.0.0"
SIZE = 1024
FORMAT = "utf-8"
PRINTER = Printer("Aws")
BOTNAMES = {"Chuck", "Bob", "Alice", "Dora"}
MAXROUNDS = 4
MAXCLIENTS = 4
# Global non-constants
connectedBotnames = []
clients = []
interactive = False
commandLineArguments = sys.argv 


class AcceptingConnections(): # Class for determining if the server is accepting new client connections

    def __init__(self):
        self.accepting = True

    def is_accepting(self): # Returns true if the server is accepting new client connections
        return self.accepting 

    def set_not_accepting(self):
        self.accepting = False

    def set_accepting(self):
        self.accepting = True

chatAcceptingConnections = AcceptingConnections() # Instance of AcceptingConnections

try:
    if "-h" in commandLineArguments or "--help" in commandLineArguments: # Prints help if -h or --help is in the command line arguments
        print("Usage: python3 server.py [port]\n")                      
        print("The port should be an integer between 1024 and 65535.\n")
        print("If no port is specified, the program will exit.\n")
        print("Optional arguments:\n -it or --aws makes the server interactive. That means you decide the action words\n"+
        "\n -c <number> or --clients <number> sets the maximum number of clients that can connect to the server. Default = 4\n"+
        "\n -r <number> or --rounds <number> sets the maximum number of rounds that can be played. Default = 4\n"+
        "\n -h or --help prints this help message.\n" +
        "\n -s <number> or --start <number> decides how many bots that have to be connected for the server to start. This number is set equal to maxclients default\n" +
        "\n -d or --debug makes the server run in debug mode.\n")
        print("Example of simple start: python3 server.py 8080\n")
        print("This will start the server on port 8080. with default values\n")
        print("Example of advanced start: python3 server.py 8080 -it -c 2 -r 3 -s 1 -d\n\nThe server will start with 2 clients, "+
              "3 rounds and 1 bot has to be connected for the server to start. This will also show debug info\n")
        sys.exit()

    # If the user wants to run the server in interactive mode
    if "-it" in commandLineArguments or "--aws" in commandLineArguments:  # If the user wants to run the server in interactive mode
        interactive = True

    # If the user wants to specify the number of maxclients
    if "-c" in commandLineArguments or "--clients" in commandLineArguments: # If the user wants to specify the number of maxclients
        try:
            argumentIndex = commandLineArguments.index("-c") + 1 # Finds the index of the argument
            MAXCLIENTS = int(commandLineArguments[argumentIndex]) # Sets the maxclients to the argument
        except:
            print("Please specify the number of clients as an" +
                  "integer from 1-4 after -c." +
                  "\nExample: python3 server.py 8080 -c 4\nIf this parameter" +
                  "is not specified, the" +
                  "default value of 4 will be used.\n")
            os._exit(0)

    # If the user wants to specify the number of rounds
    if "-r" in commandLineArguments or "--rounds" in commandLineArguments: # If the user wants to specify the number of rounds
        try:
            MAXROUNDS = int(commandLineArguments[commandLineArguments.index("-r") + 1]) # Finds the index of the argument
        except:
            print("Please specify the number of rounds as an integer after -r." +
                  "\nExample: python3 server.py 8080 -r 10\nIf this paramter is not specified," +
                  " the default value of 1 will be used.\n")
            os._exit(0)
    
    # If the user wants to specify the number of bots to start with
    if "-s" in commandLineArguments or "--start" in commandLineArguments: # If the user wants to specify the number of bots to start with
        try:
            STARTWITH = int(commandLineArguments[commandLineArguments.index("-s") + 1]) # Finds the index of the argument
        except:
            print("Please specify the number of bots to start with as an integer after -s." +
                  "\nExample: python3 server.py 8080 -s 2\nIf this paramter is not specified," +
                  " the default value of 2 will be used.\n")
            os._exit(0)
    
    # If the user wants to run the server in debug mode
    if "-d" in commandLineArguments or "--debug" in commandLineArguments: 
        PRINTER.setDebugMode(True) # Sets the debug mode of the Printer class to true

    port = int(commandLineArguments[1]) # Gets the port from the command line arguments
    print(PRINTER.centerPrint("Hosting server on port " + str(port))) # Prints the port the server is hosting on

except Exception as e: # If the user did not specify a port
    PRINTER.debugPrint(e) # Prints the exception
    print(PRINTER.centerPrint("Port was not specified, use the command line arguments -h " +
                              "or --help for instructions."))
    os._exit(0)

STARTWITH = MAXCLIENTS  # MAXCLIENTS default is the same as STARTWITH
ADDRESS = (IP, port)        # A constant address variable containing (IP, port)
PRINTER.debugPrint("Address added: " + str(ADDRESS)) # Prints the address the server is hosting on

# Creates a socket with the address family INET, which is the IPv4 protocol.
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a socket
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Sets the socket to be reusable
mySocket.bind(ADDRESS)                  # Bind the socket to the address of type (IP, port)
mySocket.listen()                       # Starts listening for connections                     
mySocket.settimeout(0.5)                # Sets a timeout of 0.5 seconds for the socket, 
                                        # this effectively makes the socket non-blocking
# Debug prints
PRINTER.debugPrint("Socket 'mySocked' created" + str(mySocket))
PRINTER.debugPrint("Socket setsockopt called, socket is now reusable")
PRINTER.debugPrint("Socket bind called, socket is bound to address: " + str(ADDRESS))
PRINTER.debugPrint("Socket listen called, socket is now listening for connections")
PRINTER.debugPrint("socket has recieved a timeout 0.5s") 

# Checks if bots "clients"-list are alive, if not, it will remove them from the list
def checkClientsAlive():
    for client in clients: # Loops through all clients
        try: # Tries to send a message to the client
            PRINTER.debugPrint("Sent command !Alive to client " + str(client))  # Prints the message sent
            client.send(f"!Alive".encode(FORMAT))  # Sends the message
        except:
            PRINTER.debugPrint(str(client) + " is not a live, removed from clients list")  # Prints the client is not a live
            clients.remove(client)  # Removes the client from the clients list
    if len(clients) == 0:
        PRINTER.debugPrint("Socket shutting down")  # Prints the socket is shutting down
        mySocket.shutdown(1)  # Shuts down the socket
        PRINTER.debugPrint("Socket closed")  # Prints the socket is closed
        mySocket.close()  # Closes the socket
        quit()

# Checks if the servers clients are alive
def purgeDeadClients():
    for client in clients:  # Loops through all clients
        if not checkClientAlive(client):  # Checks if the client is alive
            PRINTER.debugPrint("Client " + str(client) + " is not alive, removed from "+
                                                          "clients list")  # Prints the client is not alive to debug
            clients.remove(client)  # Removes the client from the clients list if it is dead

# Checks if a specific client is alive
def checkClientAlive(client):
    try:
        PRINTER.debugPrint("Sent command !Alive to client " + str(client)) # Prints the message sent
        client.send(f"!Alive".encode(FORMAT))  # Sends the message
        PRINTER.debugPrint(str(client) + " is alive")  # Prints the client is alive
        return True  # Returns true if the client is alive
    except:
        PRINTER.debugPrint(str(client) + " is not alive")
        return False  # Returns false if the client is not alive

# Gets all the botnames currently connected and alive
def getAllBotnames():
    connectedBotnamesUpdated = []  
    for client in clients:  # Loops through all clients
        if checkClientAlive(client):  # Checks if the client is alive
            PRINTER.debugPrint("Sent command !RetrieveBotname to client " + str(client))  # Prints the message sent
            client.send("!RetrieveBotname".encode(FORMAT))  # Sends the message
            connectedBotnamesUpdated.append(client.recv(SIZE).decode(FORMAT))  # Adds the botname to the list
            PRINTER.debugPrint("Recieved botname " + str(connectedBotnamesUpdated[-1]) +
                               " from client " + str(client))  # Prints the botname recieved
    return connectedBotnamesUpdated  # Returns the list of botnames

# main chatRoom function
def chatRoom(client, roundNumber, maxRounds=MAXROUNDS, chatAcceptingConnections=chatAcceptingConnections):
    try: # Tries to send a message to the client
        PRINTER.debugPrint("No longer accepting connections for the current round") 
        chatAcceptingConnections.set_not_accepting() # Sets the chatAcceptingConnections to not accepting new connections
        while True:
            if roundNumber == 0: 
                welcomeText = "Welcome to the DATA2410 Chatroom!\n" 
                print(PRINTER.centerPrint(welcomeText))  # Prints the welcome text
                broadcast(welcomeText.encode(FORMAT))  # Broadcasts the welcome text
           
            if roundNumber < maxRounds:  # If the round number is less than the max rounds
                if not interactive:  # If the server is not in interactive mode
                    newRoundText = f"Round {roundNumber+1} is now live. The word is yours, Aws!"  # Sets the new round text
                    print(PRINTER.centerPrint(newRoundText))  # Prints the new round text
                    broadcast(newRoundText.encode(FORMAT))  # Broadcasts the new round text
                    actionWord = random.choice(allWords)    # Gets a random word from the allWords list
                    PRINTER.debugPrint("Action word is " + actionWord)  # Prints the action word
                    secondaryActionWordChecker = random.randint(0, 3)  # Gets a random number between 0 and 3
                    if secondaryActionWordChecker == 0:     # If the random number is 0
                        secondaryActionWord = random.choice(allWords)   # Gets a random word from the allWords list
                        while secondaryActionWord == actionWord:   # While the secondary action word is the same as the action word
                            secondaryActionWord = random.choice(allWords)   # Gets a random word from the allWords list
                    
                    if secondaryActionWordChecker != 0:   # If the random number is not 0
                        message = f"Aws: How about {actionWord}"    # Sets the message
                        print(PRINTER.bordered(message)) 
                        time.sleep(1.5)
                    else:  # If the random number is 0, then use the secondary action word as well
                        message = f"Aws: Let's discuss {actionWord} and {secondaryActionWord}"  
                        print(PRINTER.bordered(message))
                        time.sleep(1.5)

                    for client in clients:  # Loops through all clients
                        if checkClientAlive(client):  # Checks if the client is alive
                            PRINTER.debugPrint("Sent command !ActionWord to client " + str(client))  
                            client.send(message.encode(FORMAT))  # Sends the message

                    for client in clients:  # Loops through all clients
                        time.sleep(1.5)
                        PRINTER.debugPrint("Waiting for response from " + str(client))
                        actionMessageResponse = client.recv(SIZE).decode(FORMAT)  # Recieves the response from each client
                        PRINTER.debugPrint("Recieved response from " + str(client) + " : " + 
                                           actionMessageResponse)
                        print(PRINTER.bordered(actionMessageResponse))
                        broadcast(actionMessageResponse)  # Broadcasts the response

                    PRINTER.debugPrint("Now accepting waiting connections for the next round")
                    chatAcceptingConnections.set_accepting()  # Sets the chatAcceptingConnections to accepting new connections
                    time.sleep(3)
                    chatRoom(client, roundNumber+1)  # Calls the chatRoom function again recursively with the next round number

                else:  # If the server is in interactive mode
                    newRoundText = f"Round {roundNumber+1} is now live. The word is yours, Aws!"
                    print(PRINTER.centerPrint(newRoundText))
                    broadcast(newRoundText.encode(FORMAT))
                    serverMessage = input("What do you want the bots to discuss?\n")  # Gets the server message from the user
                    PRINTER.debugPrint("Action word is " + actionWord)
                    serverMessage = "Aws: " + serverMessage
                    print(PRINTER.bordered(serverMessage))
                    time.sleep(1.5)

                    for client in clients:  # Loops through all clients
                        if checkClientAlive(client):  # Checks if the client is alive
                            PRINTER.debugPrint("Sent the current message to " + str(client))
                            client.send(message.encode(FORMAT))

                    for client in clients:  # Loops through all clients
                        time.sleep(1.5)
                        PRINTER.debugPrint("Waiting for response from " + str(client))
                        actionMessageResponse = client.recv(SIZE).decode(FORMAT)  # Recieves the response from each client
                        PRINTER.debugPrint("Recieved response from " + str(client) + " : " + 
                                           actionMessageResponse)
                        print(PRINTER.bordered(actionMessageResponse))
                        broadcast(actionMessageResponse)
                    PRINTER.debugPrint("Now accepting waiting connections for the next round")
                    chatAcceptingConnections.set_accepting()   # Sets the chatAcceptingConnections to accepting new connections
                    time.sleep(3)                              # While the new round is being set up

                    chatRoom(client, roundNumber+1)  # Calls the chatRoom function again recursively with the next round number

            if roundNumber >= maxRounds:  # If it is the last round
                broadcast(f"!Finished")  # Broadcasts the !Finished command
                PRINTER.debugPrint("Finished.")  
                print(PRINTER.centerPrint("Chatroom has ended. Thank you for participating!"))
                print(PRINTER.centerPrint("To start a new chatroom, please restart the server and "+
                                          "connect the clients again."))
                os._exit(0)

    except Exception:  # Catches any exceptions and gives them to debugPrint
        PRINTER.debugPrint("Exception in chatRoom")
        print(PRINTER.centerPrint("A bot has suddenly disconnected. "+
                                  "The chatroom has been stopped. "+
                                  "Thank you for participating!"))
        gracefullyKickBots()  # Kicks all bots gracefully

# Function to send a message to all clients except the one that sent it to the server
def broadcast(messageToClient, sender=None):
    if type(messageToClient) != bytes:  # If the message is not bytes
        PRINTER.debugPrint("Message to client is not bytes, encoding to bytes for transfer.")
        messageToClient = messageToClient.encode(FORMAT)  # Encodes the message to bytes
    checkClientsAlive()  # Checks if all clients are alive
    for client in clients:  # Loops through all clients
        if client != sender:  # If the client is not the sender
            PRINTER.debugPrint(f"Sending {messageToClient} to client " + str(client))
            client.send(messageToClient)  # Sends the message to the client

    time.sleep(0.5)

# Function to gracefully kick all bots
def gracefullyKickBots():
    broadcast(f"!Kicked")  # Broadcasts the !Kicked command
    PRINTER.debugPrint("Kicking all bots, then shutting down.")
    mySocket.shutdown(1)  # Shuts down the server socket
    mySocket.close()      # Closes the server socket
    quit()

# function to check an incoming bot name against the bot names connected to the server
def checkBotname(client, chatAcceptingConnections=chatAcceptingConnections):
    if checkClientAlive(client):  # Checks if the client is alive
        PRINTER.debugPrint("Sent command !RetrieveBotname to client " + str(client))
        client.send("!RetrieveBotname".encode(FORMAT))  # Sends the RetrieveBotname command to the client
        botname = client.recv(SIZE).decode(FORMAT)      # Recieves the botname from the client
        PRINTER.debugPrint("Recieved botname " + str(botname) + " from client " + str(client))
        purgeDeadClients()   # Purges dead clients
        connectedBotnames = getAllBotnames()   # Gets all botnames currently connected to the server
        while not chatAcceptingConnections.is_accepting():  # While the chatAcceptingConnections is not accepting connections
            if checkClientAlive(client):   # Checks if the client is alive
                PRINTER.debugPrint("Sent command !Waiting to client " + str(client))
                client.send("!Waiting".encode(FORMAT))  # Sends the !Waiting command to the client
                time.sleep(0.5)                         # Waits for the client to recieve the command and then continues the loop untill
                                                        # the chatAcceptingConnections is accepting connections
            else:
                return

        if botname not in connectedBotnames and len(clients) != MAXCLIENTS: # If the botname is not connected to the server and the server is not full
            clients.append(client)            # Adds the client to the clients list
            connectedBotnames.append(botname) # Adds the botname to the connectedBotnames list
            print(PRINTER.centerPrint(f"{botname} has connected to the chatroom!"))
            PRINTER.debugPrint("Sending welcome message to client " + str(client))
            client.send(f"Welcome to the DATA2410 Chatroom!".encode(FORMAT))
            broadcast(f"{botname} is now connected to the chatroom!\n".encode(FORMAT), client)  # Broadcasts the botname to all clients
            broadcast(f"There are now {len(clients)}/{MAXCLIENTS} bots connected.\n".encode(FORMAT), 
                      client)   

        elif len(clients) < MAXCLIENTS:  # If the server is not full
            PRINTER.debugPrint("Sending command !Occupied to client " + str(client))
            client.send(f"!Occupied".encode(FORMAT))  # Sends the !Occupied command to the client, indicating that the botname is already connected
            availableBotnames = set(BOTNAMES).difference(set(connectedBotnames))
            PRINTER.debugPrint("Sending available bot names to the client " + str(client))
            client.send(f"{' and '.join(availableBotnames)} are still available".encode(FORMAT))  # Sends the available botnames to the client
            PRINTER.debugPrint("Closing the socket to client " + str(client))
            client.close()  # Closes the socket to the client

        else:
            PRINTER.debugPrint("Sending command !Full to client " + str(client))
            client.send(f"!Full".encode(FORMAT))  # Sends the !Full command to the client, indicating that the server is full
            PRINTER.debugPrint("Closing the socket to client " + str(client))
            client.close()


# Listening for new connections. Target for threadListen.
# Runs while the chatroom is full
def listen():
    while True:
        PRINTER.debugPrint("Listening for new connections.")
        client, _ = mySocket.accept()  # Accepts a new connection
        PRINTER.debugPrint("Accepted new connection from " + str(client))
        if checkClientAlive(client):  # Checks if the client is alive
            if len(clients) != MAXCLIENTS:  # If the server is not full
                checkBotname(client)  # Checks the botname of the client
            else:  # If the server is full
                PRINTER.debugPrint("Sending command !Full to client " + str(client))
                client.send(f"!Full".encode(FORMAT))   # Sends the !Full command to the client, indicating that the server is full
                PRINTER.debugPrint("Closing the socket to client " + str(client))
                client.close()  # Closes the socket to the client


def main():
    while True:
        try:
            print(PRINTER.centerPrint(f"The server is waiting for {STARTWITH} bots to connect..."))

            while len(clients) < STARTWITH:  # While the has less than the STARTWITH number of bots
                try:
                    PRINTER.debugPrint("Listening for new connections.")
                    client, address = mySocket.accept()  # Accepts a new connection
                    PRINTER.debugPrint("Accepted new connection from " + str(client))
                    checkBotname(client)  # Checks the botname of the client
                except socket.timeout:  # If the server times out
                    continue            # Continues the loop to make it non blocking
                except Exception as e:
                    PRINTER.debugPrint(e)
                    print(PRINTER.centerPrint("\nServer has encountered an error. "+
                                              "The connected bots are being kicked gracefully."))
                    gracefullyKickBots()   # Kicks all bots gracefully
            
            while len(clients) == STARTWITH:
                PRINTER.debugPrint("Removed the socket timeout")
                mySocket.settimeout(None)       # Removes the socket timeout
                print(f"Chatroom is now starting! Chatting will now commence.")
                broadcast(f"Chatroom is now starting! Chatting will now commence.")
                time.sleep(2)
                PRINTER.debugPrint("Starting listing thread.")
                threadListenForNewConnections = threading.Thread(target=listen)  # Creates a thread to listen for new connections
                threadListenForNewConnections.start()                            # Starts the thread
                threadChatroom = threading.Thread(target=chatRoom, args=(client, 0))     # Creates a thread to chat
                PRINTER.debugPrint("Starting chat thread.")
                threadChatroom.start()                                           # Starts the thread
                while True:
                    threadChatroom.join(1)                 # Joins the thread and set a timeout at 1 second
                    threadListenForNewConnections.join(1)  # Joins the thread and set a timeout at 1 second
            quit()

        except KeyboardInterrupt:
            PRINTER.debugPrint("Keyboard interrupt detected. Shutting down gracefully.")
            print(PRINTER.centerPrint("\nKeyboard interrupt detected. Shutting down gracefully."))
            gracefullyKickBots()  # Kicks all bots gracefully

# Starts the main function if the file is run directly
if __name__ == "__main__":
    main()
