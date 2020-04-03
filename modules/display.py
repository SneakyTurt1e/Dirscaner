import time
import os
import datetime
import sys
start_time=None
def StartBanner(dirpath,url,thread,timeout,useragent,banlist,Allurl):
	global start_time
	print("+"+"-"*84)
	print("| DirScaner")
	print("| By SneakyTurt1e https://github.com/SneakyTurt1e/")
	print("+"+"-"*84)
	if dirpath:
		print("| Wordlist Path:",os.path.abspath(dirpath))
	else:
		print('| Wordlist Path: Scraper Mod')
	print("| Target Url: ",url) 
	print("| Threads: ",thread)	
	print("| Timeout: %ds"%timeout)
	if useragent:
		print("| User Agent: ",useragent)
	else:
		print("| User Agent: Random")
	print("| Baned Code: " + " ".join(banlist))
	print("| Total requests: ",len(Allurl))
	start_time = datetime.datetime.now()
	print("| Start Time: " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	print("+"+"-"*83+'+')
	'''
	if scraper == False:
		print("| PAGE |" +" "*45+'| SIZE |' +" "*16 +'| CODE |')
	elif scraper == True:
		print("|"+' '*15+"    Note: The result may not be the standard url"+' '*20+"|")
	print('+'+'-'*83+'+')
	'''


def EndBanner():
	endtime = datetime.datetime.now()
	print('+'+'-'*83+'+'+' ')
	print("[+] Scan Finish ")
	print("[+] Time used: %ds"%(endtime - start_time).seconds)
	print("[+] Finish Time: "+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))


def DisplayUrl(requrl,page_size,recode,relocation,nocolor):
	#print(requrl)
	a = 50 - len(requrl)
	b =75 - int(len(requrl)+a+len(str(page_size)))
	c = ' '*40
	if recode.startswith('2') and nocolor == False:
		print("\033[1;32m"+
		'[+] '+requrl + " "*a +str(page_size) + " "*b+recode+
		"\033[0m"+c)
	elif recode.startswith('2') and nocolor ==True:
		print('[+] '+requrl + " "*a +str(page_size) + " "*b+recode+c)


	elif recode.startswith('3') and nocolor == False:
		print("\033[1;33m"+
		'[?] '+requrl + " "*a +str(page_size) + " "*b +recode +' '*5+'--->'+' '*3+relocation+
		"\033[0m"+c)
	elif recode.startswith('3') and nocolor ==True:
		print('[?] '+requrl + " "*a +str(page_size) + " "*b+recode+' '*5+'--->'+' '*3+relocation+c)


	elif recode.startswith('4') and nocolor == False:
		print("\033[1;31m"+
		'[-] '+requrl + " "*a +str(page_size) + " "*b+recode+
		"\033[0m"+c)			
	elif recode.startswith('4') and nocolor == True:
		print('[+] '+requrl + " "*a +str(page_size) + " "*b+recode+c)


def ProgressBar(requrl,counturl,Allurl):
	# time.sleep(1)

	sz = os.get_terminal_size()

	alllen = '[*] [{:.2%}'.format(counturl/len(Allurl)) + '| %d / %d]'%(counturl,len(Allurl))+'  Requesting:%s' %requrl
	barlen = sz.columns - len(alllen) - 1

	allbar = alllen +' '*barlen + '\r'
	sys.stdout.write(allbar)
	sys.stdout.flush()
