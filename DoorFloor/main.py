# ===================================== #
#   Penguin Polar Door-Floor Hosting    #
#             Project Enum              #
#  Official Copyright of Penguin Polar  #
# ===================================== #

# Import Libaries

import socket, os

# CreateServer function

def CreateServer(host="127.0.0.1", port=80):
    os.chdir("public_html/")
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serversocket.bind((host, port))
        serversocket.listen(5)
        while True:
            clientsocket, clientaddr = serversocket.accept(); clientaddr = clientaddr[0]
            rd = clientsocket.recv(10000).decode()
            file = rd.split("\n")
            if (len(file) > 0): print(f"{clientaddr} Requested {file[0]}")
            data =  "HTTP/1.1 200 OK\r\n"
            if rd.split("/")[1] == " HTTP":
                data += "Content-Type: text/html\r\n\r\n"
                data += open("index.html", "r").read()
                data += "\r\n\r\n"
            if rd.split("/")[1] == "logo-500x500 HTTP":
                data += "Content-Type: image/jpeg\r\n\r\n"
                data += open("assets/logo-500x500.jpg", "rb").read()
                data += "\r\n\r\n"
            clientsocket.sendall(data.encode())
            print(f"Sent {clientaddr} File: {file[0]}")
            clientsocket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        print("Shutting Down the Server...")

    serversocket.close()
    serversocket.shutdown(socket.SHUT_WR)

print(f"Server Running on http://{socket.gethostbyname(socket.gethostname())}:80")
CreateServer(port=8080 )