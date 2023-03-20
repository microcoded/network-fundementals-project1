# import socket module
from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 80  # HTTP port
# Fill in start
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
# Fill in end
while True:
    modified = 'Monday, 20 Mar 2023 02:07:52 GMT'  # Date webpage was last modified
    modified_since = ''  # Default this value as blank to make the if statement later work.

    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()  # Fill in start              #Fill in end
    print(f'{addr} connected')
    try:
        # TCP packet size is 1500 bytes
        message = connectionSocket.recv(1500)  # Fill in start          #Fill in end

        # Decode the request from the web browser as a string, so we can get If-Modified-Since to know if we need to
        # send 304 Not Modified or 200 OK.
        message_str = message.decode()
        # Check first that we have a modified since, so that we don't get index out of range. Then, get the date.
        if 'If-Modified-Since:' in message_str:
            modified_since = message_str.split('If-Modified-Since: ')[1].split('\r\n')[0]

        filename = message.split()[1]
        f = open(filename[1:])

        # Read contents of file opened
        outputdata = f.read()  # Fill in start       #Fill in end
        # Send one HTTP header line into socket
        # Fill in start

        # Now, we decide if we need to send the webpage with 200 OK, or to not send the webpage and tell the browser
        # to use its cache (304 Not Modified).
        if modified == modified_since:
            # Send 304 Not Modified; dates are the same
            http = f"HTTP/1.1 304 Not Modified\r\n\r\n"
            connectionSocket.send(http.encode('utf-8'))
            print("Sent:", http)
        else:
            # Send webpage and 200 OK
            http = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nLast-Modified: {modified}\r\n\r\n"
            connectionSocket.send(http.encode('utf-8'))
            print("Sent:", http)
            # Fill in end
            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
    except IOError:
        # Send response message for file not found
        # Fill in start
        http = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nLast-Modified: {modified}\r\n"
        connectionSocket.send(http.encode('utf-8'))
        print("Sent:", http)

        # Send 404 webpage
        f = open("404.html")
        outputdata = f.read()
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

        # Fill in end
        # Close client socket
        # Fill in start
        connectionSocket.close()
        # Fill in end
serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
