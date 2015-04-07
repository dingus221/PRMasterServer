#gs presence server (29900)
#based on works: prmasterserver, miniircd, gsopensdk, aluigi's works
#
#
#RECHECK input info for wrong characters and lengths
#ONE TCP SERVER SOCKET BASE                             CHECK
#Session number bundled with socket instance
#ONE DATABASE FOR USER INFORMATION                      CHECK
#PASSWORD GSBASE64DEC, GSENC, MD5-HASHING PROCEDURES    CHECK
#PASSWORD LOGINCHECK_TRANSFORMATION                     CHECK
#PASSWORD -> PROOF TRANSFORMATION                       CHECK
##<|lc\1 <- (login or newuser)                          CHECK
##>|login -> lc\2                                       ?
##>|newuser -> nur                                      CHECK
##<|bdy,blk,bm
##>|getprofile -> pi
##>|status ->bdy,blk,bm
##?|lt
##?|ka

import socket
import select
import time
import sqlite3
from gs_consts2 import *
import gsenc2


class GPClient:
    def __init__(self, server, socket):
        self.server = server
        self.socket = socket        
        (self.host, self.port) = socket.getpeername()
        self.__timestamp = time.time()
        self.__readbuffer = ""
        self.__writebuffer = ""
        self.__sent_ping = False
        self.session = -1#??? session number generator utility
        #?make session be equal or derived from logindb id field

    def write_queue_size(self):
        return len(self.__writebuffer)

    def LOGIN(self,data):
        print "login"
        #check  nick for forbidden characters?
        #check if user exists
        dbdata = self.server.db.get_usr(data['uniquenick'])
        
        #id, hashencpw, sess
        if dbdata != None:
            #compare pwderivatives
            if data['response'] == gsenc2.PW_Hash_to_Resp(dbdata[1],data['uniquenick'],gpschal,data['challenge']):
                print "PW CHECK"
                #set session value
                self.session = 3000000 + int(dbdata[0])
                #update lastip, lasttime, session += 1 (session here - number of times logged in)
                
                #generate response
                m =  '\\lc\\2\\sesskey\\' + str(3000000+int(dbdata[0]))
                m += '\\proof\\' + gsenc2.PW_Hash_to_Proof(dbdata[1],data['uniquenick'],gpschal,data['challenge'])
                m += '\\userid\\' + str(2000000 + int(dbdata[0]) )
                m += '\\profileid\\' + str(1000000 + int(dbdata[0]) )
                m += '\\uniquenick\\' + data['uniquenick']
                m += '\\lt\\NONREPRESENTATIONALISM__\\id\\1\\final\\'
                self.message(m)
            else:
                print "WRONG PW"
                self.message('\\error\\\\err\\260\\fatal\\\\errmsg\\The password provided is incorrect.\\id\\1\\final\\')
        else:
            self.message("\\error\\\\err\\260\\fatal\\\\errmsg\\Username doesn`t exist!\\id\\1\\final\\")                            
        #make session be equal or derived from logindb id field
        #self.message("\\error\\\\err\\516\\fatal\\\\errmsg\\This account name is already in use!\\id\\1\\final\\")
        '''\login\\challenge\4jv99yxEnyNWrq6EUiBmsbUfrkgmYF4f\
           uniquenick\EvilLurksInternet-tk\partnerid\0\
           response\45f06fe0f350ae4e3cc1af9ffe258c93\
           firewall\1\port\0\productid\11081\gamename\civ4bts\
           namespaceid\17\sdkrevision\3\id\1\final\
        '''
        

    def NEWUSER(self,data):
        print "NEWUSER"
        if (5<len(data.get('nick',''))<24 and  #checking len of nick
            len(data.get('email',''))>2   and  #chkng len of email
            len(data.get('passwordenc',''))>4):#chkng len of passwenc
            #check  nick for forbidden characters?
            #check if user exists
            if self.server.db.chk_usr(data['nick']) == 0:
                #prepare password
                pwhash = gsenc2.gsPWDecHash(data['passwordenc'])
                #store data
                id_ = self.server.db.newusr(data['nick'], pwhash, data['email'], self.host, int(time.time()))
                #send response                
                self.message('\\nur\\\\userid\\'+str(2000000+int(id_))+'\\profileid\\' + str(1000000+int(id_)) + '\\id\\1\\final\\')
            else:
                #name exists
                self.message("\\error\\\\err\\516\\fatal\\\\errmsg\\This account name is already in use!\\id\\1\\final\\")
        else:
            #wrong len
            self.message("\\error\\\\err\\0\\fatal\\\\errmsg\\Error creating account, check length!\\id\\1\\final\\")
        '''\newuser\\email\qqq@qq\nick\borf-tk\passwordenc\J8DHxh7t\
            productid\11081\gamename\civ4bts\namespaceid\17\uniquenick\borf-tk\
            partnerid\0\id\1\final\
        '''
        

    def GETPROFILE(self,data):
        print "GETPROFILE"

    def STATUS(self,data):
        print "STATUS"

    def UNKNOWN(self,data):
        print "unknown"
        print data
        
        

    def __parse_read_buffer(self):
        print "readbuffer"
        print self.__readbuffer
        #get first word and second word to determine command
        raw = self.__readbuffer[1:].split('\\')
        self.__readbuffer = ''
        cooked = ['\\'.join(raw[i:i+2]) for i in range(0, len(raw), 2)]
        prepared = dict(item.split('\\') for item in cooked)
        header = cooked[0].split('\\')
        com = {'login':self.LOGIN,
               'newuser':self.NEWUSER,
               'getprofile':self.GETPROFILE,
               'status':self.STATUS}
        com.get(header[0], self.UNKNOWN)(prepared)
        
    
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

class DBobject:
    def __init__(self,path):
        self.dbcon = sqlite3.connect(path)
        self.dbcur = self.dbcon.cursor()
        self.dbcur.execute("create table if not exists users ( id INTEGER PRIMARY KEY, name TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, country TEXT NOT NULL, lastip TEXT NOT NULL, lasttime INTEGER NULL DEFAULT '0', session INTEGER NULL DEFAULT '0' );")
        self.dbcon.commit()

    def chk_usr(self, uname):#chk if user exists?
        print "chk_usr"
        self.dbcur.execute("SELECT EXISTS(SELECT name FROM users WHERE name='" + uname + "' LIMIT 1);")
        return self.dbcur.fetchone()[0]

    def get_usr(self, uname): #get 3 data pieces
        print "get_usr"
        self.dbcur.execute("SELECT id, password, session FROM users WHERE name = '" + uname + "' LIMIT 1;")
        return self.dbcur.fetchone()

    def chk_in_upd(self, uname, lastip, lasttime, session):
        print "chk_in_upd"
        #???

    def newusr(self,uname,pwhash,email,lastip,lasttime):
        print "db_new_usr"
        self.dbcur.execute("INSERT INTO users VALUES(NULL,'"+uname+"','"+pwhash+"','"+email+"','','"+lastip+"',"+str(lasttime)+",0);")
        self.dbcon.commit()
        #return id
        self.dbcur.execute("SELECT id FROM users WHERE name = '" + uname + "' LIMIT 1;")
        return self.dbcur.fetchone()[0]
    

class GPServer:
    def __init__(self):
        self.GPClients = {} # Socket --> Client instance

    def remove_GPClient(self, GPClient, quitmsg): #cant delete clients inside their own functions?
        del self.GPClients[GPClient.socket]
        
    def Start(self):
        self.db = DBobject(dbpath)
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
