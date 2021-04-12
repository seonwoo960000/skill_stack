import socket
from queue import Queue
import time
import threading

connected_clients = []
HEADER_LENGTH = 10
job_queue = Queue(maxsize=10)
JOB_SCHEDULING = [0, 1, 2, 3]
NUMBER_OF_THREADS = 8

def recv_msg(idx) :
    address, connection = connected_clients[idx]
    try :
        connection.settimeout(0.1)
        header_length = int(connection.recv(HEADER_LENGTH).decode())
        client_address = f"{address[0]}:{address[1]} > "
        return client_address + connection.recv(header_length).decode()
    except socket.timeout as e :
        return ""
    except Exception as e :
        connected_clients.pop(idx)
        return ""

def msg_format(msg) :
    if type(msg) != bytes : msg = msg.encode()
    header = f"{len(msg): <{HEADER_LENGTH}}".encode()
    return header + msg

def create_socket() :
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return server

def bind_listen_socket(server, HOST="", PORT=9999, backlog=5) :
    try :
        server.bind((HOST, PORT))
    except Exception as e :
        print("Socket binding retrying...")
        time.sleep(2)
        bind_listen_socket(server)

    server.listen(5)

def accept_client(server) :
    while True :
        try :
            connection, address = server.accept()
        except Exception as e:
            print(f"Error occured while accepting connection requests : {e}")
        else:
            connected_clients.append((address, connection))

def remove_invalid_connections() :
    global start
    check_interval = 1000
    while True :
        time.sleep(check_interval)
        invalid_address_indexes = []

        for idx, (address, connection) in enumerate(connected_clients) :
            try :
                check_msg = ""
                connection.send(msg_format(check_msg))
            except :
                # means connection isn't valid
                invalid_address_indexes.append(idx)

        for idx in invalid_address_indexes:
            connected_clients.pop(idx)

def list_connected_client() :
    n = 0
    print("==========Connected Clients==========")
    for address, connection in connected_clients :
        print(f"{n} {address}")
        n += 1

    print()

def close_all_connection() :
    for address, connection in connected_clients :
        connection.close()

    connected_clients.clear()

def select_connection_and_send_message(cmd) :
    cmd = cmd.split()
    idx = int(cmd[1])

    print(".stop to stop message sending")
    while True :
        try :
            address, connection = connected_clients[idx]
            message_to_client = input("Enter message to client : ")
            if message_to_client == ".stop" :
                break
            message_to_client = msg_format(message_to_client)
            connection.send(message_to_client)
        except Exception as e :
            print(f"Selected connection{address} isn't valid : {e}")
            break

def broadcast() :
    message_to_clients = input("Enter broadcast message : ")
    message_to_clients = msg_format(message_to_clients)
    for address, connection in connected_clients :
        try :
            connection.send(message_to_clients)
        except :
            continue

def print_list_of_commands() :
    list_of_commands = [
        "1. list : list all valid connections",
        "2. close all connections : close all valid connections",
        "3. select (client ) : connect to specified client",
        "4. broadcast : broadcast to all clients"
    ]
    for command in list_of_commands :
        print(command)

def work(server) :
    print_list_of_commands()

    while True :
        cmd = input("Enter command : ")

        if cmd == "list" :
            list_connected_client()
        elif cmd == "close all connections" :
            close_all_connection()
        elif "select" in cmd :
            select_connection_and_send_message(cmd)
        elif cmd == "broadcast" :
            broadcast()
        else :
            print("Invalid command")
            print_list_of_commands()

def receive_all_incoming_messages() :
    print("Receiving from others")
    while True :
        for idx, (address, connection) in enumerate(connected_clients) :
            message_from_client = recv_msg(idx)
            if len(message_from_client) > 0 :
                print(f"\nMessage from {message_from_client}")

def scheduler(server) :
    while True :
        task_number = job_queue.get()
        if task_number == 0 :
            accept_client(server)
        elif task_number == 1 :
            remove_invalid_connections()
        elif task_number ==  2 :
            receive_all_incoming_messages()
        elif task_number == 3 :
            work(server)
        job_queue.task_done()

def create_threads(server) :
    for _ in range(NUMBER_OF_THREADS) :
        t = threading.Thread(target=scheduler, args=[server])
        t.daemon = True
        t.start()

def create_tasks():
    for JOB in JOB_SCHEDULING:
        job_queue.put(JOB)

    job_queue.join()

def main() :
    server = create_socket()
    bind_listen_socket(server)

    create_threads(server)
    create_tasks()

if __name__ == "__main__" :
    main()
