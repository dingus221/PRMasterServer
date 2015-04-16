import socket
import select
import logging
import errno


class NetworkClient(object):
    def __init__(self, server, sock):
        self.server = server
        self.socket = sock
        (self.host, self.port) = sock.getpeername()
        self._read_buffer = ''
        self._write_buffer = ''

    def __str__(self):
        return '{}@{}:{}'.format(self.__class__.__name__, self.host, self.port)

    def write_queue_size(self):
        return len(self._write_buffer)

    def socket_readable_notification(self):
        try:
            data = self.socket.recv(2 ** 10)
            if not data:
                self.disconnect('EOT')
            self._read_buffer += data
            try:
                self._read_buffer = self._parse_read_buffer(self._read_buffer)
            except Exception as err:
                logging.error('[%s] Exception during parse_read_buffer: %s', self, err)
                # Reset buffer to avoid another exception
                # Maybe we should disconnect here?
                self._read_buffer = ''
        except socket.error as err:
            if err.args[0] == errno.EAGAIN or err.args[0] == errno.EWOULDBLOCK:
                logging.warning('[%s] Nonblocking read failed, will retry: %s', self, err)
            else:
                logging.warning('[%s] Nonblocking read failed hard, disconnect: %s', self, err)
                self.disconnect(err)

    def socket_writable_notification(self):
        logging.debug('flusing writebuffer (%d bytes) of client %s', len(self._write_buffer), self)
        if not self._write_buffer:
            return
        try:
            sent = self.socket.send(self._write_buffer[:1024])
            self._write_buffer = self._write_buffer[sent:]
        except socket.error as err:
            if err.args[0] == errno.EAGAIN or err.args[0] == errno.EWOULDBLOCK:
                logging.warning('[%s] Nonblocking send failed, will retry: %s', self, err)
            else:
                logging.warning('[%s] Nonblocking send failed hard, disconnect: %s', self, err)
                self.disconnect(err)

    def disconnect(self, quitmsg):
        logging.info('[%s] client disconnected: %s', self, quitmsg)
        self.socket.close()
        self.server.remove_client(self, quitmsg)

    def write(self, msg):
        logging.debug('[%s] adding message with length %d to writebuffer.', self, len(msg))
        self.__writebuffer += msg


class NetworkServer(object):
    def __init__(self):
        self._clients_by_socket = {}
        self._server_socket_handlers = {}

    def register_client(self, sock, client):
        self._clients_by_socket[sock] = client

    def unregister_client(self, sock, client):
        del self._clients_by_socket[sock]

    def register_server(self, server_socket, client_class):
        def handler():
            (client_sock, addr) = server_socket.accept()
            client = client_class(self, client_sock)
            self.register_client(client_sock, client)
            logging.info('Accepted connection from %d:%d, spawning new %s',
                         addr[0], addr[1], client_class.__name__)
        self._server_socket_handlers[server_socket] = handler

    def select(self, timeout=10):
        (rlst, wlst, xlst) = select.select(
            list(self._server_socket_handlers.keys()) + list(self._clients_by_socket.keys()),
            [sock for (sock, client) in self._clients_by_socket.items() if client.write_queue_size() > 0],
            [],
            timeout)
        for rsock in rlst:
            if rsock in self._clients_by_socket:
                self._clients_by_socket[rsock].socket_readable_notification()
            elif rsock in self._server_socket_handlers:
                try:
                    self._server_socket_handlers[rsock]()
                except Exception as err:
                    logging.error('Exception occured during client creation: %s', err)
            else:
                logging.error('Invalid rlist socket from select')

        for wsock in wlst:
            try:
                self._clients_by_socket[wsock].socket_writable_notification()
            except Exception as err:
                logging.error('Exception occured during writable_notification: %s', err)

    def run(self):
        print('Server ready, waiting for connections.')
        while True:
            self.select()
