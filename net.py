import json
import socket

def recvall(sock):
	BUFF_SIZE = 4 # 4 KiB
	data = b''
	while True:
		part = sock.recv(BUFF_SIZE)
		data += part
		if len(part) < BUFF_SIZE:
			break
	return data

def data2bytes(data):
    return bytes(json.dumps({'data' : data}), encoding='utf8')
    
def bytes2data(bytes):
	return json.loads(bytes.decode('utf8'))
