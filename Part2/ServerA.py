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
from watchdog.observers import Observer                     # To observe the target directory
from watchdog.events import FileSystemEventHandler          #For File handling
############################################################################################################################################################

c=[]                                                        # Creating empty list to store data at thread
b=[]                                                        # Creating Empty list to collect all file data
a = queue.Queue()                                           # Creating a queue for retriving data from thread

############################################################################################################################################################

portB = 5372                                                # port no to connect to Server B
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
def filefetch():
    l1 = []
    for i in os.scandir("/Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A"):
        dats = [str(i.name), str(i.stat().st_size), str(timeformat(i.stat().st_atime))]
        b.append(('        '.join(dats)))
        l1.append(('        '.join(dats)))
        l1.sort()                               # sorting the list using the sort() method
        b.sort()
    return l1

############################################################################################################################################################

sync1 = filefetch()                              #Fetching the files from the function and printing the original list
print("Before Synchronization")
for i in range(0, len(sync1)):
    print(sync1[i])

############################################################################################################################################################

print("Starting Server A.....")

############################################################################################################################################################

print("After Synchronization")
os.system('rsync -a /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/ /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/')
#Synchronization Using Rsync
sync = filefetch()                              # After Synchronization

for i in range(0, len(sync)):
    print(sync[i])

############################################################################################################################################################

def on_created(event):                            # Funtion that defines the sync process when file is created
    print("Created")
    os.system('rsync -a /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/ /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/')
    sf = filefetch()
    for i in range(0, len(sf)):
        print(sf[i])

############################################################################################################################################################

def on_deleted(event):                           # Funtion that defines the sync process when file is Deleted
    print("Deleted")
    path1 = '/Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/'
    filename = os.path.basename(event.src_path)
    file_path = os.path.join(path1, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        os.system('rsync -a --ignore-existing --recursive --delete /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/ /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/')
    sf = filefetch()
    for i in range(0, len(sf)):
        print(sf[i])

############################################################################################################################################################


def on_modified(event):                         # Funtion that defines the sync process when file is modified
    print("Modified")
    os.system('rsync -a /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/ /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/')
    sf = filefetch()
    for i in range(0, len(sf)):
        print(sf[i])

############################################################################################################################################################


def on_moved(event):                            # Funtion that defines the sync process when file is Moved
    print("Moved")
    os.system('rsync -a /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/ /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/')
    sf = filefetch()
    for i in range(0, len(sf)):
        print(sf[i])

############################################################################################################################################################

def wchdg():                                     # Watchdog functions to check the target directory for changes
    path = '/Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/'
    event_handler = FileSystemEventHandler()

    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.n_moved = on_moved
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

t1 = threading.Thread(target=filefetch)                 #To synchronization Files During runtime
t1.start()
t = threading.Thread(target = wchdg)                     #Thread to Check Target Directory During Runtime
t.start()

d = pickle.dumps(sync)                                  # Serializing the data of the string b using pickle module

############################################################################################################################################################



print("Starting Server A.....")
s.listen(3)                                          # Listning to the client

############################################################################################################################################################

while True:                                           # Checking for connection
    conn, address = s.accept()                        # Accepting the ip and port no of client
    print("Connected to address", address)
    data = conn.recv(4096).decode("utf-8")            # Receiving data from Client and decoding with file size 4096
    while data != "exit":                                # Checking For the command
        if data == "lab1":
            sync2 = filefetch()                          # Serializing the data of the string b using pickle module

            d = pickle.dumps(sync2)
            conn.send(d)                                  # Sending the serialized data to client
        else:                                               # checking for invalid command
            print("invalid command")
            break
        data = conn.recv(4096).decode("utf-8")

    else:                                             # checking for invalid command
        conn.close()

############################################################################################################################################################
