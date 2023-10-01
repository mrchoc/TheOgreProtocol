import sys
import subprocess
import os
import argparse
import random
import time
import signal
import utils

signal.signal(signal.SIGINT, utils.signal_handler)

num_relays = 3
num_exits = 2

parser = argparse.ArgumentParser()
parser.add_argument("dir_auth_port", type=int, help="the port number of the directory authority")
parser.add_argument("dest_port", type=int, help="the port number of the client's destination")
args = parser.parse_args()

os.system("~/.pyenv/versions/2.7.18/bin/python2.7 directory_authority.py " + str(args.dir_auth_port) + " &")
#wait for directory authority to spin up
time.sleep(1)

port_range = range(7000,9000)
ports = random.sample(port_range,num_relays+num_exits)
exit_port = "6666"
for port in ports[:num_relays]:
	os.system("~/.pyenv/versions/2.7.18/bin/python2.7 node.py " + str(port) + " 127.0.0.1 " + str(args.dir_auth_port) + " &")
	time.sleep(1)

for port in ports[-1*num_exits:]:
	os.system("~/.pyenv/versions/2.7.18/bin/python2.7 node.py " + str(port) + " 127.0.0.1 " + str(args.dir_auth_port) + " --exit &")
	time.sleep(1)

os.system("~/.pyenv/versions/2.7.18/bin/python2.7 client.py " + "127.0.0.1 " + str(args.dir_auth_port) + " 127.0.0.1 " +str(args.dest_port))#+ " &")
