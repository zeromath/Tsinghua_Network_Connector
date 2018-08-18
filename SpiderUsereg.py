#!/usr/bin/python
# Filename : SpiderUsereg.py
# dig info from usereg.tsinghua.edu.cn

from prettytable import PrettyTable
import urllib
import urllib2
import cookielib
import re
import os
import string
import hashlib
import User

class SpiderUsereg(User.User):
	usage = 0.0
	userOnline = []
	urlLogin = 'http://usereg.tsinghua.edu.cn/do.php'
	urlUserInfo = 'http://usereg.tsinghua.edu.cn/user_info.php'
	urlOnlineUser = 'http://usereg.tsinghua.edu.cn/online_user_ipv4.php'
	patternUserInfo = '<td.?class="maintd">\d{10,15}\(byte\).*?<(\d+\.\d{2})G></td>'
	patternOnlineUser_1 = '<td.*?class="maintd".*?>.*?'
	patternOnlineUser_2 = r'''.*?</td>.*?<td.*?class="maintd".*?>.*?(\d+\.\d+\.\d+\.\d+).*?</td>.*?<td.*?class="maintd".*?>.*?(\d+\.?\d*[BKMB]).*?</td>.*?<td.*?class="maintd".*?>.*?(\d+\.?\d*[BKMG]).*?</td>.*?<td.*?class="maintd".*?>.*?(WEB|WIN32).*?</td>.*?<td.*?class="maintd".*?>.*?(\d+-\d+-\d+.*?\d+:\d+:\d+).*?</td>.*?<input.*?type="button".*?onclick="drop\('\d+\.\d+\.\d+\.\d+','(\w{32})'\);">'''

	def __init__(self,name='',password=''):
		if name =='' and password == '':
			User.User.__init__(self)
		else:
			User.User.__init__(self,name,password)
		self.patternOnlineUser = SpiderUsereg.patternOnlineUser_1+self.user_name+SpiderUsereg.patternOnlineUser_2
		#set cookies
		self.cookie = cookielib.CookieJar()
		#use cookie to build an opener
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
		self.login_successfully = False

	def su_login(self):
		postdata = urllib.urlencode({'action':'login','user_login_name':self.user_name,'user_password':User.User.u_getMD5Password(self)})

		#post the data
		req = urllib2.Request(url = SpiderUsereg.urlLogin,data = postdata)

		result = self.opener.open(req)
		return result.read()

	def su_initLogin(self):
		while True:
			if self.su_login() == 'ok':
				print 'Login successfully'
				self.login_successfully = True
				break
			else:
				print 'Wrong password or user name'
				User.User.u_getNameAndPassword(self)
				self.patternOnlineUser = SpiderUsereg.patternOnlineUser_1+self.user_name+SpiderUsereg.patternOnlineUser_2
		
	def su_getUsage(self):
		#open the page we need
		result = self.opener.open(SpiderUsereg.urlUserInfo)

		items = re.findall(SpiderUsereg.patternUserInfo, result.read(),re.S)

		if len(items)>0: 
			print "You have used " + items[0] + "G"
			SpiderUsereg.usage = float(items[0])
		else:
			print "Something goes wrong"

	def su_getOnlineUser(self):
		return SpiderUsereg.userOnline

	def su_initOnlineUser(self):
		SpiderUsereg.userOnline = [];
		result = self.opener.open(SpiderUsereg.urlOnlineUser)
		items = re.findall(self.patternOnlineUser, result.read(), re.S)
		for i in range(0,len(items)):
			SpiderUsereg.userOnline.append({'IP':items[i][0],'IN':items[i][1],'OUT':items[i][2],'CLIENT':items[i][3],'TIME':items[i][4],'CHECKSUM':items[i][5]})
	#		print SpiderUsereg.userOnline[i]
	
	def su_letOffline(self,index):
		if index >=0 and index < len(SpiderUsereg.userOnline):
			postdata = urllib.urlencode({'action':'drop','user_ip':SpiderUsereg.userOnline[index]['IP'],'checksum':SpiderUsereg.userOnline[index]['CHECKSUM']})
			req = urllib2.Request(url = SpiderUsereg.urlOnlineUser, data = postdata)
			result = self.opener.open(req)
			print result.read()
			del SpiderUsereg.userOnline[index]

def myOutput(mylist):
	x = PrettyTable(["Index", "IP", "IN", "OUT", "CLIENT", "TIME"])
	#x.align["Index"] = "l" # Left align city names
	x.padding_width = 1 # One space between column edges and contents (default)
	for i in range(0,len(mylist)):
		x.add_row([i+1, mylist[i]['IP'], mylist[i]['IN'], mylist[i]['OUT'], mylist[i]['CLIENT'], mylist[i]['TIME']])
	print x

mySpider = SpiderUsereg()
os.system('clear')
mySpider.su_initLogin()
mySpider.su_getUsage()
mySpider.su_initOnlineUser()
print 'You have ',len(mySpider.su_getOnlineUser()),' accounts online'
myOutput(mySpider.su_getOnlineUser())

while True:
	c = str(raw_input('Type the index to get offline\nType \'q\' to quit\n'))
	if c=='q':
		break;
	else:
		mySpider.su_letOffline(int(c)-1)
		myOutput(mySpider.su_getOnlineUser())
