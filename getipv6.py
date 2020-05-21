import subprocess
HOST=subprocess.getoutput("curl -6 icanhazip.com").split()[-1]




"""
import socket as s
temp=s.getaddrinfo(s.gethostname(),8080,s.AF_INET6)
temp=map(lambda x:x[-1][0],temp)
HOST=list(filter(lambda x:x[0:x.index(":")]!='fe80',temp))
HOST=HOST[0]
"""