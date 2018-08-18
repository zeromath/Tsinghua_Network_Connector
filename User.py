#Filename : User.py
import hashlib

class User:
    def __init__(self, name = 'YOUR_USER_NAME', password = 'YOUR_PASSWORD'):
	self.user_name = name
	self.user_password = password 

    def u_setUserName(self, newName):
        self.user_name = newName

    def u_setPassword(self, newPassword):
        self.user_password = newPassword

    def u_getNameAndPassword(self):
	#get user name from the input
	self.user_name = str(raw_input("Please input your name : "))
	self.user_password = str(raw_input("Please input your password : "))

    def u_getMD5Password(self):
        return hashlib.md5(self.user_password).hexdigest()

