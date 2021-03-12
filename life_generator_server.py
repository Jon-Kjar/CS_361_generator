# utilized the following for help
# url: https://pythonprogramming.net/buffering-streaming-data-sockets-tutorial-python-3/
import socket
import pickle
from life_generator import get_top_random_toy


class LifeGenServer:
    __SERVER_PORT = 5423
    __HEADER_SIZE = 16

    def __init__(self):
        """
        Initiates everything needed for the socket listening
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((socket.gethostname(), self.port))
        self.s.listen(5)
        print("<Server> Listening on {}:{}...".format(socket.gethostname(), self.__SERVER_PORT))

    def __del__(self):
        print('<Server> Destructor called')
        self.s.close()

    def listening(self):
        """
        Starts the loop for communicating with a client
        :return: None
        """
        while True:
            client_socket, address = self.s.accept()
            print("Connection from " + str(address[0]) + " has been established.")

            data = get_top_random_toy()

            msg = pickle.dumps(data)

            # prepend message length to message
            msg = bytes(f'{len(msg):<{self.__HEADER_SIZE}}', "utf-8") + msg
            client_socket.send(msg)


def main():
    """
    Initiates the life generator server
    :return: None
    """
    lgs = LifeGenServer()
    lgs.listening()


if __name__ == "__main__":
    main()
