import socket
import threading
from queue import Queue

HEADER_LENGTH = 10
NUMBER_OF_THREADS = 2
job_queue = Queue()
JOB_SCHEDULING = [0, 1]

def recv_msg(client) :
    header_length = int(client.recv(HEADER_LENGTH).decode())
    msg = client.recv(header_length).decode()
    return msg

def msg_format(msg) :
    if type(msg) != bytes : msg = msg.encode()
    header = f"{len(msg): <{HEADER_LENGTH}}".encode()
    return header + msg

def connect_server(IP='localhost', PORT=9999) :
    try :
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))
        print("Connected to the server")
        return client
    except :
        print("Error occurred while connecting to the server")
        return None

# scheduler tasks
def receive_message_from_server(client) :
    while True :
        client.settimeout(1)
        try :
            msg_from_server = recv_msg(client)
            if len(msg_from_server) > 0:
                print(f"\nMessage from server : {msg_from_server}")
        except :
            continue

def send_message_to_server(client) :
    while True :
        msg_to_server = input("Enter message to send : ")
        msg_to_server = msg_format(msg_to_server)
        client.send(msg_to_server)

def scheduler(client) :
    while True :
        task_number = job_queue.get()
        if task_number == 0 :
            receive_message_from_server(client)
        elif task_number == 1 :
            send_message_to_server(client)

        job_queue.task_done()

def create_threads(client) :
    for _ in range(NUMBER_OF_THREADS) :
        t = threading.Thread(target=scheduler, args=[client])
        t.daemon = True
        t.start()

def create_tasks() :
    for JOB in JOB_SCHEDULING :
        job_queue.put(JOB)

    job_queue.join()

def main() :
    client = connect_server(IP='143.110.150.121', PORT=9999)

    create_threads(client)
    create_tasks()

    client.close()

if __name__ == "__main__" :
    main()
