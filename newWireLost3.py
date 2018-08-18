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

def master_thread(avg, role, addr, conn):
	while True:
		for i in range(50):
			l = 0
			while l < 25600:
				data = conn.recv(25600)
				l += sys.getsizeof(data)
			if avg is None:
				conn.sendall(b'a')
			else:
				conn.sendall(str(avg).encode())
	conn.close()

def be_master(role):
	MASTER_HOST = '192.168.2.3'
	avg = None
	if role is 0:
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
		s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s2.connect(('192.168.2.4', 50008))
		s2.sendall(str(avg).encode())

	if role is 1:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((MASTER_HOST, 50009))
		for i in range(50):
			l = 0
			while l < 25600:
				data = s.recv(25600)
				l += sys.getsizeof(data)
			s.sendall(b'a')
		s.close()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('0.0.0.0', 50007))
	while True:
		s.listen(5)
		conn, addr = s.accept()
		t = Thread(target=master_thread, args=(avg, role,addr,conn))
		t.start()

def be_node():
	HOSTS = ['192.168.2.3','192.168.2.4'] #master hosts
	PORT = 50007
	master_length = 0
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOSTS[0], PORT))

	with open('zero', 'rb') as file:
			times = []
			data = file.read()
			for i in range(50):
				start_time = datetime.datetime.now()
				s.sendall(data)
				master_length = s.recv(10)
				end_time = datetime.datetime.now()
				times.append(float((end_time-start_time).total_seconds()))
	s.close()
	avg_to_0 = float(combine(times))
	s.close()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOSTS[1], PORT))

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
	avg_to_1 = float(combine(times))
	s.close()

	position = triangulate(avg_to_0, avg_to_1, master_length)
	print('position: ',position)

if int(args.role) > 1:
	be_node()
else:
	be_master(int(args.role))
