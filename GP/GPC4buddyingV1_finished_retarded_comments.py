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
##>|status ->bdy,blk,bm                                 Not needed
##?|lt                                                  Not needed
##?|ka                                                  Not needed
##>|getprofile -> pi                                    Needed
##>bm\1\?msg?                                           Needed
##>delbuddy                                             Needed
##GPS>search                                            Needed
#TODO: make login lettercase indifferent

import socket
import select
import time
import re
import sqlite3
from gs_consts2 import *
import gsenc2


GPClients = {}


class GPSClient:
    def __init__(self, server, socket): #,gpclients_x
        self.server = server
        self.socket = socket
        (self.host, self.port) = socket.getpeername()
        self.__readbuffer = ""
        self.__writebuffer = ""
        

    def disconnect(self, quitmsg):
        print('client disconnected ({}:{}): {}', self.host, self.port, quitmsg)
        self.socket.close()
        self.server.remove_client(self, quitmsg)

    def socket_readable_notification(self):
        try:
            data = self.socket.recv(2 ** 10)
            if not data:
                self.disconnect('EOT')
            else:
                self.GPSHandle(data);
            
            
        except socket.error as err:
            if err.args[0] == errno.EAGAIN or err.args[0] == errno.EWOULDBLOCK:
                print('[{}:{}] Nonblocking read failed, will retry: {}'.format(self.host, self.port, err))
            else:
                print('[{}:{}] Nonblocking read failed hard, disconnect: {}'.format(self.host, self.port, err))
                self.disconnect(err)

    def socket_writable_notification(self):
        #print 'cp1:   ' + self.__writebuffer[:1024]
        try:
            sent = self.socket.send(self.__writebuffer[:1024])
            self.__writebuffer = self.__writebuffer[sent:]    
        except socket.error, x:
            self.disconnect(x)
        

    def write_queue_size(self):
        return len(self.__writebuffer)

    def GPSHandle(self,msg):
        words = msg.split('\\')
        if len(words) < 3 or words[0] != '':
            print("ERROR: parsing strange packet: {}".format(msg))
        command = words[1]
        words = words[1:]
        cooked = [(words[i], words[i + 1]) for i in range(0, len(words) - 1, 2)]
        data = dict(cooked)
        print('GPS_DEBUG {} -> {}'.format(command, data))
        header = cooked[0]
        com = {'search': self.GPS_search,
               'logout': self.GPS_UNKNOWN}
        data['command'] = command # for debug purposes
        com.get(command, self.GPS_UNKNOWN)(data)

    
#\nr\\nick\{0}\LeToast\uniquenick\LeToast-tk\ndone\final\
    def GPS_search(self,data):
        #self.GPS_message("\\nr\\\\nick\\letoast\\uniquenick\\letoast-tk\\ndone\\");
        #self.GPS_message("\\nur\\\\userid\\letoast\\profileid\\100004\\id\\1\\final\\");
        #self.GPS_message("\\nr\\\\ndone\\");
        #self.GPS_message("\\bsr\\24000\\nick\\LESTAT\\partnerid\\0\\profileid\\0\\uniquenick\\LESTAT-tk\\namespaceid\\17\\bsrdone\\final\\")

        #we have data['uniquenick'], now check if that is in db
        #if he is, send his ID
        try:
            user1 = self.server.user_db[data['uniquenick']]
        except KeyError:
            self.GPS_message("\\bsr\\\\bsrdone\\\\final\\")
            print 'no user in db//search'
            return

        #self.GPS_message("\\bsr\\24000\\uniquenick\\LESTAT-tk\\bsrdone\\\\final\\")
        print ''.join(["\\bsr\\", str(30000 + user1.id), "\\uniquenick\\", data['uniquenick'], "\\bsrdone\\\\final\\"])
        self.GPS_message(''.join(["\\bsr\\", str(30000 + user1.id), "\\uniquenick\\", data['uniquenick'], "\\bsrdone\\\\final\\"]))

        #self.GPS_message("\\bsrdone\\\\final\\")
        #\\bsr\\u_pid\\nick\\%s\\firstname\\%s\\lastname\\%s\\email\\%s\\uniquenick\\%s\\namespaceid\\%d
        #\\bsrdone\\
        #gpclients_x[conn].message(lc1)
        #\\bm\\100\\f\\24000\\msg\\|s|3|ss|Zeus gayclub|ls|Gayclub|ip|127.0.0.2|p|0|qm|0\\final\\
        
        #for x in self.gpclients_x:
        #    self.gpclients_x[x].message("\\bm\\100\\f\\24000\\msg\\|s|3|ss|LESTAT|ls|LESTAT|ip|127.0.0.2|p|0|qm|0\\final\\")
                
        #print len(self.gpclients_x)
        #print(data)

    def GPS_message(self, msg):
        self.__writebuffer += msg
        #print 'cp0'
        
    def GPS_UNKNOWN(self, data):
        print('IGNORING data for GPSClient {}:{}: {}'.format(self.host, self.port, data))        

class GPClient:
    __valid_nickname_regexp = re.compile(
        r"^[][\-`_^{|}A-Za-z][][\-`_^{|}A-Za-z0-9]{0,50}$") #copied from miniircd
    
    def __init__(self, server, socket):
        self.server = server
        self.socket = socket        
        (self.host, self.port) = socket.getpeername()
        self.__readbuffer = ""
        self.__writebuffer = ""
        #self.session = -1
        self.id = -1

    def write_queue_size(self):
        return len(self.__writebuffer)

    def LOGIN(self, data):
        uname = data.get('uniquenick', '')
        print("Player {} attempting to login...".format(uname))

        # FIXME: Check if these restrictions are consistent with the already existing users

        if not (5 < len(uname) < 24): #chkng len of uniquenick
            self.message("\\error\\\\err\\260\\fatal\\\\errmsg\\Username invalid!\\id\\1\\final\\")
            return

        #check  nick for forbidden characters?
        if not self.__valid_nickname_regexp.match(uname):
            self.message("\\error\\\\err\\260\\fatal\\\\errmsg\\Username invalid!\\id\\1\\final\\")
            return

        try:
            user = self.server.user_db[uname]
        except KeyError:
            self.message("\\error\\\\err\\260\\fatal\\\\errmsg\\Username doesn`t exist!\\id\\1\\final\\")
            return
        if data['response'] != gsenc2.PW_Hash_to_Resp(user.password, uname, gpschal, data['challenge']):
            
            self.message('\\error\\\\err\\260\\fatal\\\\errmsg\\PW wrong.\\id\\1\\final\\')
            return

        # TODO: What does this mean?
        # 1. The meaning of self.id is following:
        # if we would need to send other commands about buddysystem (that arent implemented), we would need to send 
        # this .id value every time
        # but it seems that in current implementation the stored value is never used
        
        # 2. Adding 30000 so that the value has 5+ digits. Thats untested, maybe it will work with 1+ digit okay
        
        # 3. In other implementations of this server, this session is a randomly generated number, but i think its less 
        # resourceconsuming if we just generate session value from userid. That way we dont need to compare if 
        # randomly generated sessionvalue is unique among other currently connected clients
        self.id = 30000 + int(user.id) #there is self.id and there is user.session - different things!!!
        
        user.lastip   = self.host
        user.lasttime = time.time()
        user.session  = user.session + 1 #this is different session

        # generate response
        m =  '\\lc\\2\\sesskey\\' + str(self.id)
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
        
    def NEWUSER(self, data):
        print("NEWUSER ", data)
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
        user = self.server.user_db.create(data['nick'], pwhash, data['email'], '', self.host)
        self.message('\\nur\\\\userid\\{}\\profileid\\{}\\id\\1\\final\\'.format(2000000 + user.id, 1000000 + user.id))

        '''\newuser\\email\qqq@qq\nick\borf-tk\passwordenc\J8DHxh7t\
            productid\11081\gamename\civ4bts\namespaceid\17\uniquenick\borf-tk\
            partnerid\0\id\1\final\
        '''
        
    def GETPROFILE(self, data):
        #TAKE CARE OF IF SENT TO NONEXISTING USER OR ADDING NONEXISTENT
        #TAKE CARE OF LENGTH AND SENT SYMBOLS
        #SHRINK THE PI, BM and SEARCH RESP MESSAGES TO MIN
        #CHECK THAT U R NOT ADDING URSELF OR WRITING TO URSELF
        #CHECK THAT ID IS INT

        #check if the dud is online
        #if he is, sed his shit
        #shorten the sht
        #check if u r not asking about urself
        #NO, DON'T CHECK, CAUSE OF NONDELETING ON QUIT
        #JUST CHECK SHIT ON SENDING MSGS
        ###print data['profileid']
        ###print self.id

        #data['profileid']
        #uniquenick
        #for x in GPClients:
        #    print GPClients[x].id
        #self.message("\\pi\\\\profileid\\30001\\nick\\LESTAT\\userid\\30001\\sig\\addf62001720ffbac4459ec2f5005643\\uniquenick\\LESTAT-tk\\p/d\\0\\lon\\0.0\\lat\\0.0\\loc\\id\\"+data['id']+"\\final\\")


        
        try:
            user2 = self.server.user_db.getUNbyID(int(data['profileid'])-30000)
        except KeyError:
            print 'no id in db//GETPROF'
            return
        
        self.message(''.join(["\\pi\\\\profileid\\", data['profileid'], "\\sig\\xxxxxx\\uniquenick\\", user2, "\\id\\", data['id'], "\\final\\"]))

        #\bm\1\sesskey\3483058\t\157928340\msg\FzJew fzmanlove\final
        #self.message("\\bm\\1\\f\\24000\\msg\\dongers\\final\\")
        #self.message("\\error\\\\err\\265\\fatal\\\\errmsg\\Username  doesn't exist!\\id\\0\\final\\")
        #Related to buddy-system
        #"\pi\\profileid\24000\nick\LESTAT\userid\24000\email\5pde@nds\sig\DONG\uniquenick\LESTAUT\pid\24000\lon\0.000000\lat\0.000000\loc\\id\2\final\";

    def ADDBUDDY(self,data):
        #\bm\1\f\475776775\msg\I have authorized your request to add me to your list\final\
        #self.message("\\bm\\1\\f\\24000\\msg\\dang\\final\\")
        #self.message("\\authadd\\\\sesskey\\30001\\fromprofileid\\24000\\sig\\addf62001720ffbac4459ec2f5005643\\final\\")
        #self.message("\\pi\\\\profileid\\24000\\nick\\LESTAT\\userid\\24001\\sig\\addf62001720ffbac4459ec2f5005643\\uniquenick\\LESTAT-tk\\p/d\\0\\lon\\0.0\\lat\\0.0\\loc\\id\\3\\final\\")
        #self.message("\\bm\\1\\f\\24000\\msg\\dongers\\final\\")
        print str(data['newprofileid'])
        print self.id
        if data['newprofileid'] == str(self.id):
            print 'ADDBUDDY FAIL. ADDING HIMSELF'
            return
        self.message(''.join(["\\bm\\100\\f\\", data['newprofileid'], "\\msg\\|s|3|ss|", "DONGERS", "\\final\\"]))
        #''.join(["\\bm\\100\\f\\", str(30000 + user.id), "\\msg\\|s|3|ss|", data['uniquenick'], "\\final\\"])
        #self.message("\\bm\\100\\f\\30001\\msg\\|s|3|ss|LESTAT\\final\\")
        #self.message(''.join(["\\bm\\100\\f\\", data['newprofileid'], "\\msg\\|s|3|ss|", "DONGERS", "\\final\\"]))

    def BUDDYMSG(self,data):
        if data['bm'] == '1':
            if (256>=len(data['msg'])>0): #maybe other checkings needed, if it turns out there are forbidden symbols or smth
                for x in GPClients:
                    if str(GPClients[x].id)==data['t']:
                        GPClients[x].message(''.join(["\\bm\\1\\f\\", str(self.id), "\\msg\\", data['msg'], "\\final\\"]))
                        return
                #Message went to noone
        else:
            print "GP_DEBUG, in BUDDYMSG: IGNORING UNKNOWN BM"

    def STATUS(self, data):
        if 'logout' in data:
            self.disconnect('status logout')

    def UNKNOWN(self, data):
        print("ERROR: unknown command, ", data)

    def LOGOUT(self, data):
        self.disconnect('logout')

    def __parse_packet(self, packet):
        words = packet.split('\\')
        if len(words) < 3 or words[0] != '':
            print("ERROR: parsing strange packet: {}".format(packet))
        command = words[1]
        words = words[1:]
        cooked = [(words[i], words[i + 1]) for i in range(0, len(words) - 1, 2)]
        data = dict(cooked)
        print('GP_DEBUG {} -> {}'.format(command, data))
        header = cooked[0]
        com = {'login': self.LOGIN,
               'logout': self.LOGOUT,
               'newuser': self.NEWUSER,
               'getprofile': self.GETPROFILE,
               'addbuddy': self.ADDBUDDY,
               'bm': self.BUDDYMSG,
               'status': self.STATUS}
        data['command'] = command # for debug purposes
        com.get(command, self.UNKNOWN)(data)

    def __parse_read_buffer(self):
        # We assume all packets and with \final\ - but never have that inbetween
        packets = self.__readbuffer.split('\\final\\')
        self.__readbuffer = ''
        # Put last word (maybe empty) back into the readbuffer as we don't know if it is complete yet.
        self.__readbuffer = packets[-1]
        packets = packets[:-1]
        # Now the packets array should contain complete packets and the readbuffer any remaining incomplete ones
        for packet in packets:
            self.__parse_packet(packet)

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
        print 'GP_SENT:   ' + self.__writebuffer[:1024]
        try:
            sent = self.socket.send(self.__writebuffer[:1024])
            self.__writebuffer = self.__writebuffer[sent:]    
        except socket.error, x:
            self.disconnect(x)

    def disconnect(self, quitmsg):
        print 'GPClient disconnected(' + self.host + ':' + str(self.port) + '). ' + str(quitmsg)
        self.socket.close()
        self.server.remove_client(self, quitmsg)

    def message(self, msg):
        self.__writebuffer += msg


# Yes this looks inefficient - but it's clever and never out of date.
# If the DB caching is too bad we can optimize later...
class UserObj:
    # Note: id not considered a field.
    fields = ['name', 'password', 'email', 'country', 'lastip', 'lasttime', 'session']

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

    def getUNbyID(self, ID):
        #used in buddying
        try:
            self.dbcur.execute("SELECT name FROM users WHERE id=? LIMIT 1;", (ID, ))
            return self.dbcur.fetchone()[0]
        except:
            raise KeyError()

    def create(self, name, password, email, country, lastip):
        self.dbcur.execute("INSERT INTO users (name, password, email, country, lastip) VALUES (?, ?, ?, ?, ?);",
                           (name, password, email, country, lastip))
        return UserObj(self, self.dbcur.lastrowid)
    

class GPServer:
    def __init__(self):
        #self.GPClients = {} GPClients is now a global variable. To access from inside GPClient
        self.all_clients = {}
        self.gps_clients = {}

    def remove_client(self, client, quitmsg): #cant delete clients inside their own functions?
        del self.all_clients[client.socket]
        if client.socket in GPClients:
            del GPClients[client.socket]
        if client.socket in self.gps_clients:
            del self.gps_clients[client.socket]
        
    def run(self):
        self.user_db = UserDB(dbpath)

        #GP SOCKET
        self.gp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gp.setblocking(0)
        try:
            self.gp.bind(("", 29900))
        except socket.error as err:
            print('Bind failed for gp (29900 TCP)', err)
            raise err
        self.gp.listen(10)

        #GPS SOCKET
        self.gps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gps.setblocking(0)
        try:
            self.gps.bind(("", 29901))
        except socket.error as err:
            print('Bind failed for gps (29901 TCP)', err)
            raise err
        self.gps.listen(10)

        print('Waiting for clients...')
        while True:
            (rlst, wlst, xlst) = select.select(
                [self.gp, self.gps] + [x.socket for x in self.all_clients.values()],
                [x.socket for x in self.all_clients.values() if x.write_queue_size() > 0],
                [],
                10)
            for x in rlst:
                if x in self.all_clients:
                    self.all_clients[x].socket_readable_notification()
                elif x is self.gp:
                    (conn, addr) = x.accept()
                    client = GPClient(self, conn)
                    GPClients[conn] = client
                    self.all_clients[conn] = client
                    lc1 = "\\lc\\1\\challenge\\" + gpschal + "\\id\\1\\final\\"
                    GPClients[conn].message(lc1)
                    print 'accepted gp connection from %s:%s.' % (addr[0], addr[1])
                else:
                    (conn, addr) = x.accept()
                    client = GPSClient(self, conn) 
                    self.gps_clients[conn] = client
                    self.all_clients[conn] = client
                    print('accepted gps connection from {}:{}.'.format(addr[0], addr[1]))
                    
            for x in wlst:
                if x in self.all_clients:
                    self.all_clients[x].socket_writable_notification()
                    
                
                

def main():
    server = GPServer()
    try:
        server.run()
    except KeyboardInterrupt:
        print "GP Interrupted."

main()