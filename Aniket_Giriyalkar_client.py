"""
File:           client.py
Language:       python3
author:         aag5405@cs.rit.edu Aniket Giriyalkar

Description:    This program is an implementation of Client side. The Client
                sends requests to the server, receives response to those
                requests and displays object using the HTTP protocol.
"""

import socket

def main():
    """
    The main function.
    :return: None
    """
    # Debug host
    # host = input("Enter host ip address ->")
    host = socket.gethostbyname(socket.gethostname())

    # Debug port number.
    # port = input("Enter port number ->")
    port = 3300

    # Create socket.
    clientSocket = socket.socket()

    print("Trying to connect to server")

    # Send Connection request to the server.
    clientSocket.connect((host, port))
    print("Connected to the Server.")

    # Enter the name of the file to search in the server.
    filename = str(input("Enter Filename(or press q to Quit) -> "))

    while filename != "q":

        # Send the filename to the server.
        clientSocket.send(filename.encode())

        # Response from the server.
        data_received = clientSocket.recv(1024).decode()

        if data_received[:7] == 'SUCCESS':
            # Display the Header Form of message
            print("HTTP/1.1 200 OK")

            fileSize = int(data_received[7:])
            # Ask the client for download.
            downloadOption = input("File " + filename
                                   + " exists.\nIt's size is " + str(fileSize)
                                   +" bytes.\nDo you still wish to download?"
                                   "(Y for yes, any other key for No) -> ")

            if downloadOption == "Y":
                clientSocket.send("Okay".encode())

                # Save the downloaded file as received_filename.
                newfile = open("received_" + filename, "wb")

                data_received = clientSocket.recv(1024)
                total_data_received = len(data_received)
                newfile.write(data_received)

                # Write until end of the file is encountered.
                while total_data_received < fileSize:
                    data_received = clientSocket.recv(1024)
                    total_data_received += len(data_received)
                    newfile.write(data_received)

                print("Download Completed!")
        else:
            # Error message when File is not found.
            print("404 Not Found")

        filename = input("Do you wish to continue?"
                         "(Y for yes, any other key to quit) -> ")

        # Send the current status of the program.
        clientSocket.send(filename.encode())

        if filename != "Y":
            break
        else:
            # Begin next set of request.
            filename = str(input
                           ("Enter Filename(or press q to Quit)-> "))
    # Close the Socket.
    clientSocket.close()


if __name__ == '__main__' :
    main()
