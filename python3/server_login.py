#!/usr/bin/env python3

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
import time
import re
import sqlite3
import logging

import config_login
from gs_network import NetworkClient, NetworkServer
import gs_enc2


class GPSClient(NetworkClient):
    def __init__(self, server, sock):
        super().__init__(server, sock)


class GPClient(NetworkClient):
    _valid_nickname_regexp = re.compile(r"^[][\-`_^{|}A-Za-z][][\-`_^{|}A-Za-z0-9]{0,50}$")

    def __init__(self, server, sock):
        super().__init__(server, sock)
        self.session = -1
        self.handlers = {'login': self.handle_login,
                         'logout': self.handle_logout,
                         'newuser': self.handle_newuser,
                         'getprofile': self.handle_getprofile,
                         'status': self.handle_status}

        # Initial greeting
        self.respond('lc', 1, 'challenge', config_login.challenge, 'id', 1)

    def handle_login(self, data):
        uname = data.get('uniquenick', '')
        logging.info("Player %s attempting to login.", uname)

        # FIXME: Check if these restrictions are consistent with the already existing users

        if not (5 < len(uname) < 24):
            self.error(260, 'fatal', 'Username invalid!')
            return

        if not self._valid_nickname_regexp.match(uname):
            self.error(260, 'fatal', 'Username invalid!')
            return

        try:
            user = self.server.user_db[uname]
        except KeyError:
            self.error(260, 'fatal', 'Username does not exist!')
            return

        if data['response'] != gs_enc2.PW_Hash_to_Resp(user.password, uname, config_login.challenge, data['challenge']):
            self.error(260, 'fatal', 'Incorrect password!')
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
        user.session  = user.session + 1

        self.respond('lc', 2,
                     'sesskey', self.sesion,
                     'proof', gsenc2.PW_Hash_to_Proof(user.password, uname, gpschal, data['challenge']),
                     'userid', 2000000 + int(user.id),
                     'profileid', 1000000 + int(user.id),
                     'uniquenick', uname,
                     'lt', '1112223334445556667778__',
                     'id', 1)


        '''\login\\challenge\4jv99yxEnyNWrq6EUiBmsbUfrkgmYF4f\
           uniquenick\EvilLurksInternet-tk\partnerid\0\
           response\45f06fe0f350ae4e3cc1af9ffe258c93\
           firewall\1\port\0\productid\11081\gamename\civ4bts\
           namespaceid\17\sdkrevision\3\id\1\final\
        '''
        
    def handle_newuser(self, data):
        print("NEWUSER ", data)
        if not (5 < len(data.get('nick', '')) < 24 and
                50 > len(data.get('email', '')) > 2 and
                24 > len(data.get('passwordenc', '')) > 7):
            self.error(0, 'fatal', 'Error creating account, check length!')
            return

        if not self._valid_nickname_regexp.match(data['nick']):
            self.error(0, 'fatal', 'Error creating account, invalid name!')
            return

        if data['nick'] in self.server.user_db:
            self.error(516, 'fatal', 'Account name already in use!')
            return

        pwhash = gs_enc2.gsPWDecHash(data['passwordenc'])
        user = self.server.user_db.create(data['nick'], pwhash, data['email'], '', self.host)
        self.respond('nur', '', 'userid', 2000000 + user.id, 'profileid', 1000000 + user.id, 'id', 1)

        '''\newuser\\email\qqq@qq\nick\borf-tk\passwordenc\J8DHxh7t\
            productid\11081\gamename\civ4bts\namespaceid\17\uniquenick\borf-tk\
            partnerid\0\id\1\final\
        '''
        
    def handle_getprofile(self, data):
        pass
        # Related to buddy-system

    def handle_status(self, data):
        if 'logout' in data:
            self.disconnect('status logout')

    def handle_logout(self, data):
        self.disconnect('logout')

    def _parse_packet(self, packet):
        words = packet.split('\\')
        if len(words) < 3 or words[0] != '':
            logging.warning('Parsing strange packet: {}', packet)
        command = words[1]
        words = words[1:]
        cooked = [(words[i], words[i + 1]) for i in range(0, len(words) - 1, 2)]
        data = dict(cooked)
        logging.debug('Receiving command %s, data: %s', command, data)
        data['command'] = command # for debug purposes
        if command in self.handlers:
            self.handlers[command](data)
        else:
            logging.warning('No handler for command: %s', command)

    def _parse_read_buffer(self, read_buffer):
        # We assume all packets and with \final\ - but never have that inbetween
        packets = read_buffer.split('\\final\\')
        # Put last word (maybe empty) back into the readbuffer as we don't know if it is complete yet.
        remainder = packets[-1]
        packets = packets[:-1]
        # Now the packets array should contain complete packets and the readbuffer any remaining incomplete ones
        for packet in packets:
            self._parse_packet(packet)
        return remainder

    def respond(self, words):
        msg = '\\'
        for word in words:
            msg += str(word)
            msg += '\\'
        msg += 'final\\'
        self.write(msg)

    def error(self, err, severity, errmsg):
        self.respond(['error', '', 'err', err, severity, '', 'errmsg', errmsg, 'id', 1])


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

    def create(self, name, password, email, country, lastip):
        self.dbcur.execute("INSERT INTO users (name, password, email, country, lastip) VALUES (?, ?, ?, ?, ?);",
                           (name, password, email, country, lastip))
        return UserObj(self, self.dbcur.lastrowid)
    

class LoginServer(NetworkServer):
    def __init__(self):
        super().__init__()

        gp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gp_socket.setblocking(0)
        try:
            gp_socket.bind(("", 29900))
        except socket.error as err:
            print('Bind failed for gp (29900 TCP): {}'.format(err))
            raise err
        gp_socket.listen(5)
        self.register_server(gp_socket, GPClient)

        gps_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gps_socket.setblocking(0)
        try:
            gps_socket.bind(("", 29901))
        except socket.error as err:
            print('Bind failed for gps (29901 TCP): {}'.format(err))
            raise err
        self.gps.listen(5)
        self.register_server(gps_socket, GPSClient)


logging.basicConfig(format='%(asctime)s %(message)s')
server = LoginServer()
try:
    server.run()
except KeyboardInterrupt:
    print("LoginServer interrupted.")
