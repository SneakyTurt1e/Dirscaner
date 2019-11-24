#!/bin/python3

import argparse
import re
import sys
try:
	import requests
except:
	print("Try 'pip install requests' to install requests")
try:
	from lxml import html
except:
	print("Try 'pip install lxml' to install lxml")
import threading
import random
import queue
import time
import datetime
import os
import re
from useragent.generater import random_UA
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
		if  args.scraper == False:
			url = _dealurl()
			show=_display()
			start = _request()
			#print(random_ua)
			if args.proxies:

				make=_makedict()
				proxies_jar=make.make_proxies(args.proxies)
				#print(proxies_jar)

			if args.cookies:
				make=_makedict()
				cookie_jar=make.make_cookie(args.cookies)
				#print(cookie_jar)
			if args.sslcheck == False:
				import requests.packages.urllib3
				requests.packages.urllib3.disable_warnings()

			url.formarturl(args.url,args.dirpath,args.ext)
			Allurl=list(set(Allurl))


			show.StartBanner()
			start.set_thread()
			show.EndBanner()
			if args.output:
				writeinto()


	#
	# If Scraper active
	#
		elif args.scraper == True:

			show=_display()
			start=_scraper()
			if args.proxies:
				make=_makedict()
				proxies_jar=make.make_proxies(args.proxies)
				#print(proxies_jar)
			if args.cookies:
				make=_makedict()
				cookie_jar=make.make_cookie(args.cookies)
				#print(cookie_jar)
			if args.sslcheck == False:
				import requests.packages.urllib3
				requests.packages.urllib3.disable_warnings()
			show.StartBanner()
			start.screper_req(args.url)
			start.basic_reslo()
			if args.output:
				writeinto()
	except FileNotFoundError:
		print('[-] Wordlist does not exist [no such file or directory]')
	except:
		print('[-] Missing arguments')
		print('[-] Try -h or --help to check the usage')




#
# Brute-force Class
#

# handle url
class _dealurl:
	global Allurl
	def formarturl(self,url,dirpath,ext):
		#global Allurl
		if type(ext) == list:
			for e in ext:
				#print(i[0])
				for line in open(dirpath,encoding='utf-8'):
					#print(line)
					if line.startswith('/'):
						line = line.split('/')[1]
					if url.endswith('/') == False:
						#print(i)
						if args.addslash == True:
							Allurl.append(url + '/' +line.strip('\n')+e)
							Allurl.append(url + '/' +line.strip('\n')+'/')
						elif args.addslash == False:
							Allurl.append(url + '/' +line.strip('\n')+e)
							Allurl.append(url + '/' +line.strip('\n'))
					elif url.endswith('/') == True:
						if args.addslash == True:
							Allurl.append(url +line.strip('\n')+ e)
							Allurl.append(url +line.strip('\n')+'/')
						elif args.addslash == False:
							Allurl.append(url +line.strip('\n')+ e)
							Allurl.append(url +line.strip('\n'))
		else:
			for line in open(dirpath,encoding='utf-8'):
				if line.startswith('/'):
					line = line.split('/')[1]
				if url.endswith('/') == False:
					if args.addslash == True:
						Allurl.append(url + '/' + line.strip('\n') + '/')
					elif args.addslash ==False:
						Allurl.append(url +'/'+line.strip('\n'))
						#a = url +'/'+line.strip('\n')
						#return a
					
				elif url.endswith('/') == True:
					if args.addslash == True:
						Allurl.append(url +line.strip('\n')+'/')
					elif args.addslash == False:
						Allurl.append(url + line.strip('\n'))
					#Allurl.append(url + line.strip('\n'))





# request url
class _request:

	def set_thread(self):
		#print(Allurl)
		threads = []
		#print(args.thread)
		for task in Allurl:
			#print(task)
			q.put(task)
			#print(q.get())
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
			requrl = q.get()
			counturl +=1
			_display.ProgressBar(self,requrl)
			if args.UA:
				user_agent = args.UA
			else:
				user_agent = random_UA()
			try:
				#print(user_agent)
				s = requests.Session()
				s.keep_alive = False
				s.mount('http://', HTTPAdapter(max_retries=args.retimes))
				s.mount('https://', HTTPAdapter(max_retries=args.retimes))      
				response = s.get(requrl, allow_redirects=args.allow_redirect,verify=args.sslcheck,timeout=args.timeout
										,cookies=cookies_jar,proxies=proxies_jar
										,headers={'Connection':'close','User-Agent':user_agent})
				response.keep_alive = False
				#print(self.response)
				self.dealresponse(response,requrl)
			except requests.exceptions.Timeout as timeou_text:
				print('[-] Cannot connect to Host')
			except requests.exceptions.TooManyRedirects as redirec_err:
				print('[-] Too Many Redirects')

			except requests.exceptions.ConnectionError as conerr:
				print("[!] Too Fast..Trying to sleep for few second ..zZZ [ConnectionError]")
				time.sleep(round(random.uniform(3,5),2))
				response = s.get(requrl, allow_redirects=args.allow_redirect,verify=args.sslcheck,timeout=args.timeout
										,cookies=cookies_jar,proxies=proxies_jar
										,headers={'Connection':'close','User-Agent':user_agent})
				response.keep_alive = False
			except urllib3.exceptions.MaxRetryError as retry_err:
				print("[!] Too Fast..Trying to sleep for few second ..zZZ [MaxRetryError]")
				time.sleep(round(random.uniform(3,5),2))
				response = s.get(requrl, allow_redirects=args.allow_redirect,verify=args.sslcheck,timeout=args.timeout
										,cookies=cookies_jar,proxies=proxies_jar
										,headers={'Connection':'close','User-Agent':user_agent})
				response.keep_alive = False
			except urllib3.exceptions.NewConnectionError as new_err:
				print("[!] Too Fast..Trying to sleep for few second ..zZZ [NewConnectionError]")
				time.sleep(round(random.uniform(3,5),2))
				response = s.get(requrl, allow_redirects=args.allow_redirect,verify=args.sslcheck,timeout=args.timeout
										,cookies=cookies_jar,proxies=proxies_jar
										,headers={'Connection':'close','User-Agent':user_agent})
				response.keep_alive = False




	def dealresponse(self,response,requrl):
		#print(requrl)
		global writelist
		relocation = None
		recode=str(response.status_code)
		page_size = len(response.text)

		if recode not in args.banlist and recode.startswith('2'):
			if type(args.size) == list and page_size in args.size:
				None
			else:
				_display._displayUrl(self,requrl,page_size,recode,relocation)
				if args.output:
					writelist.append('[%s]'%recode+' '*3+requrl)

		elif recode not in args.banlist and recode.startswith('3'):
			relocation = response.headers['Location']
			if type(args.size) == list and page_size in args.size:
				None
			else:
				_display._displayUrl(self,requrl,page_size,recode,relocation)
				if args.output:
					writelist.append('[%s]'%recode+' '*3+requrl)

		elif recode not in args.banlist and recode.startswith('4'):
			if type(args.size) == list and page_size in args.size:
				None
			else:
				_display._displayUrl(self,requrl,page_size,recode,relocation)
				if args.output:
					#writeinto(requrl,recode)
					writelist.append('[%s]'%recode+' '*3+requrl)		




# display
class _display:
	#start_time=None
	def StartBanner(self):
		print("+"+"-"*84)
		print("| DirScaner")
		print("| By SneakyTurt1e https://github.com/SneakyTurt1e/")
		print("+"+"-"*84)
		if args.dirpath:
			print("| Wordlist Path:",os.path.abspath(args.dirpath))
		else:
			print('| Wordlist Path: Scraper Mod')
		print("| Target Url: ",args.url) 
		print("| Threads: ",args.thread)	
		print("| Timeout: %ds"%args.timeout)
		if args.UA:
			print("| User Agent: ",args.UA)
		else:
			print("| User Agent: Random")
		print("| Baned Code: " + " ".join(args.banlist))
		print("| Total requests: ",len(Allurl))
		self.start_time = datetime.datetime.now()
		print("| Start Time: " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
		print("+"+"-"*83+'+')
		if args.scraper == False:
			print("| PAGE |" +" "*45+'| SIZE |' +" "*16 +'| CODE |')
		elif args.scraper == True:
			print("|"+' '*15+"    Note: The result may not be the standard url"+' '*20+"|")
		print('+'+'-'*83+'+')


	def EndBanner(self):
		endtime = datetime.datetime.now()
		print('+'+'-'*84+' '*10)
		print("[+] Scan Finish ")
		print("[+] Time used: %ds"%(endtime - self.start_time).seconds)
		print("[+] Finish Time: "+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))


	def _displayUrl(self,requrl,page_size,recode,relocation):
		#print(requrl)
		a = 50 - len(requrl)
		b =75 - int(len(requrl)+a+len(str(page_size)))
		c = ' '*25
		if recode.startswith('2') and args.nocolor == False:
			print("\033[1;32m"+
			'[+] '+requrl + " "*a +str(page_size) + " "*b+recode+
			"\033[0m"+c)
		elif recode.startswith('2') and args.nocolor ==True:
			print('[+] '+requrl + " "*a +str(page_size) + " "*b+recode+c)


		elif recode.startswith('3') and args.nocolor == False:
			print("\033[1;33m"+
			'[?] '+requrl + " "*a +str(page_size) + " "*b +recode +' '*5+'--->'+' '*3+relocation+
			"\033[0m"+c)
		elif recode.startswith('3') and args.nocolor ==True:
			print('[?] '+requrl + " "*a +str(page_size) + " "*b+recode+' '*5+'--->'+' '*3+relocation +c)


		elif recode.startswith('4') and args.nocolor == False:
			print("\033[1;31m"+
			'[-] '+requrl + " "*a +str(page_size) + " "*b+recode+
			"\033[0m" +c)
			
		elif recode.startswith('4') and args.nocolor == True:
			print('[+] '+requrl + " "*a +str(page_size) + " "*b+recode +c)


	def ProgressBar(self,requrl):
		# time.sleep(1)
		#pbar = tqdm(total=len(Allurl))
		a = 50 - len(requrl)
		#time.sleep(0.1)
		print('[*] Requesting:%s'%requrl+' '*a+'[%d / %d]'%(counturl,len(Allurl))+' {:.2%}'.format(counturl/len(Allurl))+' '*25,end="\r")
		#pbar.update(1)



# Convert to dictionary
class _makedict:

	def make_proxies(self,proxy):
		proxies = dict()
		value = proxy.split(',')
		try:
			for i in value:
				if i.startswith('http://'):
					proxies['http'] = i
				elif i.startswith('https://'):
					proxies['https'] = i
				elif i.startswith('socks5://'):
					proxies['http'] = i
					proxies['https'] = i
		except:
			print('[-] Unsupport proxy type')
		return proxies



		# for i in value:
		# 	if i.startswith('http'):
		# 		proxies['http'] = i

		# return proxies




	def make_cookie(self,cookie):
	    cookies = dict()
	    value = cookie.split(',')

	    for i in value:
	        key, val = i.split(':')
	        cookies[key] = val
	    return cookies



#write into file
def writeinto():
	with open(args.output,'w') as f:
		for i in writelist:
			f.write(i+'\n')


#
# Scraper Class
#

class _scraper:
	def screper_req(self,requrl):
		#print('1')
		if args.UA:
			user_agent = args.UA
		else:
			user_agent = random_UA()
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
					writelist.append(i)




_Banner='''
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
	writelist=[]
	counturl=0
	proxies_jar=None
	cookies_jar=None

	q = queue.Queue()
	print(_Banner)

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

	parser.add_argument('--user-agent',dest='UA',help="Request's user agnet [Default Random]",
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
