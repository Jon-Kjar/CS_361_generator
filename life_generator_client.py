import socket
import pickle

class Life_Gen_Client:
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
      
  def sendInitialInfo(self, data):
    pData = pickle.dumps(data)
    self.s.send(pData)

  def recieveInfo(self):
    full_msg = ""
    while True:
      msg = self.s.recv(8)
      if len(msg) <= 0:
        break
      full_msg += msg.decode("utf-8")
        
    if len(full_msg) > 0:
        pFull_msg = pickle.loads(full_msg)
        #print("<Client> Recieved {}".format(pFull_msg))
        
    return pFull_msg  
