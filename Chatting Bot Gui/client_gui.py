"""
GUI for client.py
"""
import tkinter as tk
import socket
import multiclient_gui as mcg

ip = 'localhost'
port = 9999
client = socket.socket()

def create_window_and_widgets():
    """Create window and widgets
    :return: window
    """
    window = tk.Tk()

    # Configuring window and widgets
    for i in range(7):
        window.rowconfigure(
            i,
            weight=1,
            minsize=50,
        )

        # ip, port entry
        if i == 0:
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

            for j in range(0, 2):
                frame = tk.Frame(
                    master=window,
                    relief=tk.RAISED,
                    borderwidth=1,
                )

                frame.grid(
                    row=i,
                    column=j,
                    sticky='nsew',
                    padx=5,
                    pady=5,
                )

                if j == 0:
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
                        except Exception as e:
                            port_entry.insert(0, "Port must be integer type")
                            return;

                        port_entry.insert(0, f'Selected port: {port}')

                    port_entry.bind(
                        '<Return>',
                        get_port,
                    )
        else:
            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=1,
            )

            frame.grid(
                row=i,
                columnspan=2,
                sticky='nsew',
                padx=5,
                pady=5,
            )

            # Connect to Server button
            if i == 1:
                button = tk.Button(
                    master=frame,
                    justify='center',
                    text='Connect to server',
                )

                button.pack(
                    fill="both",
                    expand=True,
                )

            # label for "Message from server"
            elif i == 2:
                window.rowconfigure(i, minsize=25)

                label = tk.Label(
                    master=frame,
                    justify='center',
                    text='Message from server',
                )

                label.pack(
                    fill="both",
                    expand=True,
                )

            # Display message from server
            elif i == 3:
                text_box = tk.Text(
                    master=frame,
                    height=4,
                )

                text_box.pack(
                    fill="both",
                    expand=True,
                )

                text_box.insert(tk.END, "hello world")

            # label for "Send message"
            elif i == 4:
                window.rowconfigure(i, minsize=25)

                label = tk.Label(
                    master=frame,
                    justify='center',
                    text='Send message',
                )

                label.pack(
                    fill="both",
                    expand=True,
                )

            # Enter message to send to server
            elif i == 5:
                # event handler
                def enter_message_event_handler(event=None):
                    message = message_entry.get()
                    print(message)
                    message_entry.delete(0, 'end')

                message_entry = tk.Entry(
                    master=frame,
                )

                message_entry.pack(
                    fill="both",
                    expand=True,
                )

                message_entry.bind(
                    '<Return>',
                    enter_message_event_handler
                )

            # Closer server:
            else:
                button = tk.Button(
                    master=frame,
                    justify='center',
                    text='Close connection',
                )
                button.pack(
                    fill="both",
                    expand=True,
                )

    return window

if __name__ == "__main__":

    window = create_window_and_widgets()
    window.mainloop()


