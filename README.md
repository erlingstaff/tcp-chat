# TCP/IP Chat protocol

A protocol that implements a relationship between a server and multiple connected chatbots.

The protocol works over the IPv4 network family and has a total of ten (10) commands that are used to standardize and control bot-server communication.

The commands have a special prefix that distinguishes them for the clients. The program is comprised of four main parts, the bot definition (bots.py), a printer class for prettifying messages and handling debugging prints (printer.py), the client (client.py) and the server (server.py).

In simple terms, the project works by creating a server on a port, then connecting multiple clients to that server. The server gives each client a sentence to extrapolate words from each round, and the clients respond with their opinions on the “action words” extrapolated from the sentence.
