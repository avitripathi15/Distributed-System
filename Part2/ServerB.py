"""
Avijit Tripathi
Student Id :1001937928
"""

import socket                                            # Importing Socket library to create socket
import os                                                # Used to get the extention to the directory details
import threading                                         # To access the thread module for calling server B
import time                                              # Used to get the time of creation for files in directory
import pickle                                            #Using to seralize and de serialize send and received lists
from watchdog.observers import Observer                  # To observe the target directory
from watchdog.events import FileSystemEventHandler       #For File handling
############################################################################################################################################################

a = []                                               # Initializing a blank list to save the files information of directories

############################################################################################################################################################


port = 5372                                           # Assigning a Port no to the between Server B and Server A
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
def filefetch():
    b = []
    for i in os.scandir("/Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B"):
        dats = [str(i.name), str(i.stat().st_size), str(timeformat(i.stat().st_atime))]
        b.append(('        '.join(dats)))
        b.sort()
    return b

############################################################################################################################################################

a = filefetch()                                         #Fetching the files from the function and printing the original list
print("Before Synchronization")
for i in range(0, len(a)):
    print(a[i])

############################################################################################################################################################

a = (' && '.join(a))                                   # Joining the elements of the list with and to easily seprate it in Server A and append them in a list

############################################################################################################################################################

d = pickle.dumps(a)                                    # Serializing the object before sending it to the  client

############################################################################################################################################################

print("Starting Server B.....")

print("After Synchronization")                          # Synchronization after setting connection between the servers
os.system('rsync -ad /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/ /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/')

sync = filefetch()

for i in range(0, len(sync)):
    print(sync[i])

############################################################################################################################################################


def on_created(event):                                  # Funtion that defines the sync process when file is created
    print("Created")
    os.system('rsync -a /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/ /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/')
    sf = filefetch()
    for i in range(0, len(sf)):
        print(sf[i])

############################################################################################################################################################

def on_deleted(event):                                  # Funtion that defines the sync process when file is Deleted
    print("Deleted")
    path1 = '/Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/'
    filename = os.path.basename(event.src_path)
    file_path = os.path.join(path1, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        os.system('rsync -a --ignore-existing --recursive --delete /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/ /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/')
    sf = filefetch()
    for i in range(0, len(sf)):
        print(sf[i])

############################################################################################################################################################

def on_modified(event):                                 # Funtion that defines the sync process when file is modified
    print("Modified")
    os.system('rsync -a /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/ /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/')
    sf = filefetch()
    for i in range(0, len(sf)):
        print(sf[i])

############################################################################################################################################################

def on_moved(event):                                    # Funtion that defines the sync process when file is Moved
    print("Moved")
    os.system('rsync -a /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/ /Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/A/')
    sf = filefetch()
    for i in range(0, len(sf)):
        print(sf[i])

############################################################################################################################################################


def wchdg():                                             # Watchdog functions to check the target directory for changes
    path = '/Users/avi/Documents/Lab2_Tripathi_axt7928/Test_dir/B/'
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

############################################################################################################################################################

t1 = threading.Thread(target=filefetch)                 #To synchronization Files During runtime
t1.start()
t = threading.Thread(target = wchdg)                    #Thread to Check Target Directory During Runtime
t.start()


s.listen()                                            # Listning to server A

############################################################################################################################################################

while True:                                           # Checking for server a connection
    conn, address = s.accept()                        # Accepting the port and address of Server A
    print("Connected to address", address)            # Acknowledgement of connection
    conn.send(d)                                      # Sending Serialize data to server A

############################################################################################################################################################


