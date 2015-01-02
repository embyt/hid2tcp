#!/usr/bin/env python3
import logging
import socket
import sys


VENDOR_ID  = 0x188a
PRODUCT_ID = 0x1101
TCP_PORT   = 1711



logging.basicConfig(level=logging.DEBUG)

# open connection; create an INET, STREAMing socket
serversocket = socket.socket()
# connect to server
serversocket.connect(('localhost', TCP_PORT))

# send authentication
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
received=serversocket.recv(4096)
logging.getLogger().info("Got: {}".format(
        ''.join(['%02x ' % int(abyte) for abyte in received])))
