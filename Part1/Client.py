"""
Avijit Tripathi
Student Id :1001937928
"""



import socket                                            #Importing Socket library to create socket
import pickle                                            #Using to seralize and de serialize send and received lists

############################################################################################################################################################


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Creating socket with socket.AF_INET to get ipv4 & socket.SOCK_STREAM for connection oriented TCP
client = socket.gethostbyname(socket.gethostname())     # getting host IP address by computer name
port = 5555                                             #Assigning a Port no to the between Server A and Client

############################################################################################################################################################

s.connect((client,port))                                #Estabilishing connection to server A
print("Connected...")


############################################################################################################################################################

message = input(":\>")                                  #Taking Input Message from the user

############################################################################################################################################################

while message != "exit":                                # Checking if the message is exit to exit the loop
    s.send(message.encode("utf-8"))                     # Sending an encoded message to server
    if message == 'lab1':                               # Checking if the message is lab1
        msg=pickle.loads(s.recv(4096))                  # Deserializing the data received from server
        for x in msg:                                   # Sequentially checking each index of the received list
            print(x)                                    # Sequentially printing the list

    message = input(":\>")                              # Taking the next input

s.close()                                               # Closing Connection to Server A
