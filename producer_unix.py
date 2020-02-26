import multiprocessing
import math 
import sys
import time
from rawsocketpy import RawSocket
import socket
import os

def producer(packet,num_chunks,client_socket,lock,index,interval):  
    i=0
    while i < num_chunks:
        lock.acquire()
        client_socket.send(packet)
        #time.sleep(0.00005) # 50 us
        i += 1
        if i % interval == 0:
            print("Thread " + index + " sent " + str(i) + " packets...")
        lock.release()
        #time.sleep(0.00005) # 50 us

interval = 200000
header_len_C = 42
chunk_size = int(sys.argv[2]) + header_len_C
num_chunks = int(sys.argv[3])
procCount = int(sys.argv[1])
socket_name = "/tmp/unix_dgram"
data_size = chunk_size * num_chunks
packet = ""
i=0
while i < chunk_size-1:
    packet += "x"
    i += 1

packet += "a" 

packet = packet.encode("utf-8")

client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
client_socket.connect(socket_name)
print("Ready.")

lock = multiprocessing.Lock()

procs = []

for i in range(0,procCount):
    p = multiprocessing.Process(target=producer, args=(packet,num_chunks,client_socket,lock,str(i),interval))
    procs.append(p)

start = time.time()  

for p in procs:
    p.start()

for p in procs:
    p.join()

end = time.time()

data_size = chunk_size*num_chunks*procCount/1000000
print("Done.")
print("Total chunks produced: " + str(num_chunks*procCount))
print("Total data sent: " + str(data_size) + " MB")
print("Elapsed time for PRODUCER: " + str(end-start) + " seconds")
print("Bandwidth: " + str(data_size/(end-start)) + " MB/s")


