import im  # im.py
server= im.IMServerProxy("https://web.cs.manchester.ac.uk/a65914zc/comp28112_ex1/IMserver.php")  # IMServerProxy class


print(server["Robert0"])

print(server["Robert" + str(0)])
