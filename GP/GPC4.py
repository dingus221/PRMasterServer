#gs presence server (29900)
#based on works: prmasterserver, miniircd, gsopensdk, aluigi's works
#
#
#RECHECK input info for wrong characters and lengths    CHECK
#2 TCP SERVER SOCKETs                                   CHECK
#Session number bundled with socket instance            CHECK
#1 DATABASE FOR USER INFORMATION                        CHECK
#PASSWORD GSBASE64DEC, GSENC, MD5-HASHING PROCEDURES    CHECK
#PASSWORD LOGINCHECK_TRANSFORMATION                     CHECK
#PASSWORD -> PROOF TRANSFORMATION                       CHECK
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

    def LOGIN(self, data):
        uname = data.get('uniquenick', '')
        print("LOGIN called for {}".format(uname))

        # FIXME: Check if these restrictions are consistent with the already existing users

        if not (5 < len(uname) < 24): #chkng len of uniquenick
            self.message("\\error\\\\err\\260\\fatal\\\\errmsg\\Username invalid!\\id\\1\\final\\")
            return

        #check  nick for forbidden characters?
        if not self.__valid_nickname_regexp.match(uname):
            self.message("\\error\\\\err\\260\\fatal\\\\errmsg\\Username invalid!\\id\\1\\final\\")
            return

        try:
            user = self.server.user_db[data['uniquenick']]
        except KeyError:
            self.message("\\error\\\\err\\260\\fatal\\\\errmsg\\Username doesn`t exist!\\id\\1\\final\\")
            return

        if data['response'] != gsenc2.PW_Hash_to_Resp(user.password, uname, gpschal, data['challenge']):
            self.message('\\error\\\\err\\260\\fatal\\\\errmsg\\The password provided is incorrect.\\id\\1\\final\\')
            return

        # TODO: What does this mean?
        # 1. The meaning of self.session is following:
        # if we would need to send other commands about buddysystem (that arent implemented), we would need to send 
        # this .session value every time
        # but it seems that in current implementation the stored value is never used
        
        # 2. Adding 30000 so that the value has 5+ digits. Thats untested, maybe it will work with 1+ digit okay
        
        # 3. In other implementations of this server, this session is a randomly generated number, but i think its less 
        # resourceconsuming if we just generate session value from userid. That way we dont need to compare if 
        # randomly generated sessionvalue is unique among other currently connected clients
        self.session = 30000 + int(user.id)

        user.lastip   = self.host
        user.lasttime = time.time()
        user.sesion   = user.sesion + 1

        # generate response
        m =  '\\lc\\2\\sesskey\\' + str(self.session)
        m += '\\proof\\' + gsenc2.PW_Hash_to_Proof(user.password, uname, gpschal, data['challenge'])
        m += '\\userid\\' + str(2000000 + int(user.id))
        m += '\\profileid\\' + str(1000000 + int(user.id))
        m += '\\uniquenick\\' + uname
        m += '\\lt\\1112223334445556667778__\\id\\1\\final\\'
        self.message(m)

        '''\login\\challenge\4jv99yxEnyNWrq6EUiBmsbUfrkgmYF4f\
           uniquenick\EvilLurksInternet-tk\partnerid\0\
           response\45f06fe0f350ae4e3cc1af9ffe258c93\
           firewall\1\port\0\productid\11081\gamename\civ4bts\
           namespaceid\17\sdkrevision\3\id\1\final\
        '''
        
    def NEWUSER(self,data):
        print "NEWUSER"
        if not (5 < len(data.get('nick', '')) < 24 and
                50 > len(data.get('email', '')) > 2 and
                24 > len(data.get('passwordenc', '')) > 7):
            self.message("\\error\\\\err\\0\\fatal\\\\errmsg\\Error creating account, check length!\\id\\1\\final\\")
            return

        if not self.__valid_nickname_regexp.match(data['nick']):
            self.message("\\error\\\\err\\0\\fatal\\\\errmsg\\Error creating account, forbidden characters!\\id\\1\\final\\")
            return

        if data['nick'] in self.server.user_db:
            self.message("\\error\\\\err\\516\\fatal\\\\errmsg\\This account name is already in use!\\id\\1\\final\\")
            return

        pwhash = gsenc2.gsPWDecHash(data['passwordenc'])
        user = self.server.user_db.create(data['nick'], pwhash, data['email'], self.host)
        self.message('\\nur\\\\userid\\{}\\profileid\\{}\\id\\1\\final\\'.format(2000000 + user.id, 1000000 + user.id))

        '''\newuser\\email\qqq@qq\nick\borf-tk\passwordenc\J8DHxh7t\
            productid\11081\gamename\civ4bts\namespaceid\17\uniquenick\borf-tk\
            partnerid\0\id\1\final\
        '''
        
    def GETPROFILE(self,data):
        print "GETPROFILE"
        #Related to buddy-system

    def STATUS(self,data):
        if 'logout' in data:
            self.disconnect('status logout')

    def UNKNOWN(self,data):
        print "unknown command"
        print data
        
    def __parse_read_buffer(self):
        raw = self.__readbuffer[1:].split('\\')
        self.__readbuffer = ''
        # FIXME: This will not work if the read buffer is incomplete or contains multiple messages...
        cooked = [(raw[i], raw[i + 1]) for i in range(0, len(raw) - 1, 2)]
        data = dict(cooked)
        header = cooked[0]
        com = {'login': self.LOGIN,
               'newuser': self.NEWUSER,
               'getprofile': self.GETPROFILE,
               'status': self.STATUS}
        com.get(header[0], self.UNKNOWN)(data)
            
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


# Yes this looks inefficient - but it's clever and never out of date.
# If the DB caching is too bad we can optimize later...
class UserObj:
    # Note: id not considered a field.
    fields = ['name', 'password', 'email', 'county', 'lastip', 'lasttime', 'session']

    def __init__(self, db, uid):
        self.__dict__['db'] = db
        self.__dict__['id'] = int(uid)

    def __getattr__(self, key):
        if key not in UserObj.fields:
            raise AttributeError()
        self.db.dbcur.execute('SELECT {} FROM users WHERE id = ?'.format(key), (self.id, ))
        return self.db.dbcur.fetchone()[0]

    def __setattr__(self, key, value):
        self.db.dbcur.execute('UPDATE users SET {} = ? WHERE id = ?'.format(key), (value, self.id))


class UserDB:
    def __init__(self, path):
        self.dbcon = sqlite3.connect(path, isolation_level=None)
        self.dbcur = self.dbcon.cursor()
        self.dbcur.execute("create table if not exists users ( id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
                           "password TEXT NOT NULL, email TEXT NOT NULL, country TEXT NOT NULL, lastip TEXT NOT NULL, "
                           "lasttime INTEGER NULL DEFAULT '0', session INTEGER NULL DEFAULT '0' );")

    def __contains__(self, uname):
        self.dbcur.execute("SELECT EXISTS(SELECT name FROM users WHERE name=? LIMIT 1);", (uname, ))
        return self.dbcur.fetchone()[0]

    def __getitem__(self, uname):
        try:
            self.dbcur.execute("SELECT id FROM users WHERE name=? LIMIT 1;", (uname, ))
            uid = self.dbcur.fetchone()[0]
            return UserObj(self, uid)
        except:
            raise KeyError()

    def create(self, name, password, email, lastip):
        self.dbcur.execute("INSERT INTO users (name, password, email, lastip) VALUES (?, ?, ?, ?);",
                           (name, password, email, lastip))
        return UserObj(self, self.dbcur.fetchone()[0])
    

class GPServer:
    def __init__(self):
        self.GPClients = {} # Socket --> Client instance

    def remove_GPClient(self, GPClient, quitmsg): #cant delete clients inside their own functions?
        del self.GPClients[GPClient.socket]
        
    def run(self):
        self.user_db = UserDB(dbpath)

        #GP SOCKET
        self.gp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gp.setblocking(0)
        try:
            self.gp.bind(("", 29900))
        except socket.error as err:
            print('Bind failed for gp (29900 TCP)', err)
        self.gp.listen(10)

        #GPS SOCKET
        self.gps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gps.setblocking(0)
        try:
            self.gps.bind(("", 29901))
        except socket.error as err:
            print('Bind failed for gps (29901 TCP)', err)
        self.gps.listen(10)

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
                    lc1 = "\\lc\\1\\challenge\\" + gpschal + "\\id\\1\\final\\"
                    self.GPClients[conn].message(lc1)
                    print 'accepted gp connection from %s:%s.' % (addr[0], addr[1])
            for x in wlst:
                if x in self.GPClients:
                    self.GPClients[x].socket_writable_notification()
                

def main():
    server = GPServer()
    try:
        server.run()
    except KeyboardInterrupt:
        print "GP Interrupted."

main()
