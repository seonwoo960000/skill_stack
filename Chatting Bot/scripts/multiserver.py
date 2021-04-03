import socket
import selectors
import types

sel = selectors.DefaultSelector()

HOST = ""
PORT = 9999

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print(f"listening on {(HOST, PORT)}")

# calls to this socket will not block the process
# when used with sel.select(), we can wait for events on one or more sockets and then read and write data when ready
lsock.setblocking(False)

# register() : resgister a socket to be monitored with sel.select() for the events you are interesed in
# data is used to store whatever arbitrary data you'd like along with the socket -> returned when select() returns
sel.register(lsock, selectors.EVENT_READ, data=None)

def accept_wrapper(sock) :
    conn, addr = sock.accept()
    print(f"accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')

    # we want to know when the client connection is ready for reading and writing, both of thoes events are set
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask) :
    sock = key.fileobj
    data = key.data

    # when the socket is ready for reading
    if mask & selectors.EVENT_READ :
        recv_data = sock.recv(1024)
        if recv_data :
            data.outb += recv_data
        else :
            print(f"Closing connection to {data.addr}")
            # to unmonitor closing connection
            sel.unregister(sock)
            sock.close()

    # when socket is ready to write
    if mask & selectors.EVENT_WRITE :
        # any received data stored in data.outb is echoed to the client using sock.send()
        if data.outb :
            print(f"Echoing {repr(data.outb)} to {data.addr}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

while True :
    # sel.select() blocks until there are sockets ready for I/O
    # returns a list of (key, events), one for each socket
    events = sel.select(timeout=None)

    # key is a SelectorKey namedtuple that contains a fileobj attribute
    # key.fileobj is the socket object
    # mask is an event mask of the operations that are ready
    for key, mask in events :
        # key.data == None means the socket is the listening socket
        if key.data is None :
            accept_wrapper(key.fileobj)
        # key.data != None means the socket is a client socket that'b been connected
        else :
            service_connection(key, mask)
