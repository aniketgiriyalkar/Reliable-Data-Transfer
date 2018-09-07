"""
File:           server.py
Language:       python3
author:         aag5405@cs.rit.edu Aniket Giriyalkar

Description:    This program is an implementation of Web server(server side).
                Here the server sends the objects in response to the requests
                of the client using the HTTP protocol.
"""

import socket
import os


def main():
    """
    The main function.
    :return: None
    """
    # Debug host
    # host = input("Enter host ip address")
    host = socket.gethostbyname(socket.gethostname())

    # Debug port
    # port = input("Enter port number ->")
    port = 3300

    # Create a socket.
    serverSocket = socket.socket()

    # Bind that socket to host and port number.
    serverSocket.bind((host, port))

    # listen is set to 1, so that only one client's request is processed.
    serverSocket.listen(1)
    print("Starting the Server.")

    # Connect with a client.
    connection, address = serverSocket.accept()
    print( "Connection from: " + str( address ) + " established." )

    while True:
        # try:

        # Filename is received from client.
        file_name = connection.recv(1024).decode()

        print("File to be searched is: ",file_name)

        if not os.path.isfile(file_name):
            # If file is not found.
            print("404 Not Found")
            message = "ERROR"
            connection.send(message.encode())

        else:
            # If File is found.
            print("File Found. Calculating the Size...")
            file_size = os.path.getsize(file_name)

            message = "SUCCESS" + str(file_size)

            connection.send(message.encode())
            client_reply = connection.recv( 1024 ).decode()

            # If the client wants to download the file.
            if client_reply[0:4] == "Okay":

                with open( file_name, "rb" ) as file:
                    data_sent = file.read( 1024 )
                    connection.send( data_sent )
                    total_data_sent = len( data_sent )

                    while total_data_sent < file_size:
                        data_sent = file.read( 1024 )
                        connection.send( data_sent )
                        total_data_sent += len( data_sent )
            else:
                print("Client does not want to download the file.")

        # Check if the client has any more requests.
        program_status = connection.recv(1024).decode()

        if program_status != 'Y':
            print("Closing the Connection!")
            # Close the connection.
            connection.close()
            break

        # except FileNotFoundError:
        #     print("File not present at the server")

    # Close the Socket.
    serverSocket.close()


if __name__ == '__main__':
    main()
