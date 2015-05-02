hid2tcp
=======

hid2tcp provides access to USB HID device via a TCP port. To access the USB device it uses libusb.


Installation:
=============

- clone this repository to a convenient place
- as root, run
  python3 setup.py develop
- copy or link the config file to /etc/hid2tcp.conf
- copy or link the system-v init file init.d to /etc/init.d/hid2tcp
- install the service using update-rc.d enable /etc/init.d/hid2tcp


Dependencies:
=============

To use this library you need to have
- python3 installed
- libusb installed (which should be the case on a Linux system)

There are some python library dependencies which get automatically installed when you run setup.py.

The code is tested to run on a Rhaspberry Pi using Debian Linux.
The code is platform independent and should also run on other operating systems.
On Windows there is the known limitation that message pipes cannot be handled by the select IO multiplexing. Therefore it would need minor adaptation for a windows system.


Usage:
======
You need to configure hid2tcp to the correct USB vendor and product IDs. You may also want to change the port number of the used TCP socket.

The client needs to send the vendor and product ID as the first 4 bytes after opening the socket. This authenticates the client. Afterwards it may send arbitrary byte sequences which are then forwarded to the USB port. Also it may read from the socket to get all messages received from the USB port.
