#!/usr/bin/env python3

import sys
import logging
import os

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

HID_DEVICE_PATH = [0xffa00001, 0xffa00002, 0xffa10005]


def main():
    hidwrap.set_debug(hidwrap.HID_DEBUG_ALL)
    hidwrap.set_usb_debug(0)

    hid = hidwrap.Interface(vendor_id=VENDOR_ID, product_id=PRODUCT_ID)
    hid.set_idle(32, 0)

    # Send a packet requesting release info: 04 b2 1b 00 00 00
    frame = bytes([0x04, 0xb2, 0x1b, 0x00, 0x00, 0x00])
    logging.getLogger().info("send packet")
    ret = hid.set_output_report(HID_DEVICE_PATH, "".join(map(chr, frame)))
    
    logging.getLogger().info("receive packet")
    in_packet = hid.interrupt_read(ENDPOINT_IN, 1000)

   
if __name__ == '__main__':
  main()
