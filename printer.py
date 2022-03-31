import os
import random
from time import sleep
import bots

class Printer(): # Class for printing messages in a nice way
    def __init__(self, name) -> None: # Constructor
        self.name = name
        self.names = [x.name for x in bots.botList] + ["Aws"]   # List of all bot names and Aws(the server)
        self.debug = False                                      # Debug mode
    clear = lambda: os.system('cls')                            # Clears the console
    clear()

    def clearConsole(self):         # Clears the console as a method
        os.system('cls')

    def bordered(self, messageFromServer): # Print with border around name
        if self.debug: # If debug mode is on, don't print anything
            return ""

        botName = messageFromServer.split()[0].replace(":", "") # Get bot name from messageFromServer
        if botName not in self.names: # If bot name is not in the list of bot names, return
            return messageFromServer 
    
        lines = botName.splitlines() # Split the bot name into lines
        linechecker = messageFromServer.splitlines() # Split the messageFromServer into lines
        size = int(os.get_terminal_size().columns)  # Get the size of the terminal
        width = max(len(s) for s in lines)          # Get the width of the bot name
        widthchecker = max(len(s) for s in linechecker) # Get the width of the messageFromServer

        tooLong = "" # If the bot name is too long, this will be added to the end of the bot name
        all = messageFromServer.split()[1:] # Get the messageFromServer without the bot name
        extraLines = ' '.join(all) # Join the messageFromServer without the bot name
        extra = [] # List of extra lines
        firstLine = [] # List of first line
        rest = [] # List of rest of the lines
        
        if widthchecker+3 >= size or int(size/2) < widthchecker: 
            # If the messageFromServer is too long, print it in a new line

            for i, x in enumerate(all): # Loop through all the words in the messageFromServer
                firstLine.append(x)
                all[i] = "-1"           # Replace the word iterated through with -1
                extraLines = ' '.join(firstLine)   # Join the first line
                if max(len(s) for s in extraLines.splitlines()) >= int(size/2): # If the first line is too long, break
                    break
                    
            for y in all:  # Loop through all the words in the messageFromServer
                if y != "-1":  # If the word is not -1, add it to the rest list
                    extra.append(y)  # Add the word to the rest list
                    tooLong = ' '.join(extra)  # Join the rest list
                    tooLongChecker = tooLong.splitlines()  # Split the rest list into lines
                    if max(len(s) for s in tooLongChecker) >= int(size/2):  # If the rest list is too long, break
                        if len(rest) > 0: # If the rest list is not empty, break
                            extra.insert(0, "      ")  # Add a space to the front of the rest list
                        extra.append('\n')  # Add a new line to the end of the rest list
                        tooLong = ' '.join(extra)   # Join the rest list
                        rest.append(tooLong)    # Add the rest list to the rest list
                        extra = []  # Reset the rest list
            
            if len(rest) > 0:  # If the rest list is not empty, add it to the rest list
                extra.insert(0, "      ")  # Add a space to the front of the rest list
            extra.append('\n')  # Add a new line to the end of the rest list
            tooLong = ' '.join(extra)  # Join the rest list
            rest.append(tooLong)  # Add the rest list to the rest list
            extra = []  # Reset the rest list


        restStr = ' '.join(rest)  # Join the rest list for printing

        res = ['┌' + '─' * width + '┐']  # Add the top border
        for s in lines:   # Loop through the message
            if s == self.name: # If the bot name is "me", then replace it with "Me"
                s = "Me"
            res.append('│' + (s + ' ' * width)[:width] + '│' + "  " + extraLines)  # Add the bot name and the rest of the message
            
        res.append('└' + '─' * width + '┘' + "  " + restStr + "\n\n")  # Add the bottom border and the rest of the message
        return '\n'.join(res)  # Prints the message in a nice way
    
    # Method for printing a message in the center of the screen
    def centerPrint(self, sentence): 
        if self.debug:  # If debug mode is on, don't print anything
            return ""
        size = int(os.get_terminal_size().columns)  # Get the size of the terminal
        lines = sentence.splitlines()  # Split the sentence into lines
        width = max(len(s) for s in lines)  # Get the width of the sentence
        paddingAmount = size-width  # Get the amount of padding needed
        leftPadding = paddingAmount//2  # Get the amount of left padding needed
        rightPadding = paddingAmount-leftPadding  # Get the amount of right padding needed
        res = [' ' * leftPadding + sentence + ' ' * rightPadding]  # Add the left and right padding
        return ''.join(res)  # Method for printing a message in the center of the screen
        
    def setDebugMode(self, newMode):  # Method for setting debug mode
        self.debug = newMode  # Method for printing a message in the center of the screen
    
    def debugPrint(self, message):  # Method for printing a message in the center of the screen
        if self.debug:  # If debug mode is on, print the message
            print("\n[DEBUG] - " + message)  # Print the message
