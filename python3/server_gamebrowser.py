#! /usr/bin/env python2
# Based on code copied or translated from works: miniircd,dwc_network_server_emulator, GsOpenSDK, ALuigi's projects, possibly other sources
#
import socket
import select
import time
import random
import argparse
import logging

import byteencode
import enc
from gs_consts import *
from gs_utils import *
from gs_network import NetworkClient, NetworkServer


class GameHost:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sessionid = '\x00\x00\x00\x00'
        self.lastheard = time.time()
        self.data = {}

    def refresh(self):
        self.lastheard = time.time()

    def __str__(self):
        return '{}:{}'.format(self.ip, self.port)


class SBClient(NetworkClient):
    def __init__(self, server, sock):
        super().__init__(server, sock)
        self.out_crypt = None
        self._timestamp = time.time()
        self._sent_ping = False

    def sb_00respgen(self, fields):
        #keysheader
        r = ''
        r += byteencode.ipaddr(self.host)
        r += byteencode.uint16(self.port)
        r += byteencode.uint8(len(fields))
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
                flags_buffer += byteencode.ipaddr(host.ip)
                flags_buffer += byteencode.uint16(host.port)
                #adding 1 of local ip's :localport
                #for now server sends a random localip from all supplied
                lips = []
                for key1, value1 in host.data.items():
                    if key1.startswith('localip') == True:
                        lips.append(value1)
                for x1 in lips[random.randrange(0, len(lips))].split('.'):  #value.data['localip0'].split('.'):
                    flags_buffer += chr(int(x1))
                flags_buffer += byteencode.uint16(host.data.get('localport', 6500))
                r += byteencode.uint8(flags)
                r += flags_buffer
                #adding fields
                if len(host.data) != 0:
                    for field in fields:
                        r += '\xff' + str(host.data.get(field, '0')) + '\x00'
        #ending symbols        
        r += '\x00'
        r += '\xff' * 4
        return r

    def _parse_packet(self, packet):
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
                self.write(enc.SBpreCryptHeader())
                self.out_crypt = enc.GOACryptState()
                qfromkey = gngk.get(query_game, 'Cs2iIq')
                self.out_crypt.SBCryptStart(bytearray(qfromkey), bytearray(cchallenge),
                                           bytearray(enc.SCHALLCONST))
                self.write(self.sb_00respgen(fields))
        elif packet[2] == '\x02':  #forward req
            self.info("forward request")
            self.server.qr_forw_to(packet)
        elif packet[2] == '\x03':  #ping response
            self.info("ping ack")
        else:
            self.info("SB recieved unknown command: %d", ord(packet[2]))

    def _parse_read_buffer(self, read_buffer):
        self._timestamp = time.time()
        self._sent_ping = False
        # We need at least two bytes to identify the packet length
        while len(read_buffer) >= 2:
            cplen = ord(read_buffer[0]) * 256 + ord(read_buffer[1])
            if len(read_buffer) >= cplen:
                packet = read_buffer[:cplen]
                read_buffer = read_buffer[cplen:]
                self._parse_packet(packet)
            else:
                break  # not a full packet
        return read_buffer

    def check_aliveness(self):
        now = time.time()
        if self._timestamp + 180 < now:
            self.disconnect('ping timeout')
            return
        if not self._sent_ping and self._timestamp + 80 < now:
            pingstr = '\x00\x07\x03\x77\x77\x77\x77'
            self.write(pingstr)
            self._sent_ping = True

    def write(self, msg):
        if self.out_crypt is not None:
            msg = self.out_crypt.GOAEncrypt(bytearray(msg))
        super().write(msg)


class SBQRServer(NetworkServer):
    def __init__(self):
        super().__init__()
        self.hosts = {}  # key = ip:port; value = other stuff
        self.qr_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.qr_socket.bind(("", 27900))
        except socket.error as err:
            logging.error('Bind failed for qr socket (UDP 27900): %s', err)
        self.qr_socket.setblocking(0)
        # We dont use register_server here, this is a special UDP handler that doesn't accept / create clients etc.
        self._server_socket_handlers[self.qr_socket] = self.handle_qr

        self.sb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sb_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sb_socket.bind(("", 28910))
            self.sb_socket.listen(5)
            self.sb_socket.setblocking(0)
        except socket.error as err:
            logging.error('Bind/listen failed for sb socket (TCP 28910): %s', err)
        self.register_server(self.sb_socket, SBClient)

        self.last_aliveness_check = time.time()

    def print_hostlist(self):
        print("Prining hostlist of server...")
        for index, (_, host) in enumerate(self.hosts.items()):
            print('[{}] {}:{} ({}) {}'.format(index, host.ip, host.port, host.sessionid, host.lastheard))
            print(host.data)
            print('--------')

    def qr_forw_to(self, rawdata):
        if rawdata[9:15] == '\xfd\xfc\x1e\x66\x6a\xb2':
            ip = str(ord(rawdata[3])) + '.' + str(ord(rawdata[4])) + '.' + str(ord(rawdata[5])) + '.'\
               + str(ord(rawdata[6]))
            port = ord(rawdata[7]) * 256 + ord(rawdata[8])
            if (ip, port) in self.hosts:
                logging.info('forwarding to existing host')
            else:
                logging.info('forwarding to unknown address')
            resp = '\xfe\xfd\x06'
            if (ip, port) in self.hosts:
                resp += self.hosts[(ip, port)].sessionid
            else:
                resp += '\x00' * 4
            resp += ''.join(chr(random.randrange(0, 256)) for _ in range(4))  #random cookie here
            resp += rawdata[9:]
            self.qr_send_to(resp, (ip, port), 'qrforwto')
        else:
            logging.warning('wrong data to forward')

    @staticmethod
    def qr_parse03(raw):
        prepared = raw[5:].split('\x00\x00\x00')[0].split('\x00')
        if len(prepared) % 2 == 1:
            logging.warning("Could not correctly parse03: %s", prepared)
        cooked = [(prepared[i], prepared[i + 1]) for i in range(0, len(prepared) - 1, 2)]
        return dict(cooked)

    def qr_send_to(self, resp, address, location):
        try:
            self.qr_socket.sendto(resp, address)
        except socket.error as err:
            logging.error('Socket error on location %s: %s', location, err)

    def handle_qr(self):
        recv_data, addr = self.qr_socket.recvfrom(1024)
        if len(recv_data) > 0:
            self.process_qr(recv_data, addr)

    def process_qr(self, recv_data, address):
        logging.debug('process_qr address: %s', address)
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
        msg += byteencode.uint8(flags)
        flags_buffer += byteencode.ipaddr(host.ip)
        flags_buffer += byteencode.uint16(host.port)
        localips = []
        for key1, value1 in host.data.items():
            if key1.startswith('localip'):
                localips.append(value1)
        if len(localips) == 1:
            localip = localips[0]
            logging.info('sb_sendpush02, single localip: %s', localip)
        elif not localips:
            logging.warning('sb_sendpush02: Missing localips, using fake')
            localip = '127.0.0.1'
        else:
            localip = random.choice(localips)
            logging.info('sb_sendpush02: Multiple localips: %s, using random one: %s', localips, localip)
        flags_buffer += byteencode.ipaddr(localip)
        flags_buffer += byteencode.uint16(host.data.get('localport', 6500))
        msg += flags_buffer
        for field in defaultfields:
            msg += host.data[field] + '\x00'
        msg += '\x01'
        l = byteencode.uint16(len(msg) + 2)
        msg = l + msg
        # iterate through SBClients and make a message for each
        logging.info('Sending info about host %s to %d clients', host, len(self.clients))
        for client in self.clients.values():
            client.write(msg)

    def sb_senddel04(self, address):
        msg = '\x00\x09\x04'
        msg += byteencode.ipaddr(address[0])
        msg += byteencode.uint16(address[1])
        for key in self.clients:
            self.clients[key].write(msg)

    def run(self):
        print('Server ready, waiting for connections.')
        while True:
            self.select()
            now = time.time()
            if last_aliveness_check + 10 < now:
                for client in self.clients.values():
                    client.check_aliveness()
                last_aliveness_check = now


logging.basicConfig(format='%(asctime)s %(message)s')
server = SBQRServer()
try:
    server.run()
except KeyboardInterrupt:
    print('Interrupted. Stopping')
