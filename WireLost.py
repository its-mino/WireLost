import socket
import datetime
import math
import random
import sys
from argparse import ArgumentParser

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

	#prints list, sum, length, and average
	print(lov)
	print(sum(lov))
	print(len(lov))
	print(average)


def be_server():
	HOST = ''   
	PORT = 50007
	times = []
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1)
	conn, addr = s.accept()
	with open('zero', 'rb') as file:
		data = file.read()
		for i in range(50):
			print(i)
			start_time = datetime.datetime.now()
			conn.sendall(data)
			conn.recv(1)
			end_time = datetime.datetime.now()
			times.append((end_time-start_time).total_seconds())
	conn.close()
	combine(times)

def be_client():
	HOST = ''
	PORT = 50007
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	for i in range(50):
		l = 0
		while l < 25600:
			data = s.recv(25600)
			l += sys.getsizeof(data)
		s.sendall(b'a')
	s.close()


if args.role.lower() == 's':
	be_server()
else:
	be_client()
