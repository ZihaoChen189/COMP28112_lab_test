import im  
import time
server= im.IMServerProxy("https://web.cs.manchester.ac.uk/a65914zc/comp28112_ex1/IMserver.php")

server_tag = 1   # mutex lock
Robert_time = 0  # the i-th message from Doctor Robert
Ned_time = 0     # the i-th message from Doctor Ned


def Robert():
    global server_tag, Robert_time, Ned_time
    
    if (server_tag == 1):
        print("Ned just said: " + str(server["Ned" + str(Ned_time-1)]) )
        
        server["Robert" + str(Robert_time)] = input("Robert, please input your message here: ")
        Robert_time += 1
 
        print("sending to the server(sleep 3s)")
        time.sleep(3)
        
        server_tag = 0
        print("now, tag = 0 ")
        Ned()
    else:
        print("Sorry, Ned is typing something, please wait ")


def Ned():
    global server_tag, Robert_time, Ned_time
    
    if (server_tag == 0):
        print("Robert just said: " + str(server["Robert" + str(Robert_time-1)]) )
        
        server["Ned" + str(Ned_time)] = input("Ned, please input yout message here: ")
        Ned_time += 1
  
        print("sending to the server(sleep 3s)")
        time.sleep(3)
        
        server_tag = 1
        print("now, tag = 1 ")
        Robert()
    else:
        print("Sorry, Robert is typing something, please wait ")
        

def start_transaction():
    Robert()
    
    
start_transaction()
