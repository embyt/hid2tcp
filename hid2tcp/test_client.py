#!/usr/bin/env python3
import logging
import socket
import sys
import configparser


# setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

# load config file
config = configparser.ConfigParser()
config.read("hid2tcp.conf")

# open connection; create an INET, STREAMing socket
serversocket = socket.socket()
# connect to server
serversocket.connect(('localhost', int(config.get('hid2tcp', 'tcp_port'))))

# send authentication
VENDOR_ID = int(config.get('hid2tcp', 'vendor_id'), 16)
PRODUCT_ID = int(config.get('hid2tcp', 'product_id'), 16)
auth_packet = bytes([VENDOR_ID>>8, VENDOR_ID&0xff, PRODUCT_ID>>8, PRODUCT_ID&0xff])
serversocket.send(auth_packet)

# get authentication response
if serversocket.recv(len(auth_packet)):
    logging.getLogger().info("Authorized successfully")
else:
    logging.getLogger().info("Authorization failed")
    sys.exit(1)

# send request
packet = bytes([4, 0xb2, 0x1b, 0])
logging.getLogger().info("Sending {}.".format(
        ''.join(['%02x ' % int(abyte) for abyte in packet])))
serversocket.send(packet)

# dump answer
while True:
    received=serversocket.recv(4096)
    if len(received) == 0:
        logging.getLogger().info("Server socket closed. Exiting.")
        sys.exit()
    logging.getLogger().info("Got: {}".format(
            ''.join(['%02x ' % int(abyte) for abyte in received])))
