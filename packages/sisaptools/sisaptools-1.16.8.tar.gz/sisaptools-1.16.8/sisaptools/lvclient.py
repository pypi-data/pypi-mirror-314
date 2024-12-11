# Versio 1.1.0
import socket
import json
import hashlib
import zlib

import logging


class LvClient:
    FI_TRANSMISSIO = b"[[FI_DE_TRANSMISSIO]]"
    FI_TRANSMISSIO_LEN = len(FI_TRANSMISSIO)
    PACKET_LEN = 8192
    TIMEOUT = 300  # 120
    INTENTS = 10

    def __init__(self, user="ffina", pwd="Ui34!9hd", host="10.52.137.134", port=50002):  # noqa
        if not user:
            raise Exception("Usuari obligatori")
        if not pwd:
            raise Exception("Contrasenya obligatoria")
        if not host:
            raise Exception("Host obligatori")
        if not port:
            raise Exception("Port obligatori")
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = port

    def receive(self):
        data = b''
        while True:
            data += self.socket.recv(self.PACKET_LEN)
            ultims = data[-self.FI_TRANSMISSIO_LEN:]
            if ultims == self.FI_TRANSMISSIO:
                data = data[:-self.FI_TRANSMISSIO_LEN]
                break
        uncompressed = zlib.decompress(data)
        str = uncompressed.decode('utf-8')
        return str

    def send(self, mystr):
        data = str.encode(mystr)  # Passem a byte
        compressed_data = zlib.compress(data, 1)  # compresio rapida
        compressed_data += self.FI_TRANSMISSIO  # afegim tancament missatge
        self.socket.sendall(compressed_data)

    def open_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def close(self):
        pass

    def close_socket(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:  # noqa
            pass

        try:
            self.socket.close()
        except Exception as e:  # noqa
            pass

    def hash_pwd(self):
        h = hashlib.sha1()
        h.update(self.pwd.encode())
        return h.hexdigest()

    def set_timeout(self):
        self.socket.settimeout(self.TIMEOUT)

    def query(self, str):
        msg = {
            'user': self.user,
            'pwd': self.hash_pwd(),
            'operation': 'query',
            'data': str
        }

        intent = 0
        rebut = False
        while not rebut and intent <= self.INTENTS:
            try:
                intent += 1
                self.open_socket()
                self.set_timeout()
                self.send(json.dumps(msg))
                self.set_timeout()
                response = self.receive()
                rebut = True
            except socket.timeout as e:  # noqa
                logging.error("lvclient: TIMEOUT REINTENT!!!!!!!!!!!")
            except Exception as e:  # noqa
                logging.exception("lvclient: EXCEPTION:")
            finally:
                self.close_socket()

        if not rebut:
            raise Exception("lvclient: ERROR Timeout")

        res = json.loads(response)

        if 'error' in res:
            raise Exception(res['error'])

        data = res['data'][:-1]
        for row in data.split("\n"):
            yield row.split("{")
