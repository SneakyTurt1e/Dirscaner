def make_proxies(proxy):
	proxies = dict()
	value = proxy.split(',')
	try:
		for i in value:
			#print(i)
			if i.startswith('http://') or i.startswith('https://'):
				proxies['http'] = i
				proxies['https'] = i
			elif i.startswith('socks5://'):
				proxies['socks5'] = i
	except:
		print('[-] Unsupport proxy type')
	return proxies


def make_cookie(cookie):
    cookies = dict()
    value = cookie.split(',')
    for i in value:
        key, val = i.split(':')
        cookies[key] = val
    return cookies
