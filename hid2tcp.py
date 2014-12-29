#!/usr/bin/env python3
import logging
import threading
import time
import os

#os.environ['PYUSB_DEBUG_LEVEL'] = 'debug'
#os.environ['PYUSB_DEBUG'] = 'debug'

import usb.core
import usb.util

VENDOR_ID  = 0x188a
PRODUCT_ID = 0x1101


def receiver(dev, endpoint):
    while True:
        logging.getLogger().info("Reading...")
        try:
            bytes = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, timeout=10000)
        except Exception as e:
            logging.getLogger().info("Could not read data: {}".format(e))
            continue

        # got data
        logging.getLogger().info("Got data {}.".format(
                ''.join(['%02x ' % abyte for abyte in bytes])))


def main():
    logging.basicConfig(level=logging.DEBUG)
    
    # find device
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if dev is None:
        raise ValueError('Device not found')

    try:
        dev.detach_kernel_driver(0)
        logging.getLogger().info("Kernel detach done.")
    except Exception as e:
        # this usually mean that there was no other driver active
        logging.getLogger().debug("Kernel detach not done: {}".format(e))

    # set the active configuration; 
    # with no arguments, the first configuration will be the active one
    #dev.set_configuration()

    logging.getLogger().info("claiming device")
    #usb.util.claim_interface(dev, INTERFACE)

    # getting device data
    usb_cfg = dev.get_active_configuration()
    usb_interface = usb_cfg[(0,0)]
    endpoint_in = usb_interface[0]
    endpoint_out = usb_interface[1]
    
    # start receiver thread
    treceiver = threading.Thread(target=receiver, args=(dev, endpoint_in))
    treceiver.start()
       
    while True:
        # perform communication
        time.sleep(3)
        packet = bytes([4,0xb2,0x1b,0])
        logging.getLogger().info("Sending {}.".format(
                ''.join(['%02x ' % int(abyte) for abyte in packet])))
        endpoint_out.write(packet)

    # done
    logging.getLogger().info("release claimed interface")
    #usb.util.release_interface(dev, interface)


if __name__ == '__main__':
  main()

