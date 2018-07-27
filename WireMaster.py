import socket

HOST = ''   
PORT = 50008
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
conns = []
while len(conns) < 1:
	s.listen(5)
	conn, addr = s.accept()
	conns.append(conn)
avgs = []
for conn in conns:
	avg = conn.recv(100)
	avgs.append(avg.decode())

for avg in avgs:
	a = avg.split(':')
	print(a[0])
	print(float(a[1].replace(' ', '')))
	