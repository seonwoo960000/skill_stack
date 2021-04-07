"""Scripts for client that can connect to a server
(which can accept multiple clients hence the script is named multiclient.py)

Features
    * Able to receive and sned data simultaneously using thread
"""
import socket
import threading
from queue import Queue

HEADER_LENGTH = 10
NUMBER_OF_THREADS = 2
job_queue = Queue()
JOB_SCHEDULING = [0, 1]

def recv_msg(client) :
    """Receives a message from the server and decode it
    :param client:
    :return msg: decoded message
    """
    header_length = int(client.recv(HEADER_LENGTH).decode())
    msg = client.recv(header_length).decode()
    return msg

def msg_format(msg):
    """Formats a message before sending to the server
    :param msg:
    :return msg: msg encoded with header
    """
    if not isinstance(msg, bytes):
        msg = msg.encode()

    header = f"{len(msg): <{HEADER_LENGTH}}".encode()
    return header + msg

def connect_server(ip_='localhost', port_=9999):
    """Returns a connected socket object using IP and PORT
    :param ip_: ip address of the server to connect
    :param port_: port number for the connection
    :return socket: connected socket object(or None when connection fails)
    """
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip_, port_))
        print("Connected to the server")
        return client
    except socket.error as exception:
        print(f"Error occurred while connecting to the server: {exception}")
        return None

# scheduler tasks
def receive_message_from_server(client):
    """ Wait for the message reception from the server and print it
    :param client: connected socket object
    :return None:
    """
    while True:
        try:
            client.settimeout(1)
            msg_from_server = recv_msg(client)
            if len(msg_from_server) > 0:
                print(f"\nMessage from server : {msg_from_server}")
        except socket.timeout as exc:
            continue

def send_message_to_server(client):
    """Send the input message to the server
    :param client: connected socket object
    :return None:
    """
    while True:
        msg_to_server = input("Enter message to send : ")
        msg_to_server = msg_format(msg_to_server)
        client.send(msg_to_server)

def scheduler(client):
    """Schedules threads to receive and send messages
    :param client: connected socket object
    :return None:
    """
    while True:
        task_number = job_queue.get()
        if task_number == 0:
            receive_message_from_server(client)
        elif task_number == 1:
            send_message_to_server(client)

        job_queue.task_done()

def create_threads(client):
    """create threads for scheduler
    :param client: connected socket object
    :return:
    """
    for _ in range(NUMBER_OF_THREADS):
        thread_ = threading.Thread(target=scheduler, args=[client])
        thread_.daemon = True
        thread_.start()

def create_tasks():
    """Create task and put in a job queue
    :return None:
    """
    for job in JOB_SCHEDULING:
        job_queue.put(job)

    job_queue.join()

def main():
    """Main function
        * connect to server
        * create threads and tasks
        * after all tasks end, close the connection
    :return:
    """
    client = connect_server(ip_='localhost', port_=9999)

    create_threads(client)
    create_tasks()

    client.close()

if __name__ == "__main__":
    main()
