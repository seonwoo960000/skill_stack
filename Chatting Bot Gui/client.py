"""
GUI for client.py
"""

import socket
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import sys
import threading

ip = 'localhost'
port = 9999
number_of_rows = 7
HEADER_LENGTH = 10

global btn_connect, text_box, etr_input, btn_close, thread

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

def set_base_rowconfigure(window, row, weight, minsize):
    """set base row configuration
    """
    window.rowconfigure(row, weight=weight, minsize=minsize)

def set_ip_port_entry(window, row, ):
    window.columnconfigure(
        0,
        weight=1,
        minsize=300,
    )
    window.columnconfigure(
        1,
        weight=1,
        minsize=300,
    )

    for col in range(0, 2):
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1,
        )

        frame.grid(
            row=row,
            column=col,
            sticky='nsew',
            padx=5,
            pady=5,
        )

        if col == 0:
            ip_entry = tk.Entry(
                master=frame,
                justify='center'
            )

            ip_entry.pack(
                padx=5,
                pady=5,
                fill="both",
                expand=True,
            )

            ip_entry.insert(0, f'Enter ip (default: {ip})')

            def get_ip(event=None):
                global ip
                ip = ip_entry.get()
                ip_entry.delete(0, 'end')
                ip_entry.insert(0, f"Selected ip: {ip}")
                print(f"ip: {ip}")

            ip_entry.bind(
                '<Return>',
                get_ip,
            )

        else:
            port_entry = tk.Entry(
                master=frame,
                justify='center'
            )

            port_entry.pack(
                padx=5,
                pady=5,
                fill="both",
                expand=True,
            )

            port_entry.delete(0, 'end')
            port_entry.insert(0, f'Enter port (default: {port})')

            def get_port(event=None):
                global port
                port = port_entry.get()
                try:
                    port = int(port)
                    port_entry.delete(0, 'end')

                    if not 0 <= port <= 65535:
                        port_entry.insert(0, "Port number should be between 0 ~ 65535")
                        port = -1
                        return;
                except ValueError:
                    port_entry.delete(0, 'end')
                    port_entry.insert(0, "Port must be integer type")
                    port = -1
                    return;

                port_entry.insert(0, f'Selected port: {port}')

            port_entry.bind(
                '<Return>',
                get_port,
            )

def base_frame(window, row):
    """Set base frames
    """
    frame = tk.Frame(
        master=window,
        relief=tk.RAISED,
        borderwidth=1,
    )

    frame.grid(
        row=row,
        columnspan=2,
        sticky='nsew',
        padx=5,
        pady=5,
    )

    return frame

def btn_connect_server(frame):
    """Button for connecting server
    returns reader, writer
    """
    button = tk.Button(
        master=frame,
        justify='center',
        text='Connect to server',
    )

    button.pack(
        fill="both",
        expand=True,
    )

    return button

def receive_handler(client, text_box):
    while True:
        message = recv_msg(client)
        print("for testing")
        if len(message) > 0:
            print(f'Message received: {message}')
            # text_box.delete('1.0', 'end')
            text_box.insert(tk.END, f'{message}\n')

def bind_btn_connect_with_event_handler(btn_connect):
    """bind connect button with event handler that will connect to the server
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def event_handler(event=None):
        global thread
        try:
            client.connect((ip, port))
            print(f"Connected to server {ip}:{port}")
            thread = threading.Thread(target=receive_handler, args = (client, text_box))
            thread.start()
        except socket.error as exception:
            print(f"Error occurred while connecting to server: {exception}")

    btn_connect.bind(
        '<Button-1>',
        event_handler
    )

    return client

def lbl_name(window, frame, row, name):
    """Create label and name it
    """
    window.rowconfigure(row, minsize=25)

    label = tk.Label(
        master=frame,
        justify='center',
        text=name,
    )

    label.pack(
        fill="both",
        expand=True,
    )

def tbx_display_message_from_server(frame):
    """Create text box to display message from server
    """

    text_box = scrolledtext.ScrolledText(
        master=frame,
        height=4,
        undo=True,
    )

    text_box.pack(
        fill="both",
        expand=True,
    )

    text_box['font'] = ('Roboto', '12')

    return text_box

def etr_input_message(frame):
    """Create input message box for messages to send
    """

    message_entry = tk.Entry(
        master=frame,
    )

    message_entry.pack(
        fill="both",
        expand=True,
    )

    message_entry['font'] = ('Roboto', '12')

    return message_entry

def etr_input_with_event_handler(etr_input, client):
    """bind entry input with event hadler that will receive the input from user
    """

    def enter_message_event_handler(event=None):
        """event handler to handle incoming message when enter is pressed
        """
        message = etr_input.get()
        formatted_message = msg_format(message)
        try:
            client.sendall(formatted_message)
        except Exception as e:
            print(f"{e}")
        print(f'Message sent to ther server: {message}')
        etr_input.delete(0, 'end')

    etr_input.bind(
        '<Return>',
        enter_message_event_handler,
    )



def btn_close_connection(frame):
    """button for closing connection"""

    button = tk.Button(
        master=frame,
        justify='center',
        text='Close connection',
    )
    button.pack(
        fill="both",
        expand=True,
    )

    return button

def btn_close_connection_with_event_handler(btn_close, client):
    """bind close connection button with event handler that closes connection
    """
    def event_handler(event=None):
        global thread
        try:
            client.close()
            print(f'Closed connection')
            thread.join()
            sys.exit()
        except socket.error as error:
            print(f'Error occurred while closing connection: {error}')

    btn_close.bind('<Button-1>', event_handler)

def create_window_and_widgets():
    """Create window and widgets
    :return: window
    """
    window = tk.Tk()
    window.title("Client")
    for row in range(number_of_rows):
        set_base_rowconfigure(window, row, 1, 50)
        global btn_connect, text_box, etr_input, btn_close
        if row == 0:
            set_ip_port_entry(window, row)
        else:
            frame = base_frame(window, row)
            if row == 1:
                btn_connect = btn_connect_server(frame)
            elif row == 2:
                lbl_name(window, frame, row, "Message from server")
            elif row == 3:
                text_box = tbx_display_message_from_server(frame)
            elif row == 4:
                lbl_name(window, frame, row, "Send message to server")
            elif row == 5:
                etr_input = etr_input_message(frame)
            else:
                btn_close = btn_close_connection(frame)

    client = bind_btn_connect_with_event_handler(btn_connect)
    etr_input_with_event_handler(etr_input, client)
    btn_close_connection_with_event_handler(btn_close, client)

    return window

def main():
    window = create_window_and_widgets()
    window.mainloop()
    thread.join()

if __name__ =="__main__":
    main()
