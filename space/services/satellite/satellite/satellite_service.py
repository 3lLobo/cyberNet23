#!/usr/bin/env python3

import _thread
import base64
import json
import logging
import os
import socketserver
import socket
import subprocess
import sys
import threading
import traceback
from datetime import datetime
from time import sleep
import re
import paramiko

logging.basicConfig(level=logging.INFO,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        handlers=[logging.StreamHandler(sys.stdout), ])
logger = logging.getLogger(__file__)


data_path = '/data'


# Commands
class Command:
    def __init__(*args, **kwargs):
        pass

class GetSatelliteImage(Command):
    filename = None
    def __init__(self, argument):
        self.filename = argument

    def process(self, server, channel):
        if not os.path.exists(self.filename):
            logger.error(f"Error! File {self.filename} does not exist!")
            server.send(f"Error! File {self.filename} does not exist!")
            return

        with open(f'{self.filename}', "rb") as f:
            server.send(channel, base64.b64encode(f.read()))

class Satellites(Command):
    def __init__(self, argument):
        match = re.search("^[a-zA-Z0-9-_+.*]*$", argument)
        if match:
            self.query = match.group()
        else:
            self.query = "*"

    def process(self, server, channel):
        result = subprocess.check_output(f"ls -d {self.query} | grep -v user.json; exit 0", shell=True, stderr=subprocess.STDOUT)
        server.send(channel, result)

class Timestamp(Command):
    def __init__(self, argument):
        self.filename = argument
    
    def process(self, server, channel):
        server.send(channel, f"{datetime.utcfromtimestamp(os.path.getmtime(self.filename)).isoformat()}")

class LatestFilename(Command):
    def __init__(self, argument):
        self.sat_name = argument

    def process(self, server, channel):
        filename = os.listdir(f'{data_path}/{self.sat_name}')[0]
        server.send(channel, f'{filename}\n')

commands = {
    'satellites': Satellites,
    'timestamp': Timestamp,
    'latest_filename': LatestFilename,
    'get_satellite_image': GetSatelliteImage,
}


host_key = paramiko.RSAKey(filename="satellite_rsa.key")
port = 2222


class Server(paramiko.ServerInterface):
    channel = None
    username = None
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        ssh_users = json.load(open(f'{data_path}/user.json', 'r'))
        if password == ssh_users.get(username, ''):
            self.username = username

            try:
                if self.username == 'status':
                    os.chdir(f'{data_path}/')
                else:
                    os.chdir(f'{data_path}/{username}')
            except Exception:
                return paramiko.AUTH_FAILED
            
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_shell_request(self, channel):
        logger.info("Got shell request")
        self.event.set()
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True
    
    def check_channel_exec_request(self, channel, command):
        match = re.search("^[a-zA-Z0-9_+.]*$", command)
        if not match:
            command = "*"

        try:
            channel.send(subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout)
        except Exception as err:
            channel.send('An error occurred: {}\r\n'.format(err))
        finally:
            self.event.set()
        return True

    def send(self, channel, data):
        if isinstance(data, str):
            return channel.sendall(data + '🛰️🛑\n')
        return channel.sendall(data + '🛰️🛑\n'.encode('utf-8'))
    
    def receive(self, channel):
        r = b''
        while not '🛰️🛑\n'.encode('utf-8') in r:
            data = channel.recv(1024)
            if not data:
                break
            r += data
        return r.replace('🛰️🛑\n'.encode('utf-8'), b'').decode()

class SSHHandler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            trans = paramiko.Transport(self.connection)
            trans.load_server_moduli()
            trans.add_server_key(host_key)
            server = Server()
            trans.start_server(server=server)

            # wait for auth
            chan = trans.accept(20)
            if chan is None:
                trans.close()
                return
            
            logger.info(f"[{self.client_address}] Client Authenticated as '{server.username}'")

            server.event.wait(10)

            if not server.event.is_set():
                logger.info(f'[{self.client_address}] Client never asked for a command execution')
                trans.close()
                return
 
            logger.info(f'[{self.client_address}] Communicating...')
            server.send(chan, "Welcome")
            while True:
                logger.info(f"Status {trans.is_active()}")
                input = server.receive(chan)

                if not input:
                    trans.close()
                    return

                if 'quit' in input:
                    logger.info(f"[{self.client_address}] quit")
                    break

                (input_cmd, input_data) = input.split(' ', 1) if ' ' in input else (input, None)
                cmd = commands.get(input_cmd, None)
                if cmd:
                    cmd(input_data).process(server, chan)
                else:
                    server.send(chan, f"Command '{input}' is unknown")
                    break

            server.send(chan, f'Goodbye')
            logger.info(f'[{self.client_address}] Channel closed')
            #server.channel.close()
            trans.close()
            return

        except Exception as e:
            logger.exception("*** Caught exception")
            try:
                trans.close()
            except:
                pass

def Main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info("Start Satellite service 🛰️")

    socketserver.ForkingTCPServer.allow_reuse_address = True
    sshserver = socketserver.ForkingTCPServer(("0.0.0.0", port), SSHHandler)
    logger.info(f"listening on {port}")
    sshserver.serve_forever()

if __name__ == '__main__':
    Main()
