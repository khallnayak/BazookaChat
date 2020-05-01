import os

try:
	alias=input("Enter your alias\n")
	assert 1<=len(alias)
	choice=int(input("Enter your choice\n1. Create a room\n2. Join a room\n->"))
	assert choice in [1,2]
	if(choice==1):
		os.system("python3 seeder.py "+str(alias))
	else:
		link=input("Enter link for joining the room\n>>>")
		assert 1<=len(link)
		os.system("python3 peer.py "+str(alias)+' '+str(link))
except KeyboardInterrupt:
	print("HAT BSDK Galat Input")
	
