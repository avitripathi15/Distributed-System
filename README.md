# distributed_systems

## Socket programming

# Part 1

You will write a program that will generate a composite directory listing from multiple servers. Your project will consist of a client process and two server processes and function as a command line instruction.

Each server, Server A and Server B, will feature a pre-designated directory named directory_a and directory_b b, respectively. When executed, your client will establish a connection to Server A, which will generate a listing of the contents of directory_a (this listing is analogous to the ls l

command on Linux/Bash or dir on Windows). Server A will then establish a connection to Server B, which will generate a listing of the contents of directory_b and return the listing to Server A.

Server A should combine the listing of contents of directory_a and directory_b into a single list sorted by file name. The list should only include the file name, file size, and either the time the file was created or the time the file was last modified. Server A will return the composite list to the Client, which will print the data to the command line.
For the purposes of Lab 1, neither di rectory_a nor directory_b will include subdirectories

# Part 2

Server A and Server B will autonomously synchronize the contents of directory_a and directory_b during runtime, including both files and file metadata. During runtime, any change to the contents of a directory on one server, including adding, deleting, or modifying a file, should be applied at the other server. Files will be added, deleted, or modified with the host’s native file manager (e.g., Windows Explorer for Windows or Finder on macOS), and for the purposes of this lab assignment neither directory will include subdirectories.
Upon startup, Servers A and B will generate an inventory of the contents of their designated directories and compare contents. Any content discrepancy should be addressed, with duplicated files being made consistent based on the most-recent modified-at time.
Any change to the contents of the directory during runtime should be recognized within five seconds. The user should be notified of the servers’ actions in real-time, and the notifications should include which file is being synchronized when applicable. The mechanism by which the directory contents are made consistent is left to the developer’s discretion.

# Part 3

The client will index files 0 to n - 1 when listing directory contents to the user. The user will have the ability to lock files at Server A by running a command: ./lab3 -lock -<index>.
While a file is locked at Server A, any updates to a locked file in directory_b will be placed into a FIFO queue at Server A. When a user unlocks a file by executing ./lab3 -unlock -<index> at the client, updates to that locked file will be applied in the order they were received.
Any file not locked should continue to be updated according to the instructions in Lab #2.
