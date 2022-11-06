"""
Avijit Tripathi
Student Id :1001937928
"""

import socket                                        # Importing Socket library to create socket
import os                                            # Used to get the extention to the directory details
import time                                          # Used to get the time of creation for files in directory
import pickle                                        #Using to seralize and de serialize send and received lists

############################################################################################################################################################

a = []                                               # Initializing a blank list to save the files information of directories

############################################################################################################################################################


port = 5317                                           # Assigning a Port no to the between Server B and Server A
server = socket.gethostbyname(socket.gethostname())   # Get host IP address by computer name

############################################################################################################################################################


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # Creating socket with socket.AF_INET to get ipv4 & socket.SOCK_STREAM for connection oriented TCP

############################################################################################################################################################

s.bind((server,port))                                 # Binding the socket to Server A

############################################################################################################################################################

def timeformat(t):                                   #Creating a function to arrange time in readable format
    return time.ctime(t)                             # returning the time after converting it into readable format with ctime module of time

############################################################################################################################################################
"""
1. Reading each file on the defined directory using for loop
2. Using os module to store the name , size and time of creation in list dats
3. Calling timeformat function to convert the time in a presentable format
4. Appending the list a with the elements
"""

for i in os.scandir("C:\Test dir\B"):
    dats = [str(i.name), str(i.stat().st_size), str(timeformat(i.stat().st_atime))]
    a.append(('        '.join(dats)))

############################################################################################################################################################


a = (' && '.join(a))                                   # Joining the elements of the list with and to easily seprate it in Server A and append them in a list

############################################################################################################################################################

d = pickle.dumps(a)                                    # Serializing the object before sending it to the  client

############################################################################################################################################################

print("Starting Server B.....")
s.listen()                                            # Listning to server A

############################################################################################################################################################

while True:                                           # Checking for server a connection
    conn, address = s.accept()                        # Accepting the port and address of Server A
    print("Connected to address", address)            # Acknowledgement of connection
    conn.send(d)                                      # Sending Serialize data to server A
