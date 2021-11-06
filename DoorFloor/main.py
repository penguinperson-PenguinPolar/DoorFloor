# ===================================== #
#   Penguin Polar Door-Floor Hosting    #
#             Project Enum              #
#  Official Copyright of Penguin Polar  #
# ===================================== #

# Import Libaries

import socket, platform

# Logging

open("logs/latest.log", "w").write("")
def printf(msg):
    open("logs/latest.log", "a").write(msg)
    print(msg)

# CreateServer function

def CreateServer(host="127.0.0.1", port=80):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serversocket.bind((host, port))
        serversocket.listen(5)
        while True:
            clientsocket, clientaddr = serversocket.accept(); clientaddr = clientaddr[0]
            rd = clientsocket.recv(10000).decode()
            file = rd.split("\n")
            if (len(file) > 0): printf(f"{clientaddr} Requested {file[0]}")
            data =  b"HTTP/1.1 200 OK\r\n"
            # Text/Html
            if file[0] == "GET / HTTP/1.1\r":
                data += b"Content-Type: text/html\r\n\r\n"
                data += open("public_html/index.html", "rb").read()
                data += b"\r\n\r\n"
            elif file[0] == "GET /shop HTTP/1.1\r":
                data += b"Content-Type: text/html\r\n\r\n"
                data += open("public_html/shop.html", "rb").read()
                data += b"\r\n\r\n"
            elif file[0] == "GET /server HTTP/1.1\r":
                if platform.system() == "Windows":
                    data += b"Content-Type: text/html\r\n\r\n"
                    data += open("public_html/about-server-windows.html", "rb").read()
                    data += b"\r\n\r\n"
                if platform.system() == "Linux":
                    data += b"Content-Type: text/html\r\n\r\n"
                    data += open("public_html/about-server-linux.html", "rb").read()
                    data += b"\r\n\r\n"
            elif file[0] == "GET /penguin-polar HTTP/1.1\r":
                data += b"Content-Type: text/html\r\n\r\n"
                data += open("public_html/about-penguin-polar.html", "rb").read()
                data += b"\r\n\r\n"
            elif file[0] == "GET /accounts HTTP/1.1\r":
                data += b"Content-Type: text/html\r\n\r\n"
                data += open("public_html/accounts.html", "rb").read()
                data += b"\r\n\r\n"
            elif file[0][14:-10].split("/")[0] == "new-account":
                open("accounts/usernames.data", "a").write("\n"+file[0][14:-10].split("/")[1])
                open("accounts/passwords.data", "a").write("\n"+file[0][14:-10].split("/")[2])
            elif file[0][14:-10]!="500":
                usernames = open("accounts/usernames.data", "r").readlines()
                passwords = open("accounts/passwords.data", "r").readlines()
                passwordandusername = (file[0][14:-10].split("/"))
                num1 = 0
                for i in usernames:
                    usernames[num1]=i.replace("\n","")
                    num1 += 1
                num2 = 0
                for i in passwords:
                    passwords[num2]=i.replace("\n","")
                    num2 += 1
                if passwordandusername[0] in usernames and passwordandusername[1] == passwords[usernames.index(passwordandusername[0])]:
                    data += b"Content-Type: text/html\r\n\r\n"
                    data += b"""
                    <!DOCTYPE html>
                    <html>
                        <head>
                            <title>Penguin Polar | Logged-In</title>
                        </head>
                        <body>
                            <center>
                                <h1>Hi """+bytes(passwordandusername[0], "utf-8")+b"""!</h1>
                                <p></p>
                            </center>
                        </body>
                    </html>"""
                    data += b"\r\n\r\n"
                else:
                    data += b"Content-Type: text/html\r\n\r\n"
                    data += b"Wrong username or password"
                    data += b"\r\n\r\n"
            # Binary/Images/Executables
            elif file[0] == "GET /logo-500x500 HTTP/1.1\r":
                data += b"Content-Type: image/jpeg\r\n\r\n"
                data += open("public_html/assets/logo-500x500.jpg", "rb").read()
                data += b"\r\n\r\n"
            clientsocket.sendall(data)
            printf(f"Sent {clientaddr} File: {file[0]}")
            clientsocket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        printf("Closing Down the socket...")
        serversocket.close()

        printf("Shutting Down the Socket...")
        serversocket.shutdown(socket.SHUT_WR)

printf(f"Server Running on http://{socket.gethostbyname(socket.gethostname())}:80 On a {platform.system()} Computer")
CreateServer(host="", port=80)
