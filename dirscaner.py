#!/usr/bin/env python3

import argparse
import re
import sys
try:
	import requests
except:
	print("Try 'pip install requests' to install requests")
	sys.exit()
try:
	from lxml import html
except:
	print("Try 'pip install lxml' to install lxml")
	sys.exit()
import threading
import random
import queue
import re

import urllib3
from modules.generater import random_useragent
from modules.handleurl import formarturl
from modules.display import *
from modules.makedict import *

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



# Main
def main():
	global Allurl
	global proxies_jar
	global cookie_jar	
	try:


	#
	# Brute-force active
	#
		if args.output:
			global f
			f = open(args.output,'w')
		if  args.scraper == False:
			start = request_url()
			#print(random_useragent)
			if args.proxies:
				proxies_jar=make_proxies(args.proxies)
				#print(proxies_jar)
			if args.cookies:
				cookie_jar=make_cookie(args.cookies)
				#print(cookie_jar)
			if args.sslcheck == False:
				import requests.packages.urllib3
				requests.packages.urllib3.disable_warnings()

			Allurl = formarturl(args.url,args.dirpath,args.ext,args.addslash)
			Allurl=list(set(Allurl))
			#print(Allurl)
			StartBanner(args.dirpath,args.url,args.thread,args.timeout,args.useragent,args.banlist,Allurl)
			start.set_thread(Allurl)
			EndBanner()
			if args.output:
				f.close()






	#
	# If Scraper active
	#
		elif args.scraper == True:
			StartBanner(args.dirpath,args.url,args.thread,args.timeout,args.useragent,args.banlist,Allurl)
			start=scraper()
			if args.proxies:
				make=makedict()
				proxies_jar=make.make_proxies(args.proxies)
				#print(proxies_jar)
			if args.cookies:
				make=makedict()
				cookie_jar=make.make_cookie(args.cookies)
				#print(cookie_jar)
			show.Startbanner()
			start.screper_req(args.url)
			start.basic_reslo()
			if args.output:
				f.close()

	except FileNotFoundError:
		print('[-] Wordlist does not exist [no such file or directory]')
	except KeyboardInterrupt:
		print('\n'+'[-] Input interrupt')
		sys.exit()




#
# Brute-force Class
#



# request url
class request_url:
	#print(proxies_jar)
	def set_thread(self,Allurl):
		#print(Allurl)
		threads = []
		for task in Allurl:
			#print(task)
			q.put(task)
		for i in range(int(args.thread)):
			#print(i)
			t = threading.Thread(target=self.requesturl)
			t.start()
			threads.append(t)
		for t in threads:
			t.join()


	def requesturl(self):
		#print(q.get())
		global counturl
		while not q.empty():
			#print(q.get())
			requrl = q.get()
			counturl +=1
			ProgressBar(requrl,counturl,Allurl)
			if args.useragent:
				user_agent = args.useragent
			else:
				user_agent = random_useragent()
			try:
				#print(proxies_jar)
				s = requests.Session()
				s.keep_alive = False
				s.mount('http://', HTTPAdapter(max_retries=args.retimes))
				s.mount('https://', HTTPAdapter(max_retries=args.retimes))      
				response = s.get(requrl, allow_redirects=args.allow_redirect,verify=args.sslcheck,timeout=args.timeout
										,cookies=cookies_jar,proxies=proxies_jar
										,headers={'Connection':'close','User-Agent':user_agent})
				response.keep_alive = False
				self.dealresponse(response,requrl)
			except requests.exceptions.Timeout as timeou_text:
				print('[-] Cannot connect to Host')
			except requests.exceptions.TooManyRedirects as redirec_err:
				print('[-] Too Many Redirects')

			except requests.exceptions.ConnectionError as conerr:
				print("[!] Something Wrong..Trying to sleep for few second ..zZZ [ConnectionError]")
				time.sleep(round(random.uniform(3,5),2))
				response = s.get(requrl, allow_redirects=args.allow_redirect,verify=args.sslcheck,timeout=args.timeout
										,cookies=cookies_jar,proxies=proxies_jar
										,headers={'Connection':'close','User-Agent':user_agent})
				response.keep_alive = False
			except urllib3.exceptions.MaxRetryError as retry_err:
				print("[!] Something Wrong..Trying to sleep for few second ..zZZ [MaxRetryError]")
				time.sleep(round(random.uniform(3,5),2))
				response = s.get(requrl, allow_redirects=args.allow_redirect,verify=args.sslcheck,timeout=args.timeout
										,cookies=cookies_jar,proxies=proxies_jar
										,headers={'Connection':'close','User-Agent':user_agent})
				response.keep_alive = False
			except urllib3.exceptions.NewConnectionError as new_err:
				print("[!] Something Wrong..Trying to sleep for few second ..zZZ [NewConnectionError]")
				time.sleep(round(random.uniform(3,5),2))
				response = s.get(requrl, allow_redirects=args.allow_redirect,verify=args.sslcheck,timeout=args.timeout
										,cookies=cookies_jar,proxies=proxies_jar
										,headers={'Connection':'close','User-Agent':user_agent})
				response.keep_alive = False




	def dealresponse(self,response,requrl):
		#print(requrl)
		global f
		relocation = None
		recode=str(response.status_code)
		page_size = len(response.text)

		if recode not in args.banlist and recode.startswith('2'):
			if type(args.size) == list and page_size in args.size:
				None
			else:
				DisplayUrl(requrl,page_size,recode,relocation,args.nocolor)
				if args.output:
					i = '[%s]'%recode+' '*3+requrl
					f.write(i+'\n')

		elif recode not in args.banlist and recode.startswith('3'):
			relocation = response.headers['Location']
			if type(args.size) == list and page_size in args.size:
				None
			else:
				DisplayUrl(requrl,page_size,recode,relocation,args.nocolor)
				if args.output:
					i = '[%s]'%recode+' '*3+requrl
					f.write(i+'\n')

		elif recode not in args.banlist and recode.startswith('4'):
			if type(args.size) == list and page_size in args.size:
				None
			else:
				DisplayUrl(requrl,page_size,recode,relocation,args.nocolor)
				if args.output:
					i = '[%s]'%recode+' '*3+requrl
					f.write(i+'\n')		

#
# Scraper Class
#

class scraper:
	def screper_req(self,requrl):
		#print('1')
		if args.useragent:
			user_agent = args.useragent
		else:
			user_agent = random_useragent()
		try:
			response = requests.get(requrl, allow_redirects=args.allow_redirect,verify=args.sslcheck,timeout=args.timeout,cookies=cookies_jar,proxies=proxies_jar
											,headers={'Connection':'close','User-Agent':user_agent})
			webpage = html.fromstring(response.content)			
			self.a_href=webpage.xpath('//a/@href')
			self.a_href=list(set(self.a_href))
		except:
			print('Can\'t connect to host...May be due to anti-scraper...')



	def basic_reslo(self):
		for i in self.a_href:
			p = re.compile('[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*')
			if p.match(i) and len(i)>4 :
				#print(i)
				if args.nocolor  == False:
					print("\033[1;32m"+
						'[+] '+i +
						"\033[0m")
				else:
					print('[+] '+i)
				if args.output:
					f.write(i+'\n')





banner='''
______  _       _____                                
|  _  \(_)     /  ___|                               
| | | | _  _ __\ `--.   ___  __ _  _ __    ___  _ __ 
| | | || || '__|`--. \ / __|/ _` || '_ \  / _ \| '__|
| |/ / | || |  /\__/ /| (__| (_| || | | ||  __/| |   
|___/  |_||_|  \____/  \___|\__,_||_| |_| \___||_| 
'''


description = '''
Dirscaner is a tools to brute-force web directories.Also is 
my third simple script.
It supports multi-threading ,filter the response code, 
file extension and page size,customize the cookies and user agent,
Can detect the server through the proxy.
'''



epilog= "More Info: https://github.com/SneakyTurt1e/DirScaner"





if __name__ == "__main__":
	Allurl = []
	f = None
	counturl=0
	proxies_jar=None
	cookies_jar=None
	q = queue.Queue()
	print(banner)

	parser = argparse.ArgumentParser(description=description,epilog=epilog)

	group = parser.add_mutually_exclusive_group()

	parser.add_argument("-u", "--url",dest='url',help="Target Url",type=str,
					metavar='url',required=True)

	group.add_argument('-d',dest='dirpath',help="Wordlist Path",
					metavar='location',required=False)

	parser.add_argument("-o","--output",dest='output',help="Location and name of output file",
					type=str)

	parser.add_argument('-b',dest='banlist',help="Baned response code [Default:Null  e.g:404 302]",
					type=str,metavar='code',nargs='+',default=[])

	parser.add_argument('-e',dest='ext',help="File extension",type=str,
					metavar='ext',nargs='+')

	parser.add_argument('-t',dest='thread',help="Number of thread [Default: 4]",
					type=int,default=4)

	parser.add_argument('-s',dest='size',help="Size filter,will skip pages with these/this size",
					metavar='size',type=int,nargs='+')

	parser.add_argument('--time-out',dest='timeout',help="HTTP Timeout [Default 10]",
					type=int,default=10)

	parser.add_argument('--time-retry',dest='retimes',help="The number of retry attempts when the request fails [Default 6]",
						metavar='time',type=int,default=6)

	parser.add_argument('--user-agent',dest='useragent',help="Request's user agnet [Default Random]",
					type=str)

	parser.add_argument('--no-color',dest='nocolor',help="Turn off color outputs",
					action="store_true",default=False)

	parser.add_argument('--cookie',dest='cookies',help="Your cookies to use in requests [e.g:key1:value1,key2=value2...]",
					default="")

	parser.add_argument('--proxy',dest='proxies',help="Use proxy to request [e.g:http(s)://user:pass@IP:PORT,proxy2...]",
					metavar='Proxy',default="")

	parser.add_argument('--add-slash',dest='addslash',help="Add '/' after each request",
					action="store_true",default=False)

	parser.add_argument('--ssl-check',dest='sslcheck',help="Enable SSL certificate verification",
					action="store_true",default=False)

	parser.add_argument('--allow-re',dest='allow_redirect',help="Follow redirects",
					action="store_true",default=False)	

	group.add_argument('--scraper',dest='scraper',help="Scraper Mod. Scraper all url in <a href>",
					action="store_true",default=False)

	args = parser.parse_args()

	main()
