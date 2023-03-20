# import socket module
from socket import *
from email.utils import formatdate # use for formatting current date

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 80  # HTTP port
# Fill in start
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
# Fill in end
while True:
    modified = 'Mon, 20 Mar 2023 03:17:58 GMT'  # Date webpage was last modified
    modified_since = ''  # Default this value as blank to make the if statement later work.
    etag = '3147526947+gzip'  # Random Etag, since browsers sometimes only use this for 304.
    etag_since = ''
    expires = 'Mon, 20 Mar 2024 03:17:58 GMT'
    content_length = 141 # length (in bytes) of simpleWeb.html

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

        if 'If-None-Match:' in message_str:
            etag_since = message_str.split('If-None-Match: ')[1].split('\r\n')[0]

        # Now, we decide if we need to send the webpage with 200 OK, or to not send the webpage and tell the browser
        # to use its cache (304 Not Modified).
        if modified == modified_since or etag == etag_since:
            # Send 304 Not Modified; dates are the same
            http = f"HTTP/1.1 304 Not Modified\r\nDate: {formatdate(timeval=None, localtime=False, usegmt=True)}\r\nEtag: {etag}\r\nExpires: {expires}\r\nCache-Control: no-cache\r\nLast-Modified: {modified}\r\nContent-Length: {content_length}\r\n\r\n"
            connectionSocket.send(http.encode('utf-8'))
            print("Sent:", http.encode())
        else:
            # Send webpage and 200 OK

            filename = message.split()[1]
            f = open(filename[1:])

            # Read contents of file opened
            outputdata = f.read()  # Fill in start       #Fill in end
            # Send one HTTP header line into socket
            # Fill in start

            http = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nDate: {formatdate(timeval=None, localtime=False, usegmt=True)}\r\nEtag: {etag}\r\nExpires: {expires}\r\nCache-Control: no-cache\r\nLast-Modified: {modified}\r\nContent-Length: {content_length}\r\n\r\n"
            connectionSocket.send(http.encode('utf-8'))
            print("Sent:", http.encode())
            # Fill in end
            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
    except IOError:
        # Send response message for file not found
        # Fill in start
        http = f"HTTP/1.1 404 Not Found\r\n\r\n"
        connectionSocket.send(http.encode('utf-8'))
        print("Sent:", http.encode())

        # Fill in end
        # Close client socket
        # Fill in start
        connectionSocket.close()
        # Fill in end
serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
