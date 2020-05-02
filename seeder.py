from Node import Seeder
import socket as s
import threading as th
import json
import time
import sys
from tkinter import *
import encrypt as e
import getipv6

enc=e.MYcrypt()


alias=sys.argv[1]

S=s.socket(s.AF_INET6,s.SOCK_DGRAM)
HOST=getipv6.HOST
S.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
S.bind((HOST,6969))
print("Share this link\n"+enc.encrypt(HOST,0,sep='m'))

print("*"*50+"\n"+"*"*50+"\n"+"\t\tTHIS CHAT IS POWERED BY BAZOOKA\n"+"*"*50+"\n"+"*"*50+"\n")
print("MADE BY khallnayak\n\n\n")
peer_threads={}
inp_data=""

def send_data(text):
	obj.inp_data=text.get("1.0",END)[:-1]
	text.delete("1.0",END)


def gui():
	root=Tk()
	root.geometry("300x50+0+0")
	root.protocol("WM_DELETE_WINDOW",sys.exit)
	root.title("PRESS Ctrl TO SEND")

	text=Text(root,wrap=WORD,font=("Verdana",10))
	text.pack()
	text.bind("<Control_L>",func=lambda x: send_data(text))
	root.mainloop()


new_thread=th.Thread(target=gui,)
new_thread.start()
"""
INIT FILE NAME AND GENERATE BLOCKS WITH LEDGER
ASK FOR TIER SIZE
"""

class Msg():
	def __init__(self):
		self.inp_data=""

obj=Msg()



seeder=Seeder(3)

def refresh(soc,chain,addr):
	try:
		soc.sendto(json.dumps(chain).encode(),addr)
		return True
	except OSError as e:
		return False


def seed(soc,addr):
	#print("In seed")
	msg="NanDeMoNay".encode()
	flag,number=seeder.allocate_number()
	soc.sendto(json.dumps(number).encode(),addr)
	#print(soc)
	if(type(number)==int):
		answer,ans_addr=soc.recvfrom(40)
		#print(answer,ans_addr)
		if(answer):
			seeder.init_connection(addr)
			soc.sendto(json.dumps(seeder.size).encode(),ans_addr)
			flag=refresh(soc,seeder.get_chain(),ans_addr)
			other_alias,_=soc.recvfrom(1024)
			other_alias=other_alias.decode()
			soc.sendto(str(alias).encode(),ans_addr)


			"""
			SEND LEDGER SHIT
			"""
			if(not flag):
				#Something error
				print("FLAG ERROR",flag)
		else:
			soc.close()
			print("NO ANSWER FROM PEER")
			sys.exit()
		time1=time.time()
		while True:
			try:
				if(time.time()-time1>=5):
					soc.sendto("CHAIN".encode(),ans_addr)
					chain,_=soc.recvfrom(2048)
					chain=chain.decode()
					#print(chain,"\t FROM PEER",number)
					seeder.update_chain(chain,number)
					refresh(soc,seeder.get_chain(),ans_addr)
					#print("CHAIN UPDATE")
					time1=time.time()
				else:
					"""
					1. SELECT BLOCK NUMBER AND SEND BLOCK
					2. BLOCK CHECKING ON PEER SIDE
					"""
					if(obj.inp_data!=""):
						print("[SELF] "+obj.inp_data)
						soc.sendto(obj.inp_data.encode(),ans_addr)
						obj.inp_data=""
					else:
						pass
					soc.sendto(msg,ans_addr)
					data,addr=soc.recvfrom(1024)
					if(data!=b"NanDeMoNay"):
						print("[{0}] ".format(other_alias)+data.decode())
				#time.sleep(0.2)
			except OSError as e:
				print(e)
while True:
	thread=[]
	sockets=[]
	try:
		data,addr=S.recvfrom(1024)
		print(data,addr,"IN MAIN",sep="\t")
		if(addr not in peer_threads.keys()):
			sockets.append(s.socket(s.AF_INET6,s.SOCK_DGRAM))
			sockets[-1].setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
			thread.append(th.Thread(target=seed,args=(sockets[-1],addr,)))
			thread[-1].start()
	except KeyboardInterrupt as e:
		break


		
