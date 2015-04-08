#gs presence server (29900)
#based on works: prmasterserver, miniircd, gsopensdk, aluigi's works
#
#
#RECHECK input info for wrong characters and lengths    CHECK
#ONE TCP SERVER SOCKET BASE                             CHECK
#Session number bundled with socket instance            CHECK
#ONE DATABASE FOR USER INFORMATION                      CHECK
#PASSWORD GSBASE64DEC, GSENC, MD5-HASHING PROCEDURES    CHECK
#PASSWORD LOGINCHECK_TRANSFORMATION                     CHECK
#PASSWORD -> PROOF TRANSFORMATION                       CHECK
#GPSearch socket on 29901                               CHECK
##<|lc\1 <- (login or newuser)                          CHECK
##>|login -> lc\2                                       CHECK
##>|newuser -> nur                                      CHECK
##<|bdy,blk,bm                                          Not needed
##>|getprofile -> pi                                    Not needed
##>|status ->bdy,blk,bm                                 Not needed
##?|lt                                                  Not needed
##?|ka                                                  Not needed

import socket
import select
import time
import re
import sqlite3
from gs_consts2 import *
import gsenc2


    

class GPClient:
    __valid_nickname_regexp = re.compile(
        r"^[][\-`_^{|}A-Za-z][][\-`_^{|}A-Za-z0-9]{0,50}$") #copied from miniircd
    
    def __init__(self, server, socket):
        self.server = server
        self.socket = socket        
        (self.host, self.port) = socket.getpeername()
        self.__readbuffer = ""
        self.__writebuffer = ""
        self.session = -1

    def write_queue_size(self):
        return len(self.__writebuffer)

    def LOGIN(self,data):
        print "login"
        if (5<len(data.get('uniquenick',''))<24): #chkng len of uniquenick
            #check  nick for forbidden characters?
            if self.__valid_nickname_regexp.match(data['uniquenick']):
                #check  nick for forbidden characters?
                #check if user exists
                dbdata = self.server.db.get_usr(data['uniquenick'])
                #id, hashencpw, sess
                if dbdata != None:
                    #compare pwderivatives
                    if data['response'] == gsenc2.PW_Hash_to_Resp(dbdata[1],data['uniquenick'],gpschal,data['challenge']):
                        #set session value
                        self.session = 30000 + int(dbdata[0])
                        #update lastip, lasttime, session += 1
                        self.server.db.chk_in_upd(data['uniquenick'], self.host, time.time(), int(dbdata[2]) + 1)
                        #generate response
                        m =  '\\lc\\2\\sesskey\\' + str(self.session)
                        m += '\\proof\\' + gsenc2.PW_Hash_to_Proof(dbdata[1],data['uniquenick'],gpschal,data['challenge'])
                        m += '\\userid\\' + str(2000000 + int(dbdata[0]) )
                        m += '\\profileid\\' + str(1000000 + int(dbdata[0]) )
                        m += '\\uniquenick\\' + data['uniquenick']
                        m += '\\lt\\1112223334445556667778__\\id\\1\\final\\'
                        self.message(m)
                    else:
                        self.message('\\error\\\\err\\260\\fatal\\\\errmsg\\The password provided is incorrect.\\id\\1\\final\\')
                else:
                    self.message("\\error\\\\err\\260\\fatal\\\\errmsg\\Username doesn`t exist!\\id\\1\\final\\")                            
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
            50>len(data.get('email',''))>2   and  #chkng len of email
            24>len(data.get('passwordenc',''))>7): #chkng len of passwenc
            #check  nick for forbidden characters?
            if self.__valid_nickname_regexp.match(data['nick']):
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
                self.message("\\error\\\\err\\0\\fatal\\\\errmsg\\Error creating account, forbidden characters!\\id\\1\\final\\")
        else:
            #wrong len
            self.message("\\error\\\\err\\0\\fatal\\\\errmsg\\Error creating account, check length!\\id\\1\\final\\")
        '''\newuser\\email\qqq@qq\nick\borf-tk\passwordenc\J8DHxh7t\
            productid\11081\gamename\civ4bts\namespaceid\17\uniquenick\borf-tk\
            partnerid\0\id\1\final\
        '''
        

    def GETPROFILE(self,data):
        print "GETPROFILE"
        #Related to buddy-functionality

    def STATUS(self,data):
        #print "STATUS"
        if 'logout' in data:
            self.disconnect('status logout')

    def UNKNOWN(self,data):
        print "unknown command"
        print data
        
        

    def __parse_read_buffer(self):
        #print self.__readbuffer
        #get first and second words to determine command
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


class DBobject:
    def __init__(self,path):
        self.dbcon = sqlite3.connect(path)
        self.dbcur = self.dbcon.cursor()
        self.dbcur.execute("create table if not exists users ( id INTEGER PRIMARY KEY, name TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, country TEXT NOT NULL, lastip TEXT NOT NULL, lasttime INTEGER NULL DEFAULT '0', session INTEGER NULL DEFAULT '0' );")
        self.dbcon.commit()

    def chk_usr(self, uname):#chk if user exists?
        self.dbcur.execute("SELECT EXISTS(SELECT name FROM users WHERE name='" + uname + "' LIMIT 1);")
        return self.dbcur.fetchone()[0]

    def get_usr(self, uname): #get 3 data pieces
        self.dbcur.execute("SELECT id, password, session FROM users WHERE name = '" + uname + "' LIMIT 1;")
        return self.dbcur.fetchone()

    def chk_in_upd(self, uname, lastip, lasttime, session):
        self.dbcur.execute("UPDATE users SET lastip = '" + lastip + "', lasttime = " + str(lasttime) + ", session = " + str(session) + " WHERE name = '" + uname + "';")
        self.dbcon.commit()
        
    def newusr(self,uname,pwhash,email,lastip,lasttime):
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
        a5 = ("0.0.0.0",29901)
        self.gps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gps.setblocking(0)
        try:
            self.gps.bind(a5)
        except socket.error as msg:
            print('Bind failed for gps. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        self.gps.listen(10)
        #main loop
        while True:
            (rlst, wlst, xlst) = select.select(
                [self.gp] + [x.socket for x in self.GPClients.values()],
                [x.socket for x in self.GPClients.values()
                 if x.write_queue_size() > 0],
                [],
                10)
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
                
                    
        

        

def Main():
    server = GPServer()
    try:
        server.Start()
    except KeyboardInterrupt:
        print "GP Interrupted."

Main()
