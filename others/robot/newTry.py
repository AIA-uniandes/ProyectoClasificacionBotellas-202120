# Echo client program
import socket
import time
#Server creation	
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("localhost", 31001))
serversocket.listen(5) #5 eingehende Verbindungen erlauben
HOST = "157.253.197.229" # The remote host
PORT = 30002 # The same port as used by the server
print ("Starting Program")
count = 0

while (count < 1000):
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 s.connect((HOST, PORT)) # Bind to the port 
 s.listen(5) # Now wait for client connection.
 c, addr = s.accept() # Establish connection with client.
 try:
   msg = c.recv(1024)
   print ("Pose Position = ", msg)
   msg = c.recv(1024)
   print ("Joint Positions = ", msg)
   msg = c.recv(1024)
   print ("Request = ", msg)
   time.sleep(1)
   if msg == "asking_for_data":
     count = count + 1
   print ("The count is:", count)
   time.sleep(0.5)
   print ("")
   time.sleep(0.5)
   c.send("(200,50,45)");
   print ("Send 200, 50, 45")
 except socket.error as socketerror:
   print (count)

c.close()
s.close()
print ("Program finish")