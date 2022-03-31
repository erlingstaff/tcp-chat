from code import interact
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
MAXROUNDS = 1
MAXCLIENTS = 4
# Global non-constants
connectedBotnames = []
clients = []
interactive = False
commandLineArguments = sys.argv


class AcceptingConnections():
    
    def __init__(self):
        self.accepting = True

    def isAccepting(self):
        return self.accepting
    
    def setNotAccepting(self):
        self.accepting = False
    
    def setAccepting(self):
        self.accepting = True

chatAcceptingConnections = AcceptingConnections()

try:
    if "-h" in commandLineArguments or "--help" in commandLineArguments:
        print("Usage: python3 server.py [port]\n")
        print("Example: python3 server.py 8080\n")
        print("The port should be an integer between 1024 and 65535.\n")
        print("If no port is specified, the program will exit.\n")
        os._exit(0)
    if "-it" in commandLineArguments or "--aws" in commandLineArguments:                                                # If the user wants to run the server in interactive mode
        interactive = True
    if "-c" in commandLineArguments or "--clients" in commandLineArguments:                                             # If the user wants to specify the number of clients
        try:                                                                    # If the user wants to specify the number of clients
            MAXCLIENTS = int(commandLineArguments[commandLineArguments.index("-c") + 1])
        except:
            print("Please specify the number of clients as an integer from 1-4 after -c.\nExample: python3 server.py 8080 -c 4\nIf this paramter is not specified, the default value of 4 will be used.\n")
            os._exit(0)
    if "-r" in commandLineArguments or "--rounds" in commandLineArguments:                                              # If the user wants to specify the number of rounds
        try:
            MAXROUNDS = int(commandLineArguments[commandLineArguments.index("-r") + 1])
        except:
            print("Please specify the number of rounds as an integer after -r.\nExample: python3 server.py 8080 -r 10\nIf this paramter is not specified, the default value of 1 will be used.\n")
            os._exit(0)
    if "-s" in commandLineArguments or "--start" in commandLineArguments:                                               # If the user wants to specify the number of bots to start with
        try:
            STARTWITH = int(commandLineArguments[commandLineArguments.index("-s") + 1])
        except:
            print("Please specify the number of bots to start with as an integer after -s.\nExample: python3 server.py 8080 -s 2\nIf this paramter is not specified, the default value of 2 will be used.\n")
            os._exit(0)
    if "-d" in commandLineArguments or "--debug" in commandLineArguments:                                                # If the user wants to run the server in debug mode
        PRINTER.setDebugMode(True)
    
    port = int(commandLineArguments[1])
    print(PRINTER.centerPrint("Hosting server on port " + str(port)))
except Exception as e:
    print(e)
    print(PRINTER.centerPrint("Port was not specified, use the command line arguments -h or --help for instructions."))
    os._exit(0)

STARTWITH = MAXCLIENTS
ADDRESS = (IP, port)                                            # A constant address variable containing (IP, port)
PRINTER.debugPrint("Address added: " + str(ADDRESS))
                                                                # Creates the TCP socket mySocket on the user specified port
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Creates a socket with the address family INET, which is the IPv4 protocol. SOCK_STREAM is the type of socket.
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Sets the socket to be reusable
mySocket.bind(ADDRESS)                                          # Bind the socket to the address of type (IP, port)
mySocket.listen()                                               # Starts listening for connections                     
mySocket.settimeout(0.5)
PRINTER.debugPrint("Socket 'mySocked' created" + str(mySocket))
PRINTER.debugPrint("Socket setsockopt called, socket is now reusable")
PRINTER.debugPrint("Socket bind called, socket is bound to address: " + str(ADDRESS))
PRINTER.debugPrint("Socket listen called, socket is now listening for connections")
PRINTER.debugPrint("socket has recieved a timeout 0.5s") 
                                                                # Function that runs on threadChat. Will start when four clients is connected to socket
                                                                # Runs MAXROUNDS times, works recursively. Will close program after completion.

def checkClientsAlive():
    for client in clients:
        try:
            PRINTER.debugPrint("Sent command !Alive to client " + str(client))
            client.send(f"!Alive".encode(FORMAT))
        except:
            PRINTER.debugPrint(str(client) + " is not a live, removed from clients list")
            clients.remove(client)
    if len(clients) == 0:
        PRINTER.debugPrint("Socket shutting down")
        mySocket.shutdown(1)
        PRINTER.debugPrint("Socket closed")
        mySocket.close()
        quit()

def purgeDeadClients():
    for client in clients:
        if checkClientAlive(client) == False:
            PRINTER.debugPrint("Client " + str(client) + " is not alive, removed from clients list")
            clients.remove(client)

def checkClientAlive(client):
    try:
        PRINTER.debugPrint("Sent command !Alive to client " + str(client))
        client.send(f"!Alive".encode(FORMAT))
        PRINTER.debugPrint(str(client) + " is alive")
        return True
    except:
        PRINTER.debugPrint(str(client) + " is not alive")
        return False

def getAllBotnames():
    connectedBotnamesUpdated = []
    for client in clients:
        if checkClientAlive(client):
            PRINTER.debugPrint("Sent command !RetrieveBotname to client " + str(client))
            client.send("!RetrieveBotname".encode(FORMAT))
            connectedBotnamesUpdated.append(client.recv(SIZE).decode(FORMAT))
            PRINTER.debugPrint("Recieved botname " + str(connectedBotnamesUpdated[-1]) + " from client " + str(client))
    return connectedBotnamesUpdated
            


def chatRoom(client, roundNumber, maxRounds=MAXROUNDS, chatAcceptingConnections=chatAcceptingConnections):
    try:
        PRINTER.debugPrint("No longer accepting connections for the current round")
        chatAcceptingConnections.setNotAccepting()
        while True:
            if roundNumber == 0:                                                    # Introduction for when the chatroom is initated
                welcomeText = "Welcome to the DATA2410 Chatroom!\n"
                print(PRINTER.centerPrint(welcomeText))                             # Uses my printer to pretty print the text on the server and client
                broadcast(welcomeText.encode(FORMAT))

           
            if roundNumber < maxRounds:
                if not interactive:
                    newRoundText = f"Chatting round {roundNumber+1} is now live. The word is yours, Aws!"
                    print(PRINTER.centerPrint(newRoundText))
                    broadcast(newRoundText.encode(FORMAT))
                    actionWord = random.choice(allWords)
                    PRINTER.debugPrint("Action word is " + actionWord)
                    secondaryActionWordChecker = random.randint(0, 3)
                    if secondaryActionWordChecker == 0:
                        secondaryActionWord = random.choice(allWords)
                        while secondaryActionWord == actionWord:
                            secondaryActionWord = random.choice(allWords)
                    

                    if secondaryActionWordChecker != 0:
                        message = f"Aws: How about {actionWord}"
                        print(PRINTER.bordered(message))
                        time.sleep(1.5)
                    else:                                                               
                        message = f"Aws: What do you think about {actionWord} or {secondaryActionWord}"
                        print(PRINTER.bordered(message))
                        time.sleep(1.5)

                    if checkClientAlive(client) == True:
                        PRINTER.debugPrint("Sent command !ActionWord to client " + str(client))
                        client.send(message.encode(FORMAT))

                    time.sleep(1.5)
                    PRINTER.debugPrint("Waiting for response from " + str(client))
                    actionMessageResponse = client.recv(SIZE).decode(FORMAT)
                    PRINTER.debugPrint("Recieved response from " + str(client) + " : " + actionMessageResponse)
                    print(PRINTER.bordered(actionMessageResponse))
                    broadcast(actionMessageResponse)
                    PRINTER.debugPrint("Now accepting waiting connections for the next round")
                    chatAcceptingConnections.setAccepting()
                    time.sleep(3)
                    chatRoom(client, roundNumber+1)
                else:
                    newRoundText = f"Chatting round {roundNumber+1} is now live. The word is yours, Aws!"
                    print(PRINTER.centerPrint(newRoundText))
                    broadcast(newRoundText.encode(FORMAT))
                    serverMessage = input("What do you want the bots to discuss?\n")
                    PRINTER.debugPrint("Action word is " + actionWord)
                    serverMessage = "Aws: " + serverMessage
                    print(PRINTER.bordered(serverMessage))
                    time.sleep(1.5)

                    if checkClientAlive(client) == True:
                        PRINTER.debugPrint("Sent the current message to " + str(client))
                        client.send(message.encode(FORMAT))

                    time.sleep(1.5)
                    PRINTER.debugPrint("Waiting for response from " + str(client))
                    actionMessageResponse = client.recv(SIZE).decode(FORMAT)
                    PRINTER.debugPrint("Recieved response from " + str(client) + " : " + actionMessageResponse)
                    print(PRINTER.bordered(actionMessageResponse))
                    broadcast(actionMessageResponse)
                    PRINTER.debugPrint("Now accepting waiting connections for the next round")
                    chatAcceptingConnections.setAccepting()
                    time.sleep(3)

                    chatRoom(client, roundNumber+1)

            if roundNumber >= maxRounds:
                broadcast(f"!Finished")
                PRINTER.debugPrint("Finished.")
                print(PRINTER.centerPrint("Chatroom has ended. Thank you for participating!"))
                print(PRINTER.centerPrint("To start a new chatroom, please restart the server and connect the clients again."))
                os._exit(0)

    except Exception:
        PRINTER.debugPrint("Exception in chatRoom")
        print(PRINTER.centerPrint("A bot has suddenly disconnected. The chatroom has been stopped. Thank you for participating!"))
        gracefullyKickBots()


def broadcast(messageToClient, sender=None):

    if type(messageToClient) != bytes:
        PRINTER.debugPrint("Message to client is not bytes, encoding to bytes for transfer.")
        messageToClient = messageToClient.encode(FORMAT)
    checkClientsAlive()
    for client in clients:
        if client != sender:
            PRINTER.debugPrint(f"Sending {messageToClient} to client " + str(client))
            client.send(messageToClient)

    time.sleep(0.5)


def gracefullyKickBots():
    broadcast(f"!Kicked")
    PRINTER.debugPrint("Kicking all bots, then shutting down.")
    mySocket.shutdown(1)
    mySocket.close()
    quit()


def checkBotname(client, chatAcceptingConnections=chatAcceptingConnections):
    if checkClientAlive(client) == True:
        PRINTER.debugPrint("Sent command !RetrieveBotname to client " + str(client))
        client.send("!RetrieveBotname".encode(FORMAT))
        botname = client.recv(SIZE).decode(FORMAT)
        PRINTER.debugPrint("Recieved botname " + str(botname) + " from client " + str(client))
        purgeDeadClients()
        connectedBotnames = getAllBotnames()
        while not chatAcceptingConnections.isAccepting():
            if checkClientAlive(client) == True:
                PRINTER.debugPrint("Sent command !Waiting to client " + str(client))
                client.send("!Waiting".encode(FORMAT))
                time.sleep(0.5)                                 # Wait for chatAcceptingConnections to be accepting
            else:
                return
        
        if botname not in connectedBotnames and len(clients) != MAXCLIENTS:
            clients.append(client)
            connectedBotnames.append(botname)
            print(PRINTER.centerPrint(f"{botname} has connected to the chatroom!"))
            PRINTER.debugPrint("Sending welcome message to client " + str(client))
            client.send(f"Welcome to the DATA2410 Chatroom!".encode(FORMAT))
            #client.send(f"You are connected to {IP}:{port}".encode(FORMAT))
            #client.send(f"Currently, there are {len(clients)} bots connected to the chatroom.".encode(FORMAT))
            #client.send(f"The connected bots are: {' '.join(connectedBotnames)}".encode(FORMAT))
            #client.send(f"The chatroom needs {MAXCLIENTS - (len(connectedBotnames))} more bots to begin.".encode(FORMAT))
            #client.send(f"The chatroom is currently running {MAXROUNDS} rounds.".encode(FORMAT))
            broadcast(f"{botname} is now connected to the chatroom!\n".encode(FORMAT), client)
            broadcast(f"There are now {len(clients)}/{MAXCLIENTS} bots connected to the chatroom.\n".encode(FORMAT), client)

        elif clients.__len__() < MAXCLIENTS:
            PRINTER.debugPrint("Sending command !Occupied to client " + str(client))
            client.send(f"!Occupied".encode(FORMAT))
            availableBotnames = set(BOTNAMES).difference(set(connectedBotnames))
            PRINTER.debugPrint("Sending available bot names to the client " + str(client))
            client.send(f"{' and '.join(availableBotnames)} are still available".encode(FORMAT))
            PRINTER.debugPrint("Closing the socket to client " + str(client))
            client.close()

        else:
            PRINTER.debugPrint("Sending command !Full to client " + str(client))
            client.send(f"!Full".encode(FORMAT))
            PRINTER.debugPrint("Closing the socket to client " + str(client))
            client.close()


# Listening for new connections. Target for threadListen.
# Runs while the chatroom is full
def listen():
    while True:
        PRINTER.debugPrint("Listening for new connections.")
        client, _ = mySocket.accept()
        PRINTER.debugPrint("Accepted new connection from " + str(client))
        if checkClientAlive(client) == True:
            if len(clients) != MAXCLIENTS:
                checkBotname(client)
            else:
                PRINTER.debugPrint("Sending command !Full to client " + str(client))
                client.send(f"!Full".encode(FORMAT))
                PRINTER.debugPrint("Closing the socket to client " + str(client))
                client.close()


def main():
    while True:
        try:
            print(PRINTER.centerPrint(f"The server is waiting for {STARTWITH} bots to connect..."))

            while len(clients) < STARTWITH:                                                        # As long as number of clients is under 4 accept connection and check username
                try:
                    PRINTER.debugPrint("Listening for new connections.")
                    client, address = mySocket.accept()
                    PRINTER.debugPrint("Accepted new connection from " + str(client))
                    checkBotname(client)
                except socket.timeout:
                    continue
                except Exception as e:
                    #print(e)
                    print(PRINTER.centerPrint("\nServer has encountered an error. The connected bots are being kicked gracefully."))
                    gracefullyKickBots()
            
            while len(clients) == STARTWITH:
                PRINTER.debugPrint("Removed the socket timeout")
                mySocket.settimeout(None)
                print(f"Chatroom is now starting! Chatting will now commence.")
                broadcast(f"Chatroom is now starting! Chatting will now commence.")
                time.sleep(2)
                threadList = []

                PRINTER.debugPrint("Starting listing thread.")
                threadListenForNewConnections = threading.Thread(target=listen)
                threadListenForNewConnections.start()
                threadList.append(threadListenForNewConnections)

                for client in clients:
                    currentClientThread = threading.Thread(target=chatRoom, args=(client, 0))
                    currentClientThread.start()
                    threadList.append(currentClientThread)

                PRINTER.debugPrint("Starting chat threads.")
                while True:
                    for thread in threadList:
                        thread.join(1)
            quit()
        except KeyboardInterrupt:
            PRINTER.debugPrint("Keyboard interrupt detected. Shutting down gracefully.")
            print(PRINTER.centerPrint("\nKeyboard interrupt detected. Shutting down gracefully."))
            gracefullyKickBots()

# Starts the main function if the file is run directly
if __name__ == "__main__":
    main()
