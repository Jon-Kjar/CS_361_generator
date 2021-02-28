import socket
import pickle


class LifeGenClient:
    def __init__(self, port):
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((socket.gethostname(), port))
        print("<Client> Connected on {}:{}...".format(socket.gethostname(), port))

    # Deleting (Calling destructor)
    def __del__(self):
        print('<Client> Destructor called')
        self.s.close()

    def send_initial_info(self, data):
        data_pickled = pickle.dumps(data)
        self.s.send(data_pickled)

    def receive_info(self):
        full_msg = b''
        msg_object = None
        new_msg = True
        HEADERSIZE = 10
        while True:
            msg = self.s.recv(16)
            if new_msg:
                print(f"new message length: {msg[:HEADERSIZE]}")
                msglen = int(msg[:HEADERSIZE])
                new_msg = False
            full_msg += msg

            if len(full_msg) - HEADERSIZE == msglen:
                print("full msg received")
                break

        if full_msg is not None:
            msg_object = pickle.loads(full_msg[HEADERSIZE:])

        return msg_object