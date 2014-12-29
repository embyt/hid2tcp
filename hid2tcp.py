#!/usr/bin/env python3
import logging
import threading
import time

import usb.core
import usb.util

VENDOR_ID  = 0x188a
PRODUCT_ID = 0x1101
INTERFACE = 0

#ENDPOINT_IN  = 0x81
ENDPOINT_OUT = 0x02
#EP_SIZE_OUT = 32
#EP_SIZE_IN = 19


bmRequestTypeOut = 0x21
bRequest = 0x09 # SET_REPORT
report_type = 2  # 2 = HID_RT_OUTPUT; 3==HID feat.report
report_id = 0
wValue = (report_type << 8) | report_id   # 0x02 .. Report Type Output 
wIndex = 0  # Interface 
wLength = 0 # zero


def pack_request(packet_size, *arguments):
    packet = [0x0] * packet_size
    i = 0
    for arg in arguments:
        packet[i] = arg
        i += 1
    return ''.join([chr(c) for c in packet])

    
def send(dev, packet):
    """
    Write command to blink(1)
    Send USB Feature Report 0x01 to blink(1) with 8-byte payload
    Note: arg 'buf' must be 8 bytes or bad things happen
    """
    
    # int len = usb_control_msg(hidif->dev_handle,
      # USB_ENDPOINT_OUT + USB_TYPE_CLASS + USB_RECIP_INTERFACE,
      # = 0 + (0x01 << 5) + 0x01
      # HID_REPORT_SET,
      # hidif->hid_data->ReportID + (HID_RT_OUTPUT << 8),
      # hidif->interface,
      # (char*)buffer, size, USB_TIMEOUT);
    # usb.util.CTRL_OUT, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE
    # 0, 32, 1 -> 33

    bmRequestTypeOut = usb.util.build_request_type(usb.util.CTRL_OUT, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE)
    #dev.ctrl_transfer( bmRequestTypeOut, bRequest, wValue, wIndex, packet)
    dev.write(ENDPOINT_OUT, packet)
    #dev.write(packet)

    
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
    except Exception as e: # this usually mean that kernel driver has already been dettached
        logging.getLogger().info("Kernel detach not done: {}".format(e))

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    #dev.set_configuration()

    logging.getLogger().info("claiming device")
    #usb.util.claim_interface(dev, INTERFACE)

    # getting device data
    cfg = dev.get_active_configuration()
    interface_number = cfg[(0,0)].bInterfaceNumber
    endpoint_in = cfg[(0,0)][0]
    endpoint_out = cfg[(0,0)][1]
    
    #import pdb; pdb.set_trace()
    
    # start receiver thread
    treceiver = threading.Thread(target=receiver, args=(dev, endpoint_in))
    treceiver.start()
       
    while True:
        # perform communication
        time.sleep(3)
        packet = pack_request(5, report_id, 0x04, 0xb2, 0x1b, 0x00)
        #packet = pack_request(endpoint_out.wMaxPacketSize, 0x04, 0xb2, 0x04, 0x00)
        #packet = pack_request(endpoint_out.wMaxPacketSize, 0x11, 0xd1, 0x21, 0x00, 0x00, 0x00, 0x00, 0x07, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
        logging.getLogger().info("Sending {}.".format(
                ''.join(['%02x ' % ord(abyte) for abyte in packet])))
        send(dev, packet)

    # done
    logging.getLogger().info("release claimed interface")
    #usb.util.release_interface(dev, interface)

    
def main2():
    # Find all the USB busses
    for bus in usb.busses():
        for device in bus.devices:
            if device.idVendor == VENDOR_ID and device.idProduct == PRODUCT_ID:
                dev=device
    handle=dev.open()
    
    packet = pack_request(4, 0x04, 0xb2, 0x1b, 0x00)

    handle.controlMsg(bmRequestTypeOut, bRequest, packet, wValue, wIndex, 100)



if __name__ == '__main__':
  main()

