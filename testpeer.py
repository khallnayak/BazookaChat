import socket as s
from getipv6 import HOST

S=s.socket(s.AF_INET6,s.SOCK_DGRAM)
S.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)

addr=input("Enter the address")
data=input("Enter the string to send")

S.sendto(data.encode(),(addr,6969))

print(S.recvfrom(1024))