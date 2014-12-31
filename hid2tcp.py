#!/usr/bin/env python3
import logging
import threading
import http.server
import base64
import queue

import usb.core
import usb.util

VENDOR_ID  = 0x188a
PRODUCT_ID = 0x1101
HTTP_PORT  = 1711
TIMEOUT    = 10000


def init_usb():
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
    return endpoint_in, endpoint_out
    

def receiver(endpoint_in, data_queue):
    logging.getLogger().info("Reading...")
    while True:
        try:
            packet = endpoint_in.read(endpoint_in.wMaxPacketSize, timeout=TIMEOUT)
        except Exception as e:
            # most probably this is a read timeout
            logging.getLogger().debug("Could not read data: {}".format(e))
            continue

        # got data
        logging.getLogger().info("Got data {}.".format(
                ''.join(['%02x ' % abyte for abyte in packet])))
        data_queue.put(packet)


class HttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def parse_url(self):
        """checks for valid path, which must be: /VENDOR_ID/PRODUCT_ID/RF_PACKET"""
        request_path = self.path.split("/")
        
        # check for number of arguments
        if len(request_path) != 4:
            logging.getLogger().warning('Illegal URL requested: '.format(self.path))
            self.send_error(404, 'Illegal URL requested: '.format(self.path))
            return False
        # check for valid vendor/product ID
        if request_path[1][1:] != str(VENDOR_ID) or request_path[2][1:] != str(PRODUCT_ID):
            logging.getLogger().warning('Illegal vendor/product ID requested: '.format(self.path))
            self.send_error(404, 'Illegal vendor/product ID requested: '.format(self.path))
            return False
            
        # decode RF data
        send_packet_base64 = (request_path[3]+"==")
        self.send_packet = base64.b64decode(send_packet_base64.encode('ascii'), b'-_')
        logging.getLogger().info("RF packet to send: {}".format(
                ''.join(['%02x ' % abyte for abyte in self.send_packet])))
        return True

    def do_GET(self):
        if self.parse_url():
            # send packet
            self.server.usb_endpoint_out.write(self.send_packet)

            # get RF response
            try:
                receive_packet = self.server.data_queue.get(True, TIMEOUT).tobytes()
                receive_packet = base64.b64encode(receive_packet)
            except queue.Empty:
                receive_packet = b''

            # set http response
            self.send_response(200)
            self.send_header('Content-type', 'text/ascii')
            self.end_headers()
            self.wfile.write(receive_packet)

    def do_POST(self):
        if self.parse_url():
            # send packet
            self.server.usb_endpoint_out.write(self.send_packet)

            # set http response
            self.send_response(200)
            self.send_header('Content-type', 'text/ascii')
            self.end_headers()


def main():
    # setup USB
    endpoint_in, endpoint_out = init_usb()
    
    # setup data queue
    data_queue = queue.Queue()
    
    # start receiver thread
    treceiver = threading.Thread(target=receiver, args=(endpoint_in, data_queue))
    treceiver.start()
    
    # setup webserver
    server_address = ('', HTTP_PORT)
    httpd = http.server.HTTPServer(server_address, HttpRequestHandler)
    httpd.usb_endpoint_out = endpoint_out
    httpd.data_queue = data_queue
    # start webserver
    httpd.serve_forever()
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

