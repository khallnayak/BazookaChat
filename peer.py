from Node import Peer
import socket as s
import threading as th
import json
import sys
import time
import random
from tkinter import *
import encrypt as e
import getipv6



alias,link=sys.argv[1:]

dec=e.MYcrypt()
link=dec.decrypt(link,0,sep='m')

print("*"*50+"\n"+"*"*50+"\n"+"\t\tTHIS CHAT IS POWERED BY BAZOOKA\n"+"*"*50+"\n"+"*"*50+"\n")
print("MADE BY khallnayak\n\n\n")
#HOST=s.gethostbyname(s.gethostname())
HOST=getipv6.HOST


P=s.socket(s.AF_INET6,s.SOCK_DGRAM)
P.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
P.bind((HOST,6970))

peer_obj=Peer()





class Msg():
	def __init__(self):
		self.inp_data=""

obj=Msg()


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





new_thread=th.Thread(target=gui)
new_thread.start()



def inter_peer(seeder_chain,soc,i,ip):
	print(seeder_chain,ip,"IN INTER_PEER",sep="\t")
	ip=tuple(ip)
	"""
	SECURITY CHECKING AND PEER AUTHENTICATION
	"""
	try:
		soc.sendto(json.dumps(peer_obj.number).encode(),ip)
		data,ip=soc.recvfrom(1024)
	except:
		print("Error connecting to peer",ip)
	
	msg=b"DORA RORA RORA"
	# while True:
	# 	try:
	# 		soc.sendto(msg,ip)
	# 		print(soc.recvfrom(1024),"FROM CHOTU "+str(i),sep="\t")
	# 	except OSError as e:
	# 		print("THREAD ERROR OCCURED",e)
	# 		break
	"""
	THE BELOW IS ROUGH FOR INTER-PEER COMMUNICATION
	IGNORE IT
	"""
	while True:
		try:
			"""
			GET TOTAL BLOCKS NUMBER
			"""
			number=10
			required_blocks=set(range(number)).difference(seeder_chain["Data"])
			req=random.choice(required_blocks)

			soc.sendto(str(req).encode(),ip)

			seeder_chain["Data"].append(req)

			data,_=soc.recvfrom(1024)
			data=data.decode()
			"""
			Data will contain block number
			"""
			while data!="OVERIDA".encode():
				try:
					data,_=soc.recvfrom(1024)
				except:
					print("FIle recv error. Fix SHIT")
			"""
			LOAD FILE INTO VARIABLE
			"""
			file=b"DORA RARA RARA"
			#ctr=int(len(block)/1024)+1

			"""
			FURTHER PART OF CHECKING THE BLOCK TRANSFERS
			history=[False]*ctr
			After a block has successfully transfered to the peer, history[block_number]=True
			If error happens the history can be used to resend the block
			"""
			
			req_block=soc.recvfrom(1024).decode()
			"""
			LOAD REQUESTED BLOCK INTO VARIABLE
			"""

			for i in range(100):
				try:
					soc.sendto(file,ip)
				except:
					"""ADD ERROR SHIT"""
					pass
			try:
				soc.sendto(b"OVERIDA",ip)
			except:
				"""ADD ERROR SHIT"""
				pass

			

		
			# while ctr!=0:
			# 	"""
			# 	LOAD BLOCK INTO VARIABLE
			# 	"""
			# 	block=file
			# 	try:
			# 		soc.sendto(block,ip)
			# 	except:
			# 		"""
			# 		ADDING THE ERROR AND INDEX OF ERROR BlOCK IN HISTORY
			# 		"""
			# 		pass
		except OSError as e:
			print("INTER PEER ERROR SHIT",e)

def process_chain(chain,soc):
	chain,ip_table=chain["CHAIN"],chain["IP_TABLE"]
	for i in map(str,range(peer_obj.number+1,peer_obj.size+1)):
		if(i not in peer_obj.fellow_peer.keys() and chain[i]['Vac']!=-1):
			peer_obj.fellow_peer[i]=[]
			peer_obj.fellow_peer[i].append(s.socket(s.AF_INET6,s.SOCK_DGRAM))
			peer_obj.fellow_peer[i][-1].setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
			peer_obj.fellow_peer[i].append(th.Thread(target=inter_peer,args=(chain[i],peer_obj.fellow_peer[i][0],i,ip_table[int(i)-1],)))
			peer_obj.fellow_peer[i][-1].start()





def seeder(S,ip,number):
	#print("INSIDE SEEDER THREAD",ip,number,sep='\t')
	msg=b"NanDeMoNay"
	"""
	SECURITY CHECKING AND PRIVATE/PUBIC KEY TRANSFER
	"""
	S.sendto("I AM HERE!".encode(),ip)
	size,_=S.recvfrom(1024)
	#print(size,"SIZE")
	size=json.loads(size)
	peer_obj.update_data(size,number)
	chain,_=S.recvfrom(1024)
	chain=json.loads(chain.decode())
	peer_obj.seeder_chain["CHAIN"],peer_obj.seeder_chain["IP_TABLE"]=json.loads(chain[0]),json.loads(chain[1])
	S.sendto(str(alias).encode(),ip)
	other_alias,_=S.recvfrom(1024)
	other_alias=other_alias.decode()


	#print(peer_obj.seeder_chain,"INITIAL D")
	"""
	RECV LEDGER SHIT
	"""
	t1=time.time()
	ctr=0
	while True:
		try:
			ans,_=S.recvfrom(1024)
			"""
			HERE IF BLOCK TRANSFER IS COMPLETE THEN CHAIN WILL BE UPDATED
			ADD BLOCK CHECKING PROCEDURE
			eg: block_checking(block_recieved)
			"""
			# if(time.time()-t1>=5):
			# 	peer_obj.seeder_chain["CHAIN"][str(peer_obj.number)]['Data'].append(ctr)
			# 	ctr+=1
			# 	t1=time.time()

			if(ans=="CHAIN".encode()):
				S.sendto(json.dumps(peer_obj.seeder_chain["CHAIN"][str(peer_obj.number)]).encode(),ip)
				chain,_=S.recvfrom(2048)
				chain=json.loads(chain.decode())
				peer_obj.seeder_chain["CHAIN"],peer_obj.seeder_chain["IP_TABLE"]=json.loads(chain[0]),json.loads(chain[1])
				#print(peer_obj.seeder_chain,"NEW CHAIN")
				process_chain(peer_obj.seeder_chain,S)
			
			elif(ans!=b"NanDeMoNay"):
				print("[{0}] ".format(other_alias)+ans.decode())

			#IF WANT ACKNOWLEGDMENT CAN BE SENT TO SEEDER FOR THE BLOCK
			#DONE IN ELSE PART BELOW
			
			else:
				if(obj.inp_data!=""):
					print("[SELF] "+obj.inp_data)
					S.sendto(obj.inp_data.encode(),ip)
					obj.inp_data=""
				else:
					S.sendto(msg,ip)
			#time.sleep(0.2)#####REMOVE SLEEP FOR SPEED TESTING
		except OSError as e:
			print(e)

def peer(data,addr,soc):
	"""
	SECURITY CHECKS FOR SEEDER-PEER AUTHENTICATION
	"""
	msg=b"DORA RORA RORA"
	# while True:
	# 	try:
	# 		soc.sendto(msg,addr)
	# 		print(soc.recvfrom(1024))
	# 		time.sleep(1)
	# 	except:
	# 		break
	#######################################################
	while True:
		try:
			req_block=soc.recvfrom(1024).decode()
			"""
			LOAD REQUESTED BLOCK INTO VARIABLE
			"""
			for i in range(100):
				soc.sendto(msg,addr)
			soc.sendto("OVERIDA".encode(),addr)
			"""
			LOAD NUMBER OF BLOCKS
			"""
			number=10
			required_blocks=set(range(number)).difference(peer_obj.seeder_chain[peer_obj.number]["Data"])
			req=random.choice(required_blocks)

			soc.sendto(str(req).encode(),addr)

			peer_obj.seeder_chain[peer_obj.number]["Data"].append(req)

			data,_=soc.recvfrom(1024)
			data=data.decode()
			"""
			Data will contain block number
			"""
			while data!="OVERIDA".encode():
				try:
					data,_=soc.recvfrom(1024)
				except:
					print("FIle recv error. Fix SHIT")



		except:
			break





"""
FIND SEEDER SHIT
"""
Seeder=(link,6969)
seeder_soc=s.socket(s.AF_INET6,s.SOCK_DGRAM)
seeder_soc.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
try:
	P.sendto("Connect".encode(),Seeder)
	data,ip=P.recvfrom(1024)
	data=json.loads(data)
	#print(data,"Seeder answer loaded",type(data))
	while type(data)!=int:
		P.sendto("Connect".encode(),data)
		data,ip=P.recvfrom(1024)
		data=json.loads(data)
	seeder_thread=th.Thread(target=seeder,args=(seeder_soc,ip,data,))
	seeder_thread.start()
	seeder_thread_active=True
except:
	pass
#print("SEEDER DONE")
while True:
	try:
		data,addr=P.recvfrom(1024)
		data=json.loads(data.decode())
		print(data,type(data),sep="\t")
		if(addr not in peer_obj.fellow_peer.keys() and type(data)==int): #### IF INT THEN FELLOW PEER
			"""
			IMPLEMENT PEER_OBJ.FELLOW_PEER SHIT AS DONE ABOVE FOR PEER AND ENABLE COMMUNICATION
			"""
			print("FELLOW_PEER")
			socketo=s.socket(s.AF_INET6,s.SOCK_DGRAM)
			socketo.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
			peer_thread=th.Thread(target=peer,args=(data,addr,socketo,))
			peer_thread.start()
			peer_obj.fellow_peer[data]=[socketo,peer_thread]
		if(addr[0] not in peer_obj.fellow_peer.keys() and type(data)==str):##### IF STR THEN DOWN LEVEL PEER
			print("DOWN LEVEL PEER")

	except OSError as e:
		print(e)
		pass



"""
NOTES FOR FUTURE IMPLEMENTATION


1. Add break statement at the end of except statement in thread
2. Implement seeder part for peer objects
3. Implement peer block transfers for peer-peer connection.
"""