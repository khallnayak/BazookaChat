import socket as s
from getipv6 import HOST

S=s.socket(s.AF_INET6,s.SOCK_DGRAM)
S.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
S.bind((HOST,6969))
print(HOST)

data,addr=S.recvfrom(1024)
print(data.decode())

string=input("Enter the string to send")

print(S.sendto(string.encode(),addr))

print("DONE")
