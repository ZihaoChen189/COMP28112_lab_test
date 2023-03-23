import sys
from ex2utils import Server
import datetime
import random

class Server(Server):
    def onStart(self):
        self.names = {}  # [name] = socket(object)
        self.active = 0  # how many CLIENTS are connecting to this server (NOT users)
        print("# The server has been activated #")
        print("# Welcome to the 28112 CHAT SYSTEM #")
        print("# Please input the message according to the hint in your client ")
    
    
    def onStop(self):
        return False
    
    
    def onConnect(self, socket):
        self.active += 1  # a client has been connected
        print("Note: A client has been connected")
        print("Now, the number of the active client was: " + str(self.active) )  # print
        
        # prevent the situation: if one people input the registered name and did the exit operation, that registed name might be deliberately deleted
        # therefore, only the client-level name was change as something after successfully registering. the delete operation in the disconnection was accepted.
        socket.name = "null"  
        
        socket.password = str("".join(random.choices('0123456789', k=6)))  # random strings to make sure an unique name tag
        socket.tag = 0  # initialize
    
    
    def onDisconnect(self, socket):
        self.active -= 1  # a client has been disconnected
        print("Note: A client has been disconnected")
        print("Now, the number of the active client was: " + str(self.active) )  # print
        if socket.name != "null":
            self.names.pop(socket.name)  # delete one pair of name-socket in the server-level dictionary
        
        
    def onMessage(self, socket, message):    
        # try:
        (name, operation, content, private) = message.strip().split("$_$_$_!@#")
        if (name not in self.names.keys()) and (socket.tag == 0):  # if socket-level tag was 0 and the input name was not in our registered information dictionary
            print("Note: " + name + " was just registered")    # print in the server
            self.names[name] = socket                              # assign the name-socket pair in the dictionary
            socket.tag = name.encode() + socket.password.encode()  # unique socket-level tag, to make sure one people used different in the client terminal
            socket.name = name
            
            if operation == str(1):
                socket.send(b"Here are all screen names connected to the server:\n")
                socket.send(str(self.names.keys()).encode())  # all the keys(names) in the dictionary 
                return True
            
            elif operation == str(2):
                content = name.encode() + b" (" + (datetime.datetime.now().strftime("%H:%M:%S")).encode() + b") said to everyone: " + content.encode()  # make a content and send to the publci
                for k,v in self.names.items():
                    v.send(content)   # send this message to all the values (socket objects) or (client terminals) 
                print(b"The server received the public message: " + content)
                return True
            
            elif operation == str(3):
                check = self.names.get(private)  # check the user name in the private chat
                if check:  # if this user is connecting to the server
                    check.send(b"The user " + name.encode() + b" just sent the PRIVATE inforamtion to you: " + content.encode())  # send this private information
                else:  # if this user is not registered 
                    socket.send(b"Sorry, this user name has not been registered, please check and try again")
                return True
            
            elif operation == str(4):
                print("The name: " + name + " just exited")
                socket.send(b"#_DISCONNECT_COMMAND_#")  # send the message back to the client and do the disconnection operation
                return True
            
            else:
                socket.send(b"Command Parsing Failed. Please check the operation number and format")
                return True
            
            
        elif (name in self.names.keys()) and (socket.tag == 0):  # the input name already exists
            socket.send(b"#_ALREADY_EXIST_COMMAND_#")
            return True
    
    
        elif (name in self.names.keys()) and (socket.tag == name.encode() + socket.password.encode()):  # if the peope continue operating 
            if operation == str(1):
                socket.send(b"Here are all screen names connected to the server:\n")
                socket.send(str(self.names.keys()).encode())  # all the keys(names) in the dictionary 
                return True
            
            elif operation == str(2):
                content = name.encode() + b" (" + (datetime.datetime.now().strftime("%H:%M:%S")).encode() + b") said to everyone: " + content.encode()  # make a content and send to the publci
                for k,v in self.names.items():
                    v.send(content)   # send this message to all the values (socket objects) or (client terminals) 
                print(b"The server received the public message: " + content)
                return True
            
            elif operation == str(3):
                check = self.names.get(private)  # check the user name in the private chat
                if check:  # if this user is connecting to the server
                    check.send(b"The user " + name.encode() + b" just sent the PRIVATE inforamtion to you: " + content.encode())  # send this private information
                else:  # if this user is not registered 
                    socket.send(b"Sorry, this user name has not been registered, please check and try again")
                return True
            
            elif operation == str(4):
                print("Note: " + name + " just exited")
                socket.send(b"#_DISCONNECT_COMMAND_#")  # send the message back to the client and do the disconnection operation
                return True
            
            else:
                socket.send(b"Command Parsing Failed. Please check the operation number and format")
                return True
            
            
        elif socket.tag != (name.encode() + socket.password.encode()):  # if one people deliberately used other name, not just registered
            socket.send(b"This is NOT the name you just registered, please check and try again")
            return True
            
            
        else:
            socket.send(b"Command Parsing Failed. Please check the operation number and format")
            return True
            
            
        # except:
        #     socket.send(b"Command Parsing Failed. Please check the Format" + b"\nError happened at: " + (datetime.datetime.now().strftime("%H:%M:%S")).encode() )

    
ip = sys.argv[1]
port = int(sys.argv[2])
server = Server()
server.start(ip, port)
