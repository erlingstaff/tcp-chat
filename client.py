import sys
import socket
from bots import *
from printer import Printer
import signal

# CONSTANTS:
SIZE = 1024                                         # 1. Size of messageFromServer received from the server
FORMAT = "utf-8"                                    # 2. Format of messageFromServer

def getArguments():
    # Function for getting command line arguments, they should be: <hostname/ip> <port> <botname>
    # If the user does not provide the correct arguments, the program will print an error messageFromServer and exit.
    # If the user writes "--help" or "-h", the program will print a help messageFromServer and exit.
    commandLineArguments = sys.argv     # Get command line arguments
    debugMode = False                # Set debug mode to false by default
    try:
        # If the user writes "--help" or "-h", the program will print a help messageFromServer and exit.
        if "--help" in commandLineArguments or "-h" in commandLineArguments:
            print(f" ------------- How to ------------- \n\n" +   # Prints help messageFromServer
                "1. Start a client?\n - Write: python3 client.py <ip> <port> <botname>\n\n"
                "2. Choose IP?\n - The server runs on localhost.\n\n" +
                "3. Choose PORT?\n - The port is the same as you chose when creating the server.\n\n" +
                "4. Choose bot?\n - The avaiable bots are: Chuck, Bob, Alice, and Dora.\n\n" +
                "5. Example connection:\n - python3 client.py localhost 8080 Dora \n\n" +
                "5. Optional argument: \n -d or --debug\n -If you want to see debug info, write ex: python3 client.py localhost 8080 Dora -d\n\n" +
                "Good luck :D!\n")
            sys.exit()  # Exit program
        ip = commandLineArguments[1]  # The first argument should be the IP address
        port = int(sys.argv[2])       # The second argument should be the port number, it is cast to an integer for socket.connect()
        
        # If the user wants to run the server in debug mode
        if "-d" in commandLineArguments or "--debug" in commandLineArguments:                                                
            debugMode = True

    except(IndexError, ValueError):     # except-clause for the case that IP and PORT are not specified correctly
        print(f"You seem to have forgotten to specify the IP and/or PORT. Use the --help or -h argument for instructions\n")
        sys.exit()

    allBots = {"Chuck", "Bob", "Alice", "Dora"}  # Acceptable botnames in lowercase for case-insensitivity

    if len(commandLineArguments) < 4:   # check if botname is specified
        print(f"You have not specified a bot. Use the --help or -h argument for instructions\n")
        sys.exit()

    name = sys.argv[3]                   # The third argument should be the bot name
    if name not in allBots:                       # If the bot name is not in the available bots, then the program will exit.
        print(f"Error:\n '{name}' is not a valid botname. Please choose one of the following: \n" +
            " - Chuck\n - Bob\n - Alice\n - Dora\n\n You can use the --help or -h argument for instructions!\n")
        sys.exit()

    return ip, port, name, debugMode                   # Returns the ip, port, botname and debugMode


IP, PORT, NAME, debugMode = getArguments()     # IP, PORT, NAME defined as constants because they will not change.
PRINTER = Printer(NAME)             # My own printer class for prettifying messages and making the program look nicer.
PRINTER.setDebugMode(debugMode)     # Debug mode setter


socketToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # Establish connection with server
PRINTER.debugPrint(f"Socket to server created" + str(socketToServer))
try:                                                                      # Try to connect to server
    socketToServer.connect((IP, PORT))                                    # Connects to the server
    PRINTER.debugPrint(f"Socket to server connected to {IP}:{PORT}")
except:             # If the program is not able to connect to the server, it will print an error messageFromServer and exit.
    print(f"Could not connect to server. Please check your connection, server and command line arguments and try again.\n\n"
    + "You can use the --help or -h command line argument for instructions on how to connect to your server.\n")
    sys.exit()


def signal_handler(signal, frame):  # Function for handling the SIGINT signal (CTR+C)
    PRINTER.debugPrint("You pressed Ctrl+C!")  # Prints a messageFromServer to debug mode
    print("\n\nYou have chosen to exit the program. Goodbye!\n")
    socketToServer.shutdown(1)  # Shuts down the socket
    socketToServer.close()  # Closes the socket
    sys.exit()


def main():
    signal.signal(signal.SIGINT, signal_handler)  # Hook for function for handling CTR+C
    while True:
        try:
            PRINTER.debugPrint("Waiting for messageFromServer")  # Prints a messageFromServer to debug mode
            messageFromServer = socketToServer.recv(SIZE).decode(FORMAT)  # Receives messageFromServer from server
            PRINTER.debugPrint(f"Received messageFromServer from server: {messageFromServer}")  # Prints messageFromServer to debug mode

            match messageFromServer:    # Matches the messageFromServer
                case "!RetrieveBotname":  # If the messageFromServer is "!RetrieveBotname"
                    PRINTER.debugPrint("Encoding and sending botname to server")
                    socketToServer.send(NAME.encode(FORMAT))  # Sends botname to server

                case "!Occupied":  # If the messageFromServer is "!Occupied"
                    print(f"Botname {NAME} is already taken. Please choose another botname.\n")
                    PRINTER.debugPrint("Botname is already taken, waiting for botname alternatives")
                    decodedBotnameTakenMessage = socketToServer.recv(SIZE).decode(FORMAT)  # Receives messageFromServer from server
                    PRINTER.debugPrint(f"Received botname alternatives from server: {decodedBotnameTakenMessage}")  # Prints messageFromServer to debug mode
                    print(f"{decodedBotnameTakenMessage}")
                    PRINTER.debugPrint("Shutting down socket")
                    socketToServer.shutdown(1)  # Shuts down the socket
                    PRINTER.debugPrint("Closing socket")
                    socketToServer.close()
                    sys.exit()

                case "!Finished":  # If the messageFromServer is "!Finished"
                    print(PRINTER.centerPrint("Chatroom has ended. Thank you for chatting!"))
                    print(PRINTER.centerPrint("To start a new chatroom, please restart the server and connect the clients again."))
                    PRINTER.debugPrint("Shutting down socket")
                    socketToServer.shutdown(1)
                    PRINTER.debugPrint("Closing socket")
                    socketToServer.close()
                    sys.exit()

                case "!Full":  # If the messageFromServer is "!Full"
                    print(PRINTER.centerPrint("Chatroom is currently full!"))
                    PRINTER.debugPrint("Shutting down socket")
                    socketToServer.shutdown(1)
                    PRINTER.debugPrint("Closing socket")
                    socketToServer.close()
                    sys.exit()

                case "!Alive":  # If the messageFromServer is "!Alive"
                    pass

                case "!Alive!RetrieveBotname":  # If the messageFromServer is "!Alive!RetrieveBotname"
                    PRINTER.debugPrint("Encoding and sending botname to server")
                    socketToServer.send(NAME.encode(FORMAT))  # Sends botname to server

                case "!Waiting":  # If the messageFromServer is "!Waiting"
                    PRINTER.clearConsole()
                    print(PRINTER.centerPrint("Waiting for the next round to start to let you in..."))

                case _:  # If the messageFromServer is not one of the above, then it is a messageFromServer from the chatroom
                    if messageFromServer.startswith("!Kicked"): # If the messageFromServer starts with "!Kicked"
                        print(PRINTER.centerPrint("You have been kicked from the chatroom."))
                        PRINTER.debugPrint("Shutting down socket")
                        socketToServer.shutdown(1)
                        PRINTER.debugPrint("Closing socket")
                        socketToServer.close()
                        sys.exit()
                    
                    elif messageFromServer.startswith("Aws"): # If the messageFromServer starts with "Aws"
                        print(PRINTER.bordered(messageFromServer))
                        currentBot = getBot(NAME) # Gets the current bot
                        clientResponse = currentBot.getResponse(messageFromServer) # Gets the response from the bot
                        PRINTER.debugPrint(f"Sending client response to server: {clientResponse}") # Prints messageFromServer to debug mode
                        socketToServer.send(f"{NAME}: {clientResponse}".encode()) # messageFromServer is then sent to server.

                    elif messageFromServer.startswith("Dora") or messageFromServer.startswith("Alice") or messageFromServer.startswith("Bob") or messageFromServer.startswith("Chuck"):
                        print(PRINTER.bordered(messageFromServer))  # Prints messageFromServer to console
                    else:
                        print(PRINTER.centerPrint(messageFromServer+"\n")) # Prints messageFromServer to console
        except Exception as e:
            PRINTER.debugPrint(e) # Prints exception to debug mode
            PRINTER.debugPrint("No messageFromServer received, shutting down and closing socket")
            socketToServer.shutdown(1)                                  # Shuts down the socket
            socketToServer.close()                                      # Close connection
            sys.exit()                                                  # Close program


if __name__ == "__main__":      # If the program is run directly, then the main function is called.
    main()
