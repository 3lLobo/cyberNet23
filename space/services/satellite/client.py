#!/usr/bin/env python3

import argparse
import base64
import sys
from pathlib import Path
from time import sleep

import paramiko

parser=argparse.ArgumentParser(
    description="ImageSync Client. Use the satellite password to retrieve the last captured image. Use status/status to get a list of satellites.")
parser.add_argument('--username', '-u', type=str, required=True, help='username')
parser.add_argument('--password', '-p', type=str, required=True, help='password')
parser.add_argument('--host', '-H', type=str, required=False, default='localhost')
parser.add_argument('--port', '-P', type=int, required=False, default=2222, help='port')
parser.add_argument('--query', '-q', type=str, required=False, default='*', help='query to filter list of sattelites')
args=parser.parse_args()

host = args.host
port = args.port
username = args.username
password = args.password
query = args.query

print(f"connecting to {host}:{port}")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    if username == 'status':
        ssh.connect(host, port, username, "status")
    else:
        ssh.connect(host, port, username, password)
except Exception as e:
    ssh.close()
    sys.exit(e)    

channel = ssh.invoke_shell()

def send(data):
        if isinstance(data, str):
            return channel.sendall(data + '🛰️🛑\n')
        return channel.sendall(data + '🛰️🛑\n'.encode('utf-8'))

def receive():
    r = b''
    while not '🛰️🛑\n'.encode('utf-8') in r:
        data = channel.recv(1024)
        if not data:
            break
        r += data
    return r.replace('🛰️🛑\n'.encode('utf-8'), b'').decode()

receive()

if username == 'status':
    send(f'satellites {query}')
    satellite_names = [x for x in receive().split('\n') if x]
    print(', '.join(satellite_names))
else:
    Path(f'sat_data').mkdir(exist_ok=True)
    Path(f'sat_data/{username}').mkdir(exist_ok=True)
    
    print(f"Get filename for {username}...")
    send(f"latest_filename {username}")
    file_name = receive().strip()
    
    send(f"timestamp {file_name}")
    print(f"Latest file is from {receive()}")
    
    Path(f'sat_data/{username}').mkdir(exist_ok=True)
    Path(f'sat_data/{username}/{file_name}').touch()
    print("Sync", file_name, '...')
    send(f"get_satellite_image {file_name}")
    recv = receive()
    if recv.startswith('Error!'):
        sys.exit(recv)
    
    with open(f'sat_data/{username}/{file_name}', 'wb') as f:
        f.write(base64.b64decode(recv))

send('quit')
receive()
ssh.close()
