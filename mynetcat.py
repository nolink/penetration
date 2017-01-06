#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os
import sys
import socket
import threading

target = None
port = 0
listen = False
command = None
execute = False

def usage():
    print './mynetcat.py -t localhost -p 80 -l -c ls -e'
    
def client_handler(client_sock):
    client_sock.close()
            
def server_loop():
    global target
    global port    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if not target:
        target = '0.0.0.0'
    sock.bind((target, port))
    sock.listen(5)
    
    print 'listen on %s:%s' % (target, port)
    
    while True:
        client_sock, addr = sock.accept()
        print 'Accept host: %s, %s' % (addr[0], addr[1])
        client_thread = threading.Thread(target=client_handler, args=[client_sock,])
        client_thread.start()
    
def main():
    opts, _ = getopt.getopt(sys.argv[1:], 'hlt:p:c:e', longopts=['help', 'listen', 'target', 'port', 'command', 'execute'])
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
    
    if not listen and target:
        sock = socket.socket(family=AF_INET, type=SOCK_STREAM)
        while True:
            s = sys.stdin.read(1024)
            
    
    if listen:
        server_loop()

main()


