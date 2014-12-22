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
from hid import *


def main():
  hid_set_debug(HID_DEBUG_ALL)
  hid_set_usb_debug(0)

  ret = hid_init()
  if ret != HID_RET_SUCCESS:
    logging.getLogger().error("hid_init failed ({}): {}".format(ret, hid_strerror(ret)))

  hid = hid_new_HIDInterface()
  matcher = HIDInterfaceMatcher()
  matcher.vendor_id = 0x188A
  matcher.product_id = 0x1101

  ret = hid_force_open(hid, 0, matcher, 3)
  if ret != HID_RET_SUCCESS:
    logging.getLogger().error("hid_force_open failed ({}): {}".format(ret, hid_strerror(ret)))

  ret = hid_close(hid)
  if ret != HID_RET_SUCCESS:
    logging.getLogger().error("hid_close failed ({}): {}".format(ret, hid_strerror(ret)))

  hid_cleanup()

if __name__ == '__main__':
  main()
