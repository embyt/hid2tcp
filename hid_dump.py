#! /usr/bin/env python3

import usb.core
import usb.util
import sys

# find our device
dev = usb.core.find(idVendor=0x188A, idProduct=0x1101)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# Display Device Descriptor
sys.stdout.write('dev.bLength=' + str(dev.bLength) + '\n')
sys.stdout.write('dev.bDescriptorType=' + str(dev.bDescriptorType) + '\n')
sys.stdout.write('dev.bcdUSB=' + str(dev.bcdUSB) + '\n')
sys.stdout.write('dev.bDeviceClass=' + str(dev.bDeviceClass) + '\n')
sys.stdout.write('dev.bDeviceSubClass=' + str(dev.bDeviceSubClass) + '\n')
sys.stdout.write('dev.bDeviceProtocol=' + str(dev.bDeviceProtocol) + '\n')
sys.stdout.write('dev.bMaxPacketSize0=' + str(dev.bMaxPacketSize0) + '\n')
sys.stdout.write('dev.idVendor=' + str(dev.idVendor) + '\n')
sys.stdout.write('dev.idProduct=' + str(dev.idProduct) + '\n')
sys.stdout.write('dev.bcdDevice=' + str(dev.bcdDevice) + '\n')
sys.stdout.write('dev.iManufacturer=' + str(dev.iManufacturer) + '\n')
sys.stdout.write('dev.iProduct=' + str(dev.iProduct) + '\n')
sys.stdout.write('dev.iSerialNumber=' + str(dev.iSerialNumber) + '\n')
sys.stdout.write('dev.bNumConfigurations=' + str(dev.bNumConfigurations) + '\n')


#To access the configurations available in the device, you can iterate over the device
for cfg in dev:
    # Display Configuration Descriptor
    sys.stdout.write('\t' + 'cfg.bLength=' + str(cfg.bLength) + '\n')
    sys.stdout.write('\t' + 'cfg.bDescriptorType=' + str(cfg.bDescriptorType) + '\n')
    sys.stdout.write('\t' + 'cfg.wTotalLength=' + str(cfg.wTotalLength) + '\n')
    sys.stdout.write('\t' + 'cfg.bNumInterfaces=' + str(cfg.bNumInterfaces) + '\n')
    sys.stdout.write('\t' + 'cfg.bConfigurationValue=' + str(cfg.bConfigurationValue) + '\n')
    sys.stdout.write('\t' + 'cfg.iConfiguration=' + str(cfg.iConfiguration) + '\n')
    sys.stdout.write('\t' + 'cfg.bmAttributes=' + str(cfg.bmAttributes) + '\n')
    sys.stdout.write('\t' + 'cfg.bMaxPower=' + str(cfg.bMaxPower) + '\n')

    # Display Interface Descriptor
    for intf in cfg:
        sys.stdout.write('\t\t' + 'intf.bLength=' + str(intf.bLength) + '\n')
        sys.stdout.write('\t\t' + 'intf.bDescriptorType=' + str(intf.bDescriptorType) + '\n')
        sys.stdout.write('\t\t' + 'intf.bInterfaceNumber=' + str(intf.bInterfaceNumber) + '\n')
        sys.stdout.write('\t\t' + 'intf.bAlternateSetting=' + str(intf.bAlternateSetting) + '\n')
        sys.stdout.write('\t\t' + 'intf.bNumEndpoints=' + str(intf.bNumEndpoints) + '\n')
        sys.stdout.write('\t\t' + 'intf.bInterfaceClass=' + str(intf.bInterfaceClass) + '\n')
        sys.stdout.write('\t\t' + 'intf.bInterfaceSubClass=' + str(intf.bInterfaceSubClass) + '\n')
        sys.stdout.write('\t\t' + 'intf.bInterfaceProtocol=' + str(intf.bInterfaceProtocol) + '\n')
        sys.stdout.write('\t\t' + 'intf.iInterface=' + str(intf.iInterface) + '\n')

        # Display Endpoint Descriptor
        for ep in intf:
            sys.stdout.write('\t\t\t' + 'ep.bLength=' + str(ep.bLength) + '\n')
            sys.stdout.write('\t\t\t' + 'ep.bDescriptorType=' + str(ep.bDescriptorType) + '\n')
            sys.stdout.write('\t\t\t' + 'ep.bEndpointAddress=' + str(ep.bEndpointAddress) + '\n')
            sys.stdout.write('\t\t\t' + 'ep.bmAttributes=' + str(ep.bmAttributes) + '\n')
            sys.stdout.write('\t\t\t' + 'ep.wMaxPacketSize=' + str(ep.wMaxPacketSize) + '\n')
            sys.stdout.write('\t\t\t' + 'ep.bInterval=' + str(ep.bInterval) + '\n')


# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

#msg = [0x05, 0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20]

#dev.ctrl_transfer(bmRequestType=0x42, bRequest=0x09, wValue=0x02, wIndex=0x00, data_or_wLength=msg, timeout=100)

#sent_bytes = dev.write(0x00, msg, 0, 100)

#assert dev.ctrl_transfer(0x40, CTRL_LOOPBACK_WRITE, 0, 0, msg) == len(msg)
#ret = dev.ctrl_transfer(0x40, CTRL_LOOPBACK_READ, 0, 0, len(msg))
#sret = ''.join([chr(x) for x in ret])
#assert sret == msg




