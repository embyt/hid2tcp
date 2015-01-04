#!/usr/bin/env python3
import syslog
import logging
import threading
import queue
import socket
import os
import select
import configparser

import usb.core
import usb.util

TIMEOUT    = 10000


class UsbInterface(threading.Thread):
    def __init__(self, config, pipeout):
        self.config = config
        self.pipeout = pipeout
        self.VENDOR_ID = int(self.config['vendor_id'], 16)
        self.PRODUCT_ID = int(self.config['product_id'], 16)
        
        # setup USB
        try:
            self.init_usb()
        except Exception as e:
            syslog.syslog('hid2tcp: error initializing USB: ' + str(e))
            raise
        
        # init reader thread
        threading.Thread.__init__(self) 
        
    def init_usb(self):
        # find device
        self.dev = usb.core.find(idVendor=self.VENDOR_ID, idProduct=self.PRODUCT_ID)
        if self.dev is None:
            raise ValueError('Device not found')

        try:
            self.dev.detach_kernel_driver(0)
            logging.getLogger().info("Kernel detach done.")
        except Exception as e:
            # this usually mean that there was no other driver active
            logging.getLogger().debug("Kernel detach not done: {}".format(e))

        # set the active configuration; 
        # with no arguments, the first configuration will be the active one
        #self.dev.set_configuration()

        logging.getLogger().info("claiming device")
        usb.util.claim_interface(self.dev, 0)

        # getting device data
        usb_cfg = self.dev.get_active_configuration()
        usb_interface = usb_cfg[(0,0)]
        self.endpoint_in = usb_interface[0]
        self.endpoint_out = usb_interface[1]

    def send(self, data):
        logging.getLogger().info("Sending data: {}".format(
                ''.join(['%02x ' % abyte for abyte in data])))
        # send packet
        self.endpoint_out.write(data)
        
    def run(self):
        logging.getLogger().info("Starting USB reading.")
        while True:
            try:
                packet = self.endpoint_in.read(self.endpoint_in.wMaxPacketSize, timeout=TIMEOUT)
            except Exception as e:
                # most probably this is a read timeout
                logging.getLogger().debug("Could not read data: {}".format(e))
                continue

            # got data
            logging.getLogger().info("Got data {}.".format(
                    ''.join(['%02x ' % abyte for abyte in packet])))
            # write data length
            os.write(self.pipeout, bytes([len(packet)]))
            # write data
            os.write(self.pipeout, packet)


class Hid2Tcp():
    def __init__(self):
        # load config file
        config = configparser.ConfigParser()
        config.read("hid2tcp.conf")
        self.config = config['hid2tcp']
        
        # setup data queue
        self.pipein, pipeout = os.pipe()
        
        # setup USB
        self.usb_interface = UsbInterface(self.config, pipeout)
        
        syslog.syslog('hid2tcp: initialized successfully')

        
    def run(self): 
        # start USB receiver thread
        self.usb_interface.start()
        
        # create an INET, STREAMing socket
        serversocket = socket.socket()
        # avoid problems with binding if address is not released yet
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
        # bind the socket to localhost, only accepting local connections
        serversocket.bind(('localhost', int(self.config['tcp_port'])))
        # become a server socket
        serversocket.listen(5)
        # no active client yet
        self.clients = []
        self.authorized = []

        # main loop
        while True:
            # setup IO multiplexing structures
            readers = [self.pipein, serversocket]
            readers += self.clients
            
            # blocking wait for new data
            logging.getLogger().debug("Waiting for data or connection.")
            ready_to_read, ready_to_write, in_error = select.select(readers, [], [], TIMEOUT/1000)
            
            # check for new socket connection
            if serversocket in ready_to_read:
                # accept connection
                logging.getLogger().info("New connection detected.")
                (clientsocket, address) = serversocket.accept()
                self.clients.append(clientsocket)
                self.authorized.append(False)
            
            # check for data from USB
            if self.pipein in ready_to_read:
                self.handle_pipein()
            
            # check for data from socket clients
            for i in range(len(self.clients)):
                if self.clients[i] in ready_to_read:
                    if self.handle_client(i) == False:
                        # client shall be removed
                        del self.clients[i]
                        del self.authorized[i]
                        # abort for loop of modified structure
                        break

                        
    def handle_pipein(self):
        # read size of data
        data_size = os.read(self.pipein, 1)
        if len(data_size) != 1:
            raise Exception("Illegal size info received: {}".format(
                    ''.join(['%02x ' % abyte for abyte in data_size])))
        data_size = data_size[0]
        # blocking read of data
        data = os.read(self.pipein, data_size)
        logging.getLogger().info("Transfering USB data ({} bytes).".format(data_size))
        
        # send data to all authorized clients
        for i in range(len(self.clients)):
            if self.authorized[i]:
                # send data
                self.clients[i].send(data)
    
    def handle_client(self, i):
        # current client
        client = self.clients[i]
        # get data
        data = client.recv(4096)
        if len(data) == 0:
            logging.getLogger().info("Client left.")
            # client closed connection
            return False

        # is this authorization data or hid data?
        if self.authorized[i]:
            # got hid data
            logging.getLogger().info("Got data to transmit.")
            self.usb_interface.send(data)
        else:
            # check authorization
            if len(data) == 4 and \
               (data[0]<<8)|data[1] == int(self.config['vendor_id'], 16) and \
               (data[2]<<8)|data[3] == int(self.config['product_id'], 16):
                # authorization successful
                logging.getLogger().info("Client authorization succeeded.")
                self.authorized[i] = True
                # echo data back to commit authentication
                client.send(data)
            else:
                # authorization failed
                logging.getLogger().info("Client authorization failed.")
                client.close()
                return False

        return True


def main():
    #logging.basicConfig(level=logging.INFO)
    hid2tcp = Hid2Tcp()
    hid2tcp.run()
    
if __name__ == '__main__':
    main()
