import socket
import datetime
import math
import random
import sys
from argparse import ArgumentParser
from threading import Thread

parser = ArgumentParser()
parser.add_argument("role", help="Choose whether to run as server or client")

args = parser.parse_args()


def combine(lov):
	lov.sort()
	z = int((round(len(lov)*.25)) - 1)

	for i in range (0,(z)):
	    del lov[i]
	    del lov[(len(lov)-1)-i]
		
	average = float(sum(lov)/len(lov))
	return average
	#prints list, sum, length, and average
	#print(lov)
	#print(sum(lov))
	#print(len(lov))
	#print(average)

def send_data(i, addr, conn):
	#connect to master process
	HOST = 'localhost'
	PORT = 50008
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	with open('zero', 'rb') as file:
		times = []
		data = file.read()
		for i in range(50):
			start_time = datetime.datetime.now()
			conn.sendall(data)
			conn.recv(1)
			end_time = datetime.datetime.now()
			times.append(float((end_time-start_time).total_seconds()))
	conn.close()
	avg = float(combine(times))
	s.sendall((str(addr[0])+": "+str(avg)).encode())
	print(str(addr)+": "+str(avg))

def be_server():
	HOST = 'localhost'
	PORT = 50007
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	i = 0
	while True:
		s.listen(5)
		conn, addr = s.accept()
		t = Thread(target=send_data, args=(i,addr,conn))
		t.start()

def recieve_data(i, HOST, PORT):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	for i in range(50):
		l = 0
		while l < 25600:
			data = s.recv(25600)
			l += sys.getsizeof(data)
		s.sendall(b'a')
	s.close()

def be_client(num):
	HOSTS = ['localhost']
	PORT = 50007
	t = Thread(target=recieve_data, args=(0,HOSTS[0],PORT))
	t.start()

if int(args.role) > 1:
	be_server()
else:
	be_client(int(args.role))
