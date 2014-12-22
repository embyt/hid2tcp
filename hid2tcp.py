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


def main():
    hidwrap.set_debug(hidwrap.HID_DEBUG_ALL)
    hidwrap.set_usb_debug(0)

    iface = hidwrap.Interface(vendor_id=0x188A, product_id=0x1101)


if __name__ == '__main__':
  main()
