import json
import socket

def recvall(sock):
	BUFF_SIZE = 32
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
	datas = []
	string = bytes.decode('utf8')
	frames = string.split('}{')
	for frame in frames:
		if frame[:1] != '{': frame = '{' + frame
		if frame[-1] != '}': frame += '}'
		datas.append(json.loads(frame))
	return datas