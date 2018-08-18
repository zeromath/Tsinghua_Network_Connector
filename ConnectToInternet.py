#!/usr/bin/python
#Filename : ConnectToInternet

import os
import time
import urllib
import urllib2
import hashlib
import User

class ConnectToInternet(User.User):
	urlLogin  = 'http://net.tsinghua.edu.cn/cgi-bin/do_login'
	urlLogout = 'http://net.tsinghua.edu.cn/cgi-bin/do_logout'
	def __init__(self,name='',password=''):
		if name == '' and password == '':
			User.User.__init__(self)
		else:
			User.User.__init__(self,name,password)

	def CTI_login(self):
		postdata = urllib.urlencode({'username':self.user_name,'password':hashlib.md5(self.user_password).hexdigest(),'drop':'0','type':'1','n':'100'})
		req = urllib2.Request(url = ConnectToInternet.urlLogin, data = postdata)
		result = urllib2.urlopen(req)
		return result.read()
	
	def CTI_logout(self):
		return urllib2.urlopen(ConnectToInternet.urlLogout).read()


#get user name from the input
myCTI = ConnectToInternet()
result =  myCTI.CTI_logout()
if 'logout_ok' in str(result):
	print result
else:
	print myCTI.CTI_login()
