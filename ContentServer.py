import socket #for infromation transfer between code
import pickle
import ContentMain as m

def socketFunction():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 5432))
    s.listen(5)

    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established!")
        data = m.getsearchedParagraph()

        msg = pickle.dumps(data)
        print("DATA\t" + str(msg))
        msg = bytes(f'{len(msg):<{10}}', "utf-8") + msg
        # clientsocket.send(msg)

        # msg = m.getsearchedParagraph()
        print(msg)
        clientsocket.send(msg)

def main():
    socketFunction()
    # m.getsearchedParagraph()

if __name__ == "__main__":
    main()

