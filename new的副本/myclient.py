""" (Suggest open this file in the VScode and Sublime to get a good reading experience)



# How to run this system???
Prepare:
A folder having myserver.py, myclient.py and ex2utils.py was opened in the terminal
Firstly, run the Command: "python3 myserver.py localhost 8090" to start the server
Secondly, run the Command: "python3 myclient.py localhost 8090" to start the client, which could be used in several terminals representing different clients not just one
There would be some hints on the server when a new client terminal was connected or disconnected (count also works if the client terminal was deliberately closed not through the command number)
(The server would also provide the hint if one name was "successfully" registered and exited for the client but the terminal should be disconnected through the command number)

How to run or use:
In one client terminal, register the name like "Robert", the client terminal will ask you to input the operation number
In another client terminal, register the name like "Ned", the client terminal will ask you to input the operation number
And choose the operation number 1, 2, 3 or 4:

For the 1: (show all screen names connected to the server)
If Robert terminal input 1, the connected names would be shown (including Robert)
Note: If Ned has NOT input 1 before "Robert + 1 operation", the name list would not show Ned, since the server has not received the operation command and saved the name information yet
Note: If Ned has also input 1 before "Robert + 1 operation", the name list would both show the Robert and Ned as the connected clients

For the 2: (send the message to EVERYONE)
If Robert terminal input 2, the system will provide hint and ask you to input the public content like
"Ned, be my hand of the king and help me"
Now, both Robert and Ned terminals would receive and see this message with the time
(But Ned must finish a whole action: input the name and input the any reasonable operation number to finish registering)
The Ned could also do the same thing

For the 3: (send the PRIVATE message)
To see what will happen for the operation 3, firstly, a new client should be created with new name like "Daenerys" with any operation number (except 4) (suggest just 1)
Then, if Robert terminal input 2, and put the information   "I am a king"
These three people would all receive and see this message with the time in their own terminal
If Robert terminal input 3, the system will provide hint and ask you to input the PRIVATE content like
"Ned, the House Targaryen was dangerous"
Then, according to the hint and input the private name for this message like "Ned"
And only the Ned terminal would receive this message: "Ned, the House Targaryen was dangerous", Robert and Daenerys would not receive that

For the 4: (exit)
For these three clients now, any one could input the operation number 4 to disconnect the server, relational message would also be shown in the server terminal
If you close them all, the server will show the number of correct active clients: 0



# How to test the functionality and stability of this system???

1. For the name exists:
Two clients were created with the same name like "Robert", no matter which terminal input the operation number firstly, this terminal would be registered as "Robert"
Another would get the hint after input the message and try to input the message again, if input "Ned", then it was OK
The server will show the number of the client numbers BUT it will also provide hint WHEN the name was registered successfully

2. For the uncorrect operation number(Becasue the input order was fixed and designed, only the content was considered especially the operation number):
One client was registered with any name and input the any number or string except 1, 2, 3 or 4, the hint would be returned and user need to try again

3. For the private chat:
One client was registered with any name and input 3 with any content, then input a new name, which is not registered, it will return the hint that "Sorry, this user name has not been registered, please check and try again"

4. For the disconnect:
One client was registered with "Robert" and input 1 to finish the register
One client was registered with "Ned" and input 1 to finsh and check the list (now there should be two items: Robert and Ned)
If a new client was created still using name "Robert" with operation number 4, the hint will return "This name is already exists"
And input 1 in the "Ned" terminal AGAIN, the Robert client was still there making no difference



"""


import sys
from ex2utils import Client
import os

class IRCClient(Client):
    def onMessage(self, socket, message):
        message = message.encode()
        if message == str("#_DISCONNECT_COMMAND_#").encode():
            print("Disconnect this client......")
            os._exit(0)
            return False

        elif message == str("#_ALREADY_EXIST_COMMAND_#").encode():
            self.name = input("This name is already registered, please try another one: \n")
            return True

        else:
            print(message)  # message on the client
            return True
        
        
    def onStart(self): 
        print("The client has been activated")
        self.name = input("Please register (input) your name here: \n")
        
        
    def listen(self):
        while True:
            print("Operation numbers hint:")
            print("1 Show all screen names connected to the server now.")
            print("2 Input the public message.")
            print("3 Input the private message.")
            print("4 Disconnect this client.")
            operation = input("Please input your operation number: \n")
            
            if (operation == str(1)) or (operation == str(4)):
                message = self.name + "$_$_$_!@#" + operation + "$_$_$_!@#" + "default" + "$_$_$_!@#" + "default"
                # print(message)
                client.send(message.encode())
            
            elif (operation == str(2)):
                content = input("Please type the message sent to everyone: \n")
                message = self.name + "$_$_$_!@#" + operation + "$_$_$_!@#" + content + "$_$_$_!@#" + "default"
                # print(message)
                client.send(message.encode())
                
            elif (operation == str(3)):
                content = input("Please type the PRIVATE message: \n")
                private = input("Please type her/his name to send this private message: \n")
                message = self.name + "$_$_$_!@#" + operation + "$_$_$_!@#" + content + "$_$_$_!@#" + private
                # print(message)
                client.send(message.encode())
                
            else:
                print("Note: Your operation number was not correct, please check and try again ")
          
                
ip = sys.argv[1]
port = int(sys.argv[2])
client = IRCClient()
client.start(ip, port)
client.listen()
