import socket
import os
import random
import threading
import datetime
import ColorsAPI

os.system("clear" if os.name == "posix" else "cls")

def get_server_port():
    server_properties_file = 'server.properties'
    if os.path.exists(server_properties_file):
        print(f"[{datetime.datetime.now()}] {ColorsAPI.FgGreen}[INFO]{ColorsAPI.Reset} Loading server.properties...")
        with open(server_properties_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("server-port="):
                    return int(line.split('=')[1])
    else:
        print(f"[{datetime.datetime.now()}] {ColorsAPI.FgGreen}[INFO]{ColorsAPI.Reset} First startup detected. Generating server.properties...")
        port = random.randint(1024, 49151)  # Choose a random port between 1024 and 49151
        with open(server_properties_file, 'w') as file:
            file.write(f"server-port={port}\n")
        return port

def main():
    server_host = '0.0.0.0'  # Listen on all available network interfaces
    server_port = get_server_port()  # Default Minecraft server port

    if server_port:
        print(f"[{datetime.datetime.now()}] {ColorsAPI.FgGreen}[INFO]{ColorsAPI.Reset} Starting Minecraft server on port {server_port}...")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_socket.bind((server_host, server_port))

        server_socket.listen()

        print(f"[{datetime.datetime.now()}] {ColorsAPI.FgGreen}[INFO]{ColorsAPI.Reset} Server is listening on port {server_port}")

        def input_thread():
            while True:
                command = input("")
                if command == "exit" or command == "stop":
                    print(f"[{datetime.datetime.now()}] {ColorsAPI.FgGreen}[INFO]{ColorsAPI.Reset} Stopping the server...")
                    os._exit(0)

        input_thread = threading.Thread(target=input_thread)
        input_thread.start()

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"[{datetime.datetime.now()}] {ColorsAPI.FgGreen}[INFO]{ColorsAPI.Reset} Grabbed a IP Address: {client_address[0]}:{client_address[1]}")

                data = client_socket.recv(1024)
                
                client_socket.send(data)

                client_socket.close()

        except Exception as e:
            print(f"[{datetime.datetime.now()}] {ColorsAPI.FgRed}[ERROR]{ColorsAPI.Reset} An error occurred: {str(e)}")

        finally:
            server_socket.close()

    else:
        print(f"[{datetime.datetime.now()}] {ColorsAPI.FgRed}[ERROR]{ColorsAPI.Reset} Failed to determine server port.")

if __name__ == "__main__":
    main()
