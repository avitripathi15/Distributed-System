"""
Avijit Tripathi
Student Id :1001937928
"""


import socket                                               # To access the Socket module
import threading                                            # To access the thread module for calling server B
import os                                                   # To access directory and its files
import time                                                 # To get the time and format it for files
import pickle                                               # Using to seralize and de serialize send and received lists
import queue                                                # To use the queue module and retrive data from thread

############################################################################################################################################################

c=[]                                                        # Creating empty list to store data at thread
b=[]                                                        # Creating Empty list to collect all file data
a = queue.Queue()                                           # Creating a queue for retriving data from thread

############################################################################################################################################################

portB = 5317                                                # port no to connect to Server B
portA = 5555                                                # port no to connect to Client
server_A = socket.gethostbyname(socket.gethostname())       # get host IP address by computer name

############################################################################################################################################################

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        # socket.AF_INET to get ipv4 & socket.SOCK_STREAM for connection oriented TCP (Socket for Client)
sB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # socket for Server B

############################################################################################################################################################

Address1 = (server_A, portA)                                # Variable for storing IP and Port No. for Client to server A
Address2 = (server_A, portB)                                # Variable for storing IP and Port No. for ServerB to server A

############################################################################################################################################################
s.bind(Address1)                                            # Binding the Server to Client
############################################################################################################################################################

def handle_thread(Address):                                 # Function to Thread server B
    sB.connect(Address)                                     # Connecting to server B
    msg = sB.recv(4096)                                     # Storing the received list in variable
    c.append(pickle.loads(msg))                             # Appending the list in c after deserialization
    a.put(c)                                                # adding the list c to queue a

############################################################################################################################################################

x= threading.Thread(target =handle_thread, args = (Address2,)) # Calling the thread to connect to server B
x.start()                                                      # Starting the thread
x.join()
while not a.empty():                                           # checking the data in list a
    temp1= a.get()                                             # storing the data in temporary variable a

############################################################################################################################################################
"""
Converting the string received from server B to a list by splitting the string from the string "&&"
storing it in list b
"""
temp2 = temp1[0]
temp3 = temp2.split(" && ")
b.extend(temp3)

############################################################################################################################################################

def timeformat(t):                                            #Creating a function to arrange time in readable format
    return time.ctime(t)                                      # returning the time after converting it into readable format with ctime module of time

############################################################################################################################################################

"""
1. Reading each file on the defined directory using for loop
2. Using os module to store the name , size and time of creation in list dats
3. Calling timeformat function to convert the time in a presentable format
4. Appending the list a with the elements
"""
for i in os.scandir("C:\Test dir\A"):
    dats = [str(i.name), str(i.stat().st_size), str(timeformat(i.stat().st_atime))]
    b.append(('        '.join(dats)))



############################################################################################################################################################

b.sort()                                             # sorting the list using the sort() method

d = pickle.dumps(b)                                  # Serializing the data of the string b using pickle module

############################################################################################################################################################



print("Starting Server A.....")
s.listen(3)                                          # Listning to the client

############################################################################################################################################################

while True:                                           # Checking for connection
    conn, address = s.accept()                        # Accepting the ip and port no of client
    print("Connected to address", address)
    data = conn.recv(4096).decode("utf-8")            # Receiving data from Client and decoding with file size 4096
    if data == "lab1":                                # Checking For the command
        conn.send(d)                                  # Sending the serialized data to client
    else:                                             # checking for invalid command
        print("invalid command")


conn.close()                                          #Closing connection to client
