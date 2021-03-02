# utilized the following for help
# url: https://pythonprogramming.net/buffering-streaming-data-sockets-tutorial-python-3/
import socket
import pickle


class LifeGenClient:
    HEADER_SIZE = 10

    def __init__(self, port):
        """
        Initiates everything needed for the socket receiving
        :param port: port to communicate with the server
        """
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((socket.gethostname(), port))
        print("<Client> Connected on {}:{}...".format(socket.gethostname(), port))

    # Deleting (Calling destructor)
    def __del__(self):
        print('<Client> Destructor called')
        self.s.close()

    def receive_info(self):
        """
        Receives a message with a header of the size of the message
        :return: the full message without the header
        """
        full_msg = b''
        msg_object = None
        new_msg = True
        while True:
            msg = self.s.recv(16)
            if new_msg:
                print(f"new message length: {msg[:self.HEADER_SIZE]}")
                msg_len = int(msg[:self.HEADER_SIZE])
                new_msg = False
            full_msg += msg

            if len(full_msg) - self.HEADER_SIZE == msg_len:
                print("full msg received")
                break

        if full_msg is not None:
            msg_object = pickle.loads(full_msg[self.HEADER_SIZE:])

        return msg_object
