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
        full_msg = None
        msg_object = None
        while True:
            msg = self.s.recv(8)
            if len(msg) <= 0:
                break
            full_msg += msg.decode("utf-8")

        if full_msg is not None:
            msg_object = pickle.loads(full_msg)

        return msg_object
