# Nettverk og skytjenester Individual Portfolio Assignment

## My own TCP/IP protocol

The protocol implements a relationship between a server and multiple connected bots over a chat terminal.

The protocol works over the IPv4 network family and has a total of ten (10) commands that are used to standardize and control bot-server communication.

The commands are being sent the same way as normal messages but have a special prefix that distinguishes them for the clients. The program is comprised of four main parts, the bot definition (bots.py), my own printer class for prettifying messages and handling debugging prints (printer.py), the client (client.py) and the server (server.py).

In simple terms, the project works by creating a server on a port, then connecting multiple clients to that server. The server gives each client a sentence to extrapolate words from each round, and the clients respond with their opinions on the “action words” in the sentence.
