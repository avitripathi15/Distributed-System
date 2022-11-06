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
m1=[]
while message != "exit":                                # Checking if the message is exit to exit the loop

    if message[0] == 'l' and message[1] == 'o' and message[2] == 'c' and message[3] == 'k' and message[4] == '-':
        s.send(message.encode("utf-8"))
        a1 = int(message[-1])
        i = 0
        for x in msg:  # Sequentially checking each index of the received list
            if i == a1:
                print(i, "  ", x , "         Locked")  # Sequentially printing the list
            else:
                print(i, "  ", x)  # Sequentially printing the list
            i += 1
        del message
    elif message == 'lab1':                               # Checking if the message is lab1
        s.send(message.encode("utf-8"))
        msg=pickle.loads(s.recv(4096))                  # Deserializing the data received from server
        i = 0
        for x in msg:  # Sequentially checking each index of the received list
            print(i, "  ", x)  # Sequentially printing the list
            i += 1
    elif message[0] == 'u' and message[1] == 'n' and message[2] == 'l' and message[3] == 'o' and message[4] == 'c' and message[5] == 'k' and message[6] == '-':
        s.send(message.encode("utf-8"))
        del message
    else:
        print("invalid command")
    message = input(":\>")  # Taking the next input


else:
    s.close()                                               # Closing Connection to Server A

