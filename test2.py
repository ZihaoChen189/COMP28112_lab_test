import im  # im.py
server= im.IMServerProxy("https://web.cs.manchester.ac.uk/a65914zc/comp28112_ex1/IMserver.php")  # IMServerProxy class


# get the value according to the key
# print(server[""])  

# del server["key2"]

print(server.clear())
