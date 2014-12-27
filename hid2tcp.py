#!/usr/bin/env python3
import os
import logging
import time

import usb.core
import usb.util

VENDOR_ID  = 0x188a
PRODUCT_ID = 0x1101
INTERFACE = 0

ENDPOINT_IN  = 0x81
ENDPOINT_OUT = 0x02
EP_SIZE_OUT = 32
EP_SIZE_IN = 19


def pack_request(*arguments):
    packet = [0x0] * EP_SIZE_OUT
    i = 0
    for arg in arguments:
        packet[i] = arg
        i += 1
    return ''.join([chr(c) for c in packet])


def main():
    logging.basicConfig(level=logging.DEBUG)

    # find device
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if dev is None:
        raise ValueError('Device not found')

    try:
        dev.detach_kernel_driver(0)
        logging.getLogger().info("Kernel detach done.")
    except Exception as e: # this usually mean that kernel driver has already been dettached
        logging.getLogger().info("Kernel detach not done: {}".format(e))

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    #dev.set_configuration()

    logging.getLogger().info("claiming device")
    #usb.util.claim_interface(dev, INTERFACE)

    # getting device data
    endpoint_in = dev[0][(0,0)][0]
    endpoint_out = dev[0][(0,0)][1]
    EP_SIZE_OUT = endpoint_out.wMaxPacketSize
    
    # perform communication
    packet = pack_request(0x04, 0xb2, 0x1b, 0x00)
    logging.getLogger().info("Sending {}.".format(
            ''.join(['%x ' % ord(abyte) for abyte in packet])))
    dev.write(endpoint_out.bEndpointAddress, packet, timeout=2000)

    logging.getLogger().info("Reading...")
    bytes = dev.read(endpoint_in.bEndpointAddress,  endpoint_in.wMaxPacketSize, timeout=2000)
    logging.getLogger().info("Got data {}.".format(
            ''.join(['%x ' % abyte for abyte in bytes])))

    # done
    logging.getLogger().info("release claimed interface")
    #usb.util.release_interface(dev, interface)


if __name__ == '__main__':
  main()

