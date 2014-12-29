#!/usr/bin/env python3
import threading
import sys
import logging
import os
import time

# add libhid to path
#libsdir = os.getcwd() + '/.libs'   # allow it to run right out of the build dir
libsdir = '/usr/local/lib/python3/dist-packages/libhid'
if os.path.isdir(libsdir) and os.path.isfile(libsdir + '/_hid.so'):
  sys.path.insert(0, libsdir)

# user defined imports
import hidwrap

VENDOR_ID  = 0x188A
PRODUCT_ID = 0x1101
ENDPOINT_IN  = 0x81
ENDPOINT_OUT = 0x02
REPORT_ID = 0

#HID_DEVICE_PATH = [0xffa00001, 0xffa00002, 0xffa10005]
HID_DEVICE_PATH = [-6291455, -6291454, -6291451]


def pack_request(packet_size, *arguments):
    packet = [0x0] * packet_size
    i = 0
    for arg in arguments:
        packet[i] = arg
        i += 1
    return ''.join([chr(c) for c in packet])


def receiver(hid_handle):
    while True:
        logging.getLogger().info("Reading...")
        try:
            packet = hid_handle.interrupt_read(ENDPOINT_IN, 10000)
        except Exception as e:
            logging.getLogger().info("Could not read data: {}".format(e))
            continue

        # got data
        logging.getLogger().info("Got data {}.".format(
                ''.join(['%02x ' % ord(abyte) for abyte in packet])))


def main():
    logging.getLogger().info("start")
    hidwrap.set_debug(hidwrap.HID_DEBUG_ALL)
    hidwrap.set_usb_debug(0)

    logging.getLogger().info("searching for device")
    hid_handle = hidwrap.Interface(vendor_id=VENDOR_ID, product_id=PRODUCT_ID)
    logging.getLogger().info("set idle")
    hid_handle.set_idle(32, 0)


    # start receiver thread
    treceiver = threading.Thread(target=receiver, args=(hid_handle,))
    treceiver.start()
    

    while True:
        # perform communication
        time.sleep(3)
        packet = pack_request(5, REPORT_ID, 0x04, 0xb2, 0x1b, 0x00)
        logging.getLogger().info("Sending {}.".format(
                ''.join(['%02x ' % ord(abyte) for abyte in packet])))
        ret = hid_handle.set_output_report(HID_DEVICE_PATH, packet)
        logging.getLogger().info("packet sent")

   
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
