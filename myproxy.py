import os
import sys
import socket
import threading

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(str, unicode) else 2
    
    for i in xrange(0, len(str), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X  %-*s  %s" % (i, length*(digits + 1), hexa, text))
    print b'\n'.join(result)

def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer

def receive_from(sock):
    buffer = ""
    sock.settimeout(2)
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer

def client_handler(client_sock, target_host, target_port, receive_first):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.connect((target_host, target_port))
    if receive_first:
        buffer = receive_from(sock)
        hexdump(buffer)
        
	buffer = response_handler(buffer)
	if len(buffer):
            client_sock.send(buffer)
    while True:
        local_buffer = receive_from(client_sock)
        if len(local_buffer):
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            sock.send(local_buffer)
        buffer = receive_from(sock)
        if len(buffer):
            hexdump(buffer)
            buffer = response_handler(buffer)
            client_sock.send(buffer)
        if not len(buffer) or not len(local_buffer):
            client_sock.close()
            sock.close()
            break

def server_loop(local_host, local_port, target_host, target_port, receive_first):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((local_host, local_port))

    sock.listen(5)

    while True:
        client_sock, addr = sock.accept()
        
        print 'accept on: %s:%s' % (addr[0], addr[1])
        client_thread = threading.Thread(target=client_handler, args=(client_sock,target_host, target_port, receive_first,))
        client_thread.start()

def main():
    if len(sys.argv[1:]) != 5:
        print 'usage: myproxy.py local_host local_port target_host target_port receive_first'
        sys.exit(1)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    target_host = sys.argv[3]
    target_port = int(sys.argv[4])
    
    if 'True' in sys.argv[5]:
        receive_first = True
    else:
        receive_first = False
    
    server_loop(local_host, local_port, target_host, target_port, receive_first)

main()

