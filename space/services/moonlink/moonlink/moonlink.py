#!/usr/local/bin/python3 -u

import binascii
import sys
import subprocess

from mooncomms import *
from datetime import datetime

if __name__ == '__main__':
    logging.basicConfig(filename='moonlog.txt',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d [%(levelname)s] %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    logging.info("Moonlink Service 🌘🛰️📶")

    inp = ""
    while inp not in ['stop', 'quit', 'q']:
        sys.stdout.write(">\n")  # Ask for input

        t = datetime.now()
        buf = sys.stdin.readline().strip()
        inp = binascii.unhexlify(buf)
        #cmd = ['/bin/echo',inp,'>>','/var/log/dcsc']
        #subprocess.run(cmd)
        if "kill" in str(inp):
            break
        if "egrep" in str(inp):
            break
        request = pickle.loads(inp)

        # Wrap the processing in a try/except. We do not want a rogue request crash our service, do we?
        try:
            response = request.process()
        except Exception as e:  # noqa
            logging.error(f"Responding to the request failed: {e}")
            print(f"Responding to the request failed: {e}")
        else:
            logging.debug(f"{datetime.now() - t}: send back {response}")
            sys.stdout.write(binascii.hexlify(response.dump()).decode()+'\n')
