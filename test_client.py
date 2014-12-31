#!/usr/bin/env python3
import logging
import urllib.request
import base64


VENDOR_ID  = 0x188a
PRODUCT_ID = 0x1101
HTTP_PORT  = 1711

packet = bytes([4, 0xb2, 0x1b, 0])


logging.basicConfig(level=logging.DEBUG)
logging.getLogger().info("Sending {}.".format(
        ''.join(['%02x ' % int(abyte) for abyte in packet])))

# create URL
packet_base64=base64.b64encode(packet, b'-_').decode('ascii')[:-2]
url = "http://localhost:{}/v{}/p{}/{}".format(HTTP_PORT, VENDOR_ID, PRODUCT_ID, packet_base64)
logging.getLogger().info("Requesting {}.".format(url))

# send request
response = urllib.request.urlopen(url)

# dump answer
received_base64=response.read()
received=base64.b64decode(received_base64)
logging.getLogger().info("Got: {}".format(
        ''.join(['%02x ' % int(abyte) for abyte in received])))
