def formarturl(url,dirpaths,extention,addslash):
	Allurl = []
	if type(extention) == list:
		for e in extention:
			#print(i[0])
			for line in open(dirpaths,encoding='ISO-8859-1'):
				#print(line)
				if line.startswith('/'):
					line = line.split('/')[1]
				if url.endswith('/') == False:
					#print(i)
					if addslash == True:
						Allurl.append(url + '/' +line.strip('\n')+e)
						Allurl.append(url + '/' +line.strip('\n')+'/')
					elif addslash == False:
						Allurl.append(url + '/' +line.strip('\n')+e)
						Allurl.append(url + '/' +line.strip('\n'))
				elif url.endswith('/') == True:
					if addslash == True:
						Allurl.append(url +line.strip('\n')+ e)
						Allurl.append(url +line.strip('\n')+'/')
					elif addslash == False:
						Allurl.append(url +line.strip('\n')+ e)
						Allurl.append(url +line.strip('\n'))
			#print(Allurl)
		return Allurl
	else:
		for line in open(dirpaths,encoding='ISO-8859-1'):
			if line.startswith('/'):
				line = line.split('/')[1]
			if url.endswith('/') == False:
				if addslash == True:
					Allurl.append(url + '/' + line.strip('\n') + '/')
				elif addslash ==False:
					Allurl.append(url +'/'+line.strip('\n'))
					#a = url +'/'+line.strip('\n')
					#return a
				
			elif url.endswith('/') == True:
				if addslash == True:
					Allurl.append(url +line.strip('\n')+'/')
				elif addslash == False:
					Allurl.append(url + line.strip('\n'))
				#Allurl.append(url + line.strip('\n'))
		return Allurl
