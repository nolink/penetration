#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os
import sys
import socket
import threading

target = ''
port = 0
listen = False
command = ''
execute = False

def usage():
    print './mynetcat.py -t localhost -p 80 -l -c ls -e'
    
def main():
    opts, _ = getopt.getopt(sys.argv[1:], 'h:t:p:l:c:e', longopts=['help', 'target', 'port', 'listen', 'command', 'execute'])
    global target
    global port
    global listen
    global command
    global execute
    for p, arg in opts:
        if p in ('-h', '--help'):
            usage()
            break
        elif p in ('-t', '--target'):
            target = arg
        elif p in ('-p', '--port'):
            port = int(arg)
        elif p in ('-l', '--listen'):
            listen = True
        elif p in ('-c','--command'):
            command = arg
        elif p in ('-e', '--execute'):
            execute = True
        else:
            print 'error'
            sys.exit(1)
    
    if listen:
        server_loop()
    

def client_handler(client_sock):
    client_sock.close()
            
def server_loop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', port))
    sock.listen(5)
    
    print 'listen on %s:%s' % ('localhost', port)
    
    while True:
        client_sock, addr = sock.accept()
        print 'Accept host: %s, %s' % (addr[0], addr[1])
        client_thread = threading.Thread(target=client_handler, args=[client_handler,])
        client_thread.start()


main()


