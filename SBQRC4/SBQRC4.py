#! /usr/bin/env python2
# Based on code copied or translated from works: miniircd,dwc_network_server_emulator, GsOpenSDK, ALuigi's projects, possibly other sources
#
import socket
import select
import time
import random

import argparse

import enc
from gs_consts import *
from gs_utils import *


class GameHost:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sessionid = '\x00\x00\x00\x00'
        self.lastheard = time.time()
        self.data = {}

    def refresh(self):
        self.lastheard = time.time()


class SBClient:
    def __init__(self, server, sock):
        self.server = server
        self.socket = sock
        self.out_crypt = None
        (self.host, self.port) = sock.getpeername()
        self.__timestamp = time.time()
        self.__readbuffer = ""
        self.__writebuffer = ""
        self.__sent_ping = False

    def write_queue_size(self):
        return len(self.__writebuffer)

    def sb_00respgen(self, fields):
        #keysheader
        r = ''
        for x in self.host.split('.'):
            r += chr(int(x))
        r += chr(self.port / 256)
        r += chr(self.port % 256)
        r += chr(len(fields))
        for field in fields:
            r += '\x00' + field + '\x00'
        r += '\x00'
        #list of hosts
        for key, host in self.server.hosts.items():
            if host.lastheard + 360 < time.time():  #deleting old servers here so we dont need a timer for that
                del self.server.hosts[key]
                #print "deleting old gamehost"
            else:
                flags = 0
                flags_buffer = ''
                #setting flags - this part has potential to be improved
                if len(host.data) != 0:
                    flags |= UNSOLICITED_UDP_FLAG
                    flags |= HAS_KEYS_FLAG
                    if "natneg" in host.data:
                        flags |= CONNECT_NEGOTIATE_FLAG
                    flags |= NONSTANDARD_PORT_FLAG
                    flags |= PRIVATE_IP_FLAG  #?
                    flags |= NONSTANDARD_PRIVATE_PORT_FLAG  #?
                #adding ?public? ip, port
                for x in host.ip.split('.'):
                    flags_buffer += chr(int(x))
                flags_buffer += chr(host.port / 256)
                flags_buffer += chr(host.port % 256)
                #adding 1 of local ip's :localport
                #for now server sends a random localip from all supplied
                lips = []
                for key1, value1 in host.data.items():
                    if key1.startswith('localip') == True:
                        lips.append(value1)
                for x1 in lips[random.randrange(0, len(lips))].split('.'):  #value.data['localip0'].split('.'):
                    flags_buffer += chr(int(x1))
                localport = int(host.data.get('localport', 6500))
                flags_buffer += chr(localport / 256)
                flags_buffer += chr(localport % 256)
                r += chr(flags)
                r += flags_buffer
                #adding fields
                if len(host.data) != 0:
                    for field in fields:
                        r += '\xff' + str(host.data.get(field, '0')) + '\x00'
        #ending symbols        
        r += '\x00'
        r += '\xff' * 4
        return r

    def __parse_read_buffer(self):
        try:
            while len(self.__readbuffer) > 0:
                cplen = ord(self.__readbuffer[0]) * 256 + ord(self.__readbuffer[1])
                packet = None
                if len(self.__readbuffer) >= cplen:
                    packet = self.__readbuffer[:cplen]
                    self.__readbuffer = self.__readbuffer[cplen:]
                if packet == None:
                    break  #not full packet
                if packet[2] == '\x00':  #List request
                    if len(packet) > 25:
                        idx = 9
                        query_game = get_string(packet, idx)
                        idx += len(query_game) + 1
                        game_name = get_string(packet, idx)
                        idx += len(query_game) + 1
                        cchallenge = ''.join(packet[idx:idx + 8])
                        idx += 8
                        f = get_string(packet, idx)
                        idx += len(f) + 1
                        fields = get_string(packet, idx)
                        if '\\' in fields:
                            fields = [x for x in fields.split('\\') if x and not x.isspace()]
                        self.message(enc.SBpreCryptHeader())
                        self.out_crypt = enc.GOACryptState()
                        qfromkey = gngk.get(query_game, 'Cs2iIq')
                        self.out_crypt.SBCryptStart(bytearray(qfromkey), bytearray(cchallenge),
                                                   bytearray(enc.SCHALLCONST))
                        self.message(self.sb_00respgen(fields))

                elif packet[2] == '\x02':  #forward req
                    print("forward request")
                    self.server.qr_forw_to(packet)

                elif packet[2] == '\x03':  #ping response
                    print("ping ack")

                else:
                    print("SB recieved unknown command {}".format(ord(packet[2])))
        except Exception, err:
            print(err)

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
            # FIXME: this seems to be a blocking send... not so nice :-(
            sent = self.socket.send(self.__writebuffer[:1024])
            self.__writebuffer = self.__writebuffer[sent:]
        except socket.error as err:
            self.disconnect(err)

    def disconnect(self, quitmsg):
        print('client disconnected ({}:{}): {}', self.host, self.port, quitmsg)
        self.socket.close()
        self.server.remove_client(self, quitmsg)

    def message(self, msg):
        if self.out_crypt is not None:
            msg = self.out_crypt.GOAEncrypt(bytearray(msg))
        self.__writebuffer += msg

    def check_aliveness(self):
        now = time.time()
        if self.__timestamp + 180 < now:
            self.disconnect("ping timeout")
            return
        if not self.__sent_ping and self.__timestamp + 80 < now:
            pingstr = '\x00\x07\x03\x77\x77\x77\x77'
            self.message(pingstr)
            self.__sent_ping = True


class SBQRServer:
    def __init__(self):
        self.clients = {}  # Socket --> Client instance
        self.hosts = {}  # key = ip:port; value = other stuff

    def addfakehost(self, hostname, mapname, nump, maxp, new):
        addr = ('.'.join(str(random.randrange(0, 256)) for _ in range(4)), 6500)
        self.hosts[addr] = GameHost(*addr)
        zz1 = """\x03\x79\x91\x42\x05\x6C\x6F\x63\x61\x6C\x69\x70\x30\x00\x31\x30\x39\x2E\x32\x30\x30\x2E\x31\x34\x37\x2E\x32\x00\x6C\x6F\x63\x61\x6C\x69\x70\x31\x00\x31\x30\x2E\x32\x34\x30\x2E\x31\x32\x2E\x32\x32\x00\x6C\x6F\x63\x61\x6C\x69\x70\x32\x00\x31\x39\x32\x2E\x31\x36\x38\x2E\x31\x33\x37\x2E\x31\x00\x6C\x6F\x63\x61\x6C\x70\x6F\x72\x74\x00\x36\x35\x30\x30\x00\x6E\x61\x74\x6E\x65\x67\x00\x31\x00\x73\x74\x61\x74\x65\x63\x68\x61\x6E\x67\x65\x64\x00\x33\x00\x67\x61\x6D\x65\x6E\x61\x6D\x65\x00\x63\x69\x76\x34\x00\x70\x75\x62\x6C\x69\x63\x69\x70\x00\x30\x00\x70\x75\x62\x6C\x69\x63\x70\x6F\x72\x74\x00\x30\x00\x68\x6F\x73\x74\x6E\x61\x6D\x65\x00\x74\x65\x61\x6D\x65\x72\x78\x70\x00\x67\x61\x6D\x65\x6D\x6F\x64\x65\x00\x6F\x70\x65\x6E\x73\x74\x61\x67\x69\x6E\x67\x00\x6E\x75\x6D\x70\x6C\x61\x79\x65\x72\x73\x00\x31\x00\x6D\x61\x78\x70\x6C\x61\x79\x65\x72\x73\x00\x33\x32\x00\x68\x6F\x73\x74\x6E\x61\x6D\x65\x00\x74\x65\x61\x6D\x65\x72\x78\x70\x00\x67\x61\x6D\x65\x76\x65\x72\x00\x30\x00\x70\x61\x73\x73\x77\x64\x00\x30\x00\x68\x6F\x73\x74\x70\x6F\x72\x74\x00\x32\x30\x35\x36\x00\x73\x74\x61\x67\x69\x6E\x67\x00\x31\x00\x6E\x65\x77\x67\x61\x6D\x65\x00\x31\x00\x6D\x61\x70\x6E\x61\x6D\x65\x00\x42\x61\x6C\x61\x6E\x63\x65\x64\x00\x67\x61\x6D\x65\x74\x79\x70\x65\x00\x00\x6D\x79\x6E\x75\x6D\x70\x6C\x61\x79\x65\x72\x73\x00\x31\x00\x6D\x61\x78\x6E\x75\x6D\x70\x6C\x61\x79\x65\x72\x73\x00\x33\x00\x6E\x75\x6D\x6D\x69\x73\x73\x69\x6E\x67\x00\x32\x00\x70\x69\x74\x62\x6F\x73\x73\x00\x30\x00\x00\x00\x01\x70\x6C\x61\x79\x65\x72\x5F\x00\x70\x69\x6E\x67\x5F\x00\x70\x69\x6E\x67\x5F\x00\x00\x64\x69\x6E\x67\x75\x73\x32\x32\x31\x2D\x74\x6B\x00\x30\x00\x30\x00\x00\x00\x00"""
        self.hosts[addr].data = SBQRServer.qr_parse03(zz1)
        self.hosts[addr].data['hostname'] = hostname
        self.hosts[addr].data['mapname'] = mapname
        self.hosts[addr].data['mynumplayers'] = nump
        self.hosts[addr].data['maxnumplayers'] = maxp
        self.hosts[addr].data['nummissing'] = maxp - nump
        self.hosts[addr].data['newgame'] = new

    def print_hostlist(self):
        for index, host in enumerate(self.hosts.keys()):
            print('[{}] {}:{} ({}) {}'.format(index, host.ip, host.port, host.sessionid, host.lastheard))
            print(host.data)
            print('--------')

    def qr_forw_to(self, rawdata):
        if rawdata[9:15] == '\xfd\xfc\x1e\x66\x6a\xb2':
            ip = str(ord(rawdata[3])) + '.' + str(ord(rawdata[4])) + '.' + str(ord(rawdata[5])) + '.'\
               + str(ord(rawdata[6]))
            port = ord(rawdata[7]) * 256 + ord(rawdata[8])
            if (ip, port) in self.hosts:
                print('forwarding to existing host')
            else:
                print('forwarding to unknown address')
            resp = '\xfe\xfd\x06'
            if (ip, port) in self.hosts:
                resp += self.hosts[(ip, port)].sessionid
            else:
                resp += '\x00' * 4
            resp += ''.join(chr(random.randrange(0, 256)) for _ in range(4))  #random cookie here
            resp += rawdata[9:]
            self.qr_send_to(resp, (ip, port), 'qrforwto')
        else:
            print('wrong data to forward')

    @staticmethod
    def qr_parse03(raw):
        prepared = raw[5:].split('\x00\x00\x00\x01')[0].split('\x00')
        cooked = [(prepared[i], prepared[i + 1]) for i in range(0, len(prepared), 2)]
        return dict(cooked)

    def qr_send_to(self, resp, address, location):
        #sending from qr, with error handliing
        try:
            self.qr_socket.sendto(resp, address)
        except socket.error, x:
            print
            str(location) + str(x)

    def process_qr(self, recv_data, address):
        print('handle qr')
        if recv_data[0] == '\x09' and len(recv_data) >= 5:  #09,4xUid,'civ4bts','0'  - game checks if qr is up
            resp = '\xfe\xfd\x09' + recv_data[1:5] + '\x00'
            self.qr_send_to(resp, address, '09')
        elif recv_data[0] == '\x08' and len(recv_data) >= 5:  #08 4xuid - ping
            resp = '\xfe\xfd\x08' + recv_data[1:5]
            self.qr_send_to(resp, address, '08')
        elif recv_data[0] == '\x07' and len(recv_data) >= 5:  #06 ACK - no response
            hexprint(recv_data)
        elif recv_data[0] == '\x01' and len(recv_data) >= 5:  #resp to our challenge
            resp = '\xfe\xfd\x0a' + recv_data[1:5]
            self.qr_send_to(resp, address, '01')
        elif recv_data[0] == '\x03' and len(recv_data) >= 5:
            print('03')
            parsed = SBQRServer.qr_parse03(recv_data)
            if parsed.get('statechanged', 0) == '3':
                if address in self.hosts:
                    del self.hosts[address]
                self.hosts[address] = GameHost(*address)
                self.hosts[address].sessionid = recv_data[1:5]
                self.hosts[address].data = parsed
                resp = '\xfe\xfd\x01' + recv_data[1:5] + ghchal
                self.qr_send_to(resp, address, '03-3')
                self.sb_sendpush02(self.hosts[address])
            elif parsed.get('statechanged', 0) == '2':
                if address in self.hosts:
                    self.sb_senddel04(address)
                    del self.hosts[address]
            elif parsed.get('statechanged', 0) == '1':
                if address in self.hosts:
                    self.hosts[address].data = parsed
                    self.hosts[address].refresh()
                    self.sb_sendpush02(self.hosts[address])
            elif parsed.get('statechanged', 0) == 0:
                if address in self.hosts:
                    self.hosts[address].refresh()

    def sb_sendpush02(self, host):
        msg = '\x02'
        flags = 0
        flags_buffer = ''
        if len(host.data) != 0:
            flags |= UNSOLICITED_UDP_FLAG
            flags |= HAS_KEYS_FLAG
            if "natneg" in host.data:
                flags |= CONNECT_NEGOTIATE_FLAG
                flags |= NONSTANDARD_PORT_FLAG
                flags |= PRIVATE_IP_FLAG  #?
                flags |= NONSTANDARD_PRIVATE_PORT_FLAG  #?
        msg += chr(flags)
        for x in host.ip.split('.'):
            flags_buffer += chr(int(x))
        flags_buffer += chr(host.port / 256)
        flags_buffer += chr(host.port % 256)
        localips = []
        for key1, value1 in host.data.items():
            if key1.startswith('localip'):
                localips.append(value1)
        if len(localips) == 1:
            localip = localips[0]
            print("sb_sendpush02, single localip: {}".format(localip))
        elif not localips:
            print("WARNING: sb_sendpush02: Missing localips, using fake")
            localip = '127.0.0.1'
        else:
            localip = random.choice(localips)
            print("WARNING: sb_sendpush02: Multiple localips: {}, using random: {}".format(localips, localip))
        for x1 in localip.split('.'):
            flags_buffer += chr(int(x1))
        port = int(host.data.get('localport', 6500))
        flags_buffer += chr(port / 256)
        flags_buffer += chr(port % 256)
        msg += flags_buffer
        for field in defaultfields:
            msg += host.data[field] + '\x00'
        msg += '\x01'
        l = ''.join([chr(i) for i in divmod(len(msg) + 2, 256)])  # length of the msg stored in 2 bytes
        msg = l + msg
        # iterate through SBClients and make a message for each
        for key in self.clients:
            self.clients[key].message(msg)

    def sb_senddel04(self, address):
        msg = '\x00\x09\x04'
        for x in address[0].split('.'):
            msg += chr(int(x))
        msg += chr(address[1] / 256)
        msg += chr(address[1] % 256)
        #iterate through SBClients and make a message for each
        for key in self.clients:
            self.clients[key].message(msg)

    def remove_client(self, client, quitmsg):  #cant delete clients inside their own functions?
        del self.clients[client.socket]

    def run(self):
        #Starting qr socket
        self.qr_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.qr_socket.bind(("0.0.0.0", 27900))
        except socket.error as msg:
            print('Bind failed for qr. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        self.qr_socket.setblocking(0)
        #starting sb socket
        self.sb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sb_socket.bind(("0.0.0.0", 28910))
        except socket.error as msg:
            print('Bind failed for sb. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        self.sb_socket.listen(5)
        last_aliveness_check = time.time()
        #socket processing loop
        while True:
            (rlst, wlst, _) = select.select(
                [self.qr_socket, self.sb_socket] + [x.socket for x in self.clients.values()],
                [x.socket for x in self.clients.values() if x.write_queue_size() > 0],
                [], 15)
            for x in rlst:
                if x == self.qr_socket:
                    try:
                        recv_data, addr = self.qr_socket.recvfrom(1024)
                        if len(recv_data) > 0:
                            self.process_qr(recv_data, addr)
                    except socket.error as err:
                        print(err)
                elif x in self.clients:
                    self.clients[x].socket_readable_notification()
                else:
                    (conn, addr) = x.accept()
                    self.clients[conn] = SBClient(self, conn)
                    print('accepted sb connection from %s:%s.' % (addr[0], addr[1]))
            for x in wlst:
                if x in self.clients:  # client may have been disconnected
                    self.clients[x].socket_writable_notification()
            now = time.time()
            if last_aliveness_check + 10 < now:
                for client in self.clients.values():
                    client.check_aliveness()
                last_aliveness_check = now


def main():
    parser = argparse.ArgumentParser(description='Partial GameSpy server emulator.')
    parser.add_argument('--fakehosts', dest='fakehosts', action='store_true', help='Add fake hosts for testing.')

    args = parser.parse_args()
    server = SBQRServer()

    if args.fakehosts:
        for _ in range(0, 10):
            name = ' '.join([random.choice(fakenames['tags']) for _ in range(0, random.randrange(0, 3))] +
                            [random.choice(fakenames['types'])] +
                            [random.choice(fakenames['tags']) for _ in range(0, random.randrange(0, 3))])
            mapname = random.choice(fakenames['maps'])
            max_players = random.randrange(2, 220)
            num_players = random.randrange(1, max_players)
            is_new = random.choice([True, False])
            server.addfakehost(name, mapname, num_players, max_players, is_new)

    try:
        server.run()
    except KeyboardInterrupt:
        print("Interrupted. Stopping")


main()

