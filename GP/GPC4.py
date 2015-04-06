#gs presence server (29900)
#based on works: prmasterserver, miniircd, gsopensdk
#
#
#ONE TCP SERVER SOCKET BASE
#Session number bundled with socket instance
#ONE DATABASE FOR USER INFORMATION
#CHALLENGE DECODING PROCEDURE
#PASSWORD ENCODING/DECODING, MD5-HASHING PROCEDURES
##<|lc\1 <- (login or newuser) X
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

    def LOGIN(self,arg):
        print "login" + str(arg)

    def NEWUSER(self,arg):
        print "NEWUSER" + str(arg)

    def GETPROFILE(self,arg):
        print "GETPROFILE" + str(arg)

    def STATUS(self,arg):
        print "STATUS" + str(arg)

    def UNKNOWN(self,arg):
        print "unknown" + str(arg)
        
        

    def __parse_read_buffer(self):
        print "readbuffer"
        print self.__readbuffer
        #get first word and second word to determine command
        raw = self.__readbuffer[1:].split('\\')
        cooked = ['\\'.join(raw[i:i+2]) for i in range(0, len(raw), 2)]
        prepared = dict(item.split('\\') for item in cooked)
        header = cooked[0].split('\\')
        com = {'login':self.LOGIN,
               'newuser':self.NEWUSER,
               'getprofile':self.GETPROFILE,
               'status':self.STATUS}
        com.get(header[0], self.UNKNOWN)(header[1])
        
        '''\login\\challenge\4jv99yxEnyNWrq6EUiBmsbUfrkgmYF4f\
           uniquenick\EvilLurksInternet-tk\partnerid\0\
           response\45f06fe0f350ae4e3cc1af9ffe258c93\
           firewall\1\port\0\productid\11081\gamename\civ4bts\
           namespaceid\17\sdkrevision\3\id\1\final\ '''
    
    def socket_readable_notification(self):
        try:
            data = self.socket.recv(2 ** 10)
            quitmsg = "EOT"
        except socket.error, x:
            data = ""
            quitmsg = x
        if data:
            self.__readbuffer += data
            self.__parse_read_buffer()
            self.__timestamp = time.time()
            self.__sent_ping = False
        else:
            self.disconnect(quitmsg)

    def socket_writable_notification(self):
        try:
            sent = self.socket.send(self.__writebuffer[:1024])
            self.__writebuffer = self.__writebuffer[sent:]    
        except socket.error, x:
            self.disconnect(x)

    def disconnect(self, quitmsg):
        print 'GPClient disconnected(' + self.host + ':' + str(self.port) + '). ' + str(quitmsg)
        self.socket.close()
        self.server.remove_GPClient(self, quitmsg)

    def message(self, msg):
        self.__writebuffer += msg

    def check_aliveness(self):
        pass

class GPServer:
    def __init__(self):
        self.GPClients = {} # Socket --> Client instance

    def remove_GPClient(self, GPClient, quitmsg): #cant delete clients inside their own functions?
        del self.GPClients[GPClient.socket]

    def Start(self):
        a4 = ("0.0.0.0",29900)
        self.gp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gp.setblocking(0)
        try:
            self.gp.bind(a4)
        except socket.error as msg:
            print('Bind failed for gp. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        self.gp.listen(10)
        last_aliveness_check = time.time()
        #main loop
        while True:
            (rlst, wlst, xlst) = select.select(
                [self.gp] + [x.socket for x in self.GPClients.values()],
                [x.socket for x in self.GPClients.values()
                 if x.write_queue_size() > 0],
                [],
                15)
            for x in rlst:
                if x in self.GPClients:
                    self.GPClients[x].socket_readable_notification()
                else:
                    (conn, addr) = x.accept()
                    self.GPClients[conn] = GPClient(self,conn)
                    lc1 = "\\lc\\1\\challenge\\xxxxxxxx\\id\\1\\final\\"
                    self.GPClients[conn].message(lc1)
                    print 'accepted gp connection from %s:%s.' % (addr[0], addr[1])
            for x in wlst:
                if x in self.GPClients:
                    self.GPClients[x].socket_writable_notification()
            now = time.time()
            if last_aliveness_check + 10 < now:
                for client in self.GPClients.values():
                    client.check_aliveness()
                last_aliveness_check = now
                
                    
        

        

def Main():
    server = GPServer()
    try:
        server.Start()
    except KeyboardInterrupt:
        print "GP Interrupted."

Main()
