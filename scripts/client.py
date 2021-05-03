#!/usr/bin/python

import socket, cv2, pickle, struct, sys, time

base_t = time.time()
# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = sys.argv[1] + '.tcp.ngrok.io' # paste your server ip address here
port = int(sys.argv[2])
#host_ip = '127.0.1.1' # paste your server ip address here
#port = 9999
client_socket.connect((host_ip, port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")

print(time.time() - base_t)

while True:
    base_t = time.time()
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) # 4K
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("RECEIVING VIDEO",frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break
    print(time.time() - base_t)
client_socket.close()
