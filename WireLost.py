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

def triangulate(AB, BC, AC):
	A = (math.acos(((AC**2 + AB**2) - BC**2)/(2*AC*AB)))
	B = (math.acos(((AB**2 + BC**2) - AC**2)/(2*AB*BC)))
	C = math.radians(180)-(A+B)

	a_loc = (0,0)
	c_loc = (AC,0)

	ac_slope = 0
	bc_slope = math.tan(C)
	ab_slope = -1 * math.tan(A)
	
	x = sympy.Symbol('x')
	Bx = sympy.solve(bc_slope*(x-AC) - ab_slope*(x))
	Bx = Bx[0]
	By = ab_slope * Bx

	return (Bx, By)

def combine(lov):
	lov.sort()
	z = int((round(len(lov)*.25)) - 1)

	for i in range (0,(z)):
	    del lov[i]
	    del lov[(len(lov)-1)-i]
		
	average = float(sum(lov)/len(lov))
	return average

def send_data(i, addr, conn):
	#connect to master process
	HOST = 'localhost'
	PORT = 50008
	master_lengths = None
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	with open('zero', 'rb') as file:
		times = []
		data = file.read()
		for i in range(50):
			start_time = datetime.datetime.now()
			conn.sendall(data)
			length = conn.recv(50)
			if len(length) > 1:
				master_lengths = length
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
		i += 1
		if i > 1:
			i = 0

def recieve_data(i, HOST, PORT, avg):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	for i in range(50):
		l = 0
		while l < 25600:
			data = s.recv(25600)
			l += sys.getsizeof(data)
		if avg is None:
			s.sendall(b'a')
		else:
			s.sendall(str(avg).encode())
	s.close()

def be_client(num):
	MASTER_HOST = ''
	HOSTS = ['']
	PORT = 50007
	avg = None
	if num is 0:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('0.0.0.0', 50009))
		s.listen(1)
		conn, addr = s.accept()
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
	if num is 1:
		recieve_data(i, MASTER_HOST, 50009) 
	t = Thread(target=recieve_data, args=(0,HOSTS[0],PORT,avg))
	t.start()

if int(args.role) > 1:
	be_server()
else:
	be_client(int(args.role))
