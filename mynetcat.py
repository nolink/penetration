#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os
import sys
import socket
import subprocess
import threading

target = None
port = 0
listen = False
command = False
execute = ''
upload_dest = ''

def usage():
    print './mynetcat.py -t localhost -p 80 -l -c -u xx -e xx'
   
def run_command(cmd_str):
    cmd_str = cmd_str.rstrip()
    try:
        output = subprocess.check_output(cmd_str, stderr=subprocess.STDOUT, shell = True)
    except:
        output = "failed"
    return output
 
def client_handler(client_sock):
    global upload
    global execute
    global command
    
    if len(upload_dest):
        file_buffer = ""
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        try:
            with open(upload_dest, 'wb') as fd:
                fd.write(file_buffer)
            client_sock.send('succesfully save file to %s\r\n' % upload_dest)
        except:
            client_sock.send('failed to save file to %s\r\n' % upload_dest)

    if len(execute):
        output = run_command(execute)
        client_sock.send(output)

    if command:
        while True:
            client_sock.send("<MYNETCAT:#>")
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_sock.recv(1024)
            resp = run_command(cmd_buffer)
            client_sock.send(resp)
             
        
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
    
def client_sender(buffer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((target, port))
        if len(buffer):
            sock.send(buffer)
        
        while True:
            recv_len = 1
            resp = ""
            while recv_len:
                data = sock.recv(4096)
                recv_len = len(data)
                resp += data
                if recv_len < 4096:
                    break
            print resp
            buffer = raw_input("")
            buffer += "\n"
            sock.send(buffer)
    except:
        print 'error, exiting...'
        sock.close()    

def main():
    opts, _ = getopt.getopt(sys.argv[1:], 'hlt:p:u:e:c', longopts=['help', 'listen', 'target', 'port', 'command','upload', 'execute'])
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
            command = True
        elif p in ('-e', '--execute'):
            execute = arg
        elif p in ('-u', '--upload'):
            upload_dest = arg
        else:
            print 'error'
            sys.exit(1)
    
    if not listen and len(target) and port  > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)
            
    
    if listen:
        server_loop()

main()


