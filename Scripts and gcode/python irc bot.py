
import sys
import socket
import string
import os
import threading
import time
import random
windowtitle = "Nezzbot IRC Client"
from os import system
system("title "+windowtitle)
nickname = raw_input("Nickname: ")
password = raw_input("Password: ")
channel = raw_input("Channel: ")
os.system('cls')
host = "irc.freenode.net"
PORT = 6667
realname = nickname
ident = nickname
s=socket.socket( )
s.connect((host, PORT))
s.send("NICK %s\r\n" % nickname)
s.send("USER %s %s bla :%s\r\n" % (ident, host, realname))
s.send("nickserv IDENTIFY %s\r\n" % password)
s.send("JOIN :%s\r\n" % channel)  		
while True:
	data = s.recv(4096)
	data = data.lower()
	print (data)
	if data.find ( 'ping' ) != -1:
		s.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )  
	if not data.find( "privmsg" ) == -1:
				try:
							IRC_PRIVMSG_Information = [
								data.split( ":" )[ 1 ].split( "!" )[ 0 ], #nick
								data.split( "!" )[ 1 ].split( "@" )[ 0 ], #user  
								data.split( " " )[ 0 ].split( "@" )[ 1 ], #host
								data.split( " " )[ 2 ], #Channel, Message
								":".join( data.split( ":" )[  2: ] ), True ] # Channel or PM
							if not IRC_PRIVMSG_Information[ 3 ][ 0 ] == "#":
								IRC_PRIVMSG_Information[ 5 ] = False
							name = IRC_PRIVMSG_Information[0].capitalize()
							if not nickname.lower() in IRC_PRIVMSG_Information[4]:
								if "action is dead" in IRC_PRIVMSG_Information[4]:
									time.sleep(2)
									s.send("PRIVMSG %s :%s\r\n" % (channel, "ACTION is resurrecting " + name + ""))
									time.sleep(2)
									s.send("PRIVMSG %s :%s\r\n" % (channel, name + " has been resurrected."))
							if nickname.lower() in IRC_PRIVMSG_Information[4]:
								if "hello" in IRC_PRIVMSG_Information[4]: 
									s.send("PRIVMSG %s :%s\r\n" % (channel, "Hello" + " " + name))
								if "disconnect" in IRC_PRIVMSG_Information[4]:
									sys.exit()
								if "set status to away" in IRC_PRIVMSG_Information[4]:
									reason = IRC_PRIVMSG_Information[4]
									reason = reason.split("*")
									print (reason[1])
									s.send("AWAY " + reason[1])
								if "come back" in IRC_PRIVMSG_Information[4]:
									s.send("BACK \n")
								if "what are you?" in IRC_PRIVMSG_Information[4]:
									s.send("PRIVMSG %s :%s\r\n" % (channel, "I am a Cleric, " + name))
								if "roll d20" in IRC_PRIVMSG_Information[4]:
									s.send("PRIVMSG %s :%s\r\n" % (channel, "ACTION rolled a " + str(random.randrange(1,20+1)) + ""))
								if "flip a coin" in IRC_PRIVMSG_Information[4]:
									coin = random.randrange(1,2+1)
									if coin == 1:
										answer = "heads"
									if coin == 2:
										answer = "tails"
									s.send("PRIVMSG %s :%s\r\n" % (channel, "ACTION flips a coin"))
									s.send("PRIVMSG %s :%s\r\n" % (channel, "Coin lands on " + answer))
							print (IRC_PRIVMSG_Information)
				except Exception, Error: print ("Error: %s" % ( Error ))
Sign up for free to join this conversation on GitHub. Already have an account? Sign in to comment
Status API Training Shop Blog About Help
© 2015 GitHub, Inc. Terms Privacy Security Contact
