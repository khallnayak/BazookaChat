class MYcrypt():
	def encrypt(self,string,offset,sep="\\"):
		try:
			assert len(string)>=1
			output=""
			output+=str(ord(string[0])+offset)+sep
			prev=ord(string[0])
			for i in string[1:]:
				output+=str(ord(i)-prev)+sep
				prev=ord(i)
			return output
		except AssertionError:
			print("Length of string should be greater than 1")
		except OSError as e:
			print(e)
		return None

	def decrypt(self,string,offset,sep="\\"):
		try:
			assert len(string)>=1
			output=""
			string=string.split(sep)
			string=string[:-1]
			output+=chr(int(string[0])-offset)
			constant=int(string[0])-offset
			for i in string[1:]:
				output+=chr(int(i)+constant)
				constant=int(i)+constant
			return output
		except AssertionError:
			print("Length of string should be greater than 1")
		except OSError as e:
			print(e)
		return None