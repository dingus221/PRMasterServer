#gs presence server (29900)
#based on works: prmasterserver, miniircd, gsopensdk
#
#
#ONE TCP SERVER SOCKET BASE
#Session number bundled with socket instance
#ONE DATABASE FOR USER INFORMATION
#CHALLENGE DECODING PROCEDURE
#PASSWORD ENCODING/DECODING, MD5-HASHING PROCEDURES
##<|lc\1 <- (login or newuser)
##>|login -> lc\2
##>|newuser -> nur
##<|bdy,blk,bm
##>|getprofile -> pi
##>|status ->bdy,blk,bm
##?|lt
##?|ka


import socket
import select
import time


class GPClient:
    def __init__(self,server, socket):
        self.server = server
        self.socket = socket        
        (self.host, self.port) = socket.getpeername()
        self.__timestamp = time.time()
        self.__readbuffer = ""
        self.__writebuffer = ""
        self.__sent_ping = False

    def write_queue_size(self):
        return len(self.__writebuffer)

    def __parse_read_buffer(self):
        pass
    
    def socket_readable_notification(self):
        pass

    def socket_writable_notification(self):
        pass

    def disconnect(self, quitmsg):
        print 'GPClient disconnected(' + self.host + ':' + str(self.port) + '). ' + str(quitmsg)
        self.socket.close()
        self.server.remove_GPClient(self, quitmsg)

    def message(self, msg):
        pass

    def check_aliveness(self):
        pass

class GPServer:
    def __init__(self):
        self.GPClients = {} # Socket --> Client instance

    def remove_client(self, GPClient, quitmsg): #cant delete clients inside their own functions?
        del self.GPClients[GPClient.socket]

    def Start(self):
        pass

def Main():
    server = GPServer()
    try:
        server.Start()
    except KeyboardInterrupt:
        print "GP Interrupted."

Main()
