import socket as s
HOST=s.getaddrinfo(s.gethostname(),8080,s.AF_INET6)
HOST=HOST[0][4][0]
