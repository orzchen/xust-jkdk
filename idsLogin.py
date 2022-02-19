# 这个类用来实现统一身份认证登录 主要就是为了获取token
import requests
import json
import time
import datetime
import pytz
import execjs
import re
from lxml import etree
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
	'Host': 'ids.xust.edu.cn',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
	'Accept-Encoding': 'gzip, deflate',
	'Connection': 'close',
	'Origin': 'http://ids.xust.edu.cn',
	'Referer': 'http://ids.xust.edu.cn/authserver/login?service=https%3A%2F%2Fehallnew.xust.edu.cn%2Fossh_server%2Fcaslogin',
	'Upgrade-Insecure-Requests': '1'
}


class IDSLogin(object):
	"""docstring for IDSLogin"""
	def __init__(self):
		super(IDSLogin, self).__init__()
		self.service = 'https://ehallnew.xust.edu.cn/ossh_server/caslogin' # 需要认证的服务 https
		self.ids_url = 'http://ids.xust.edu.cn/authserver/login?service=' # 认证地址
		self.Session = None
		self.JSESSIONID = None 
		self.TOKEN = None

	# 首次获取用户session
	def getSession(self):
		r = requests.get(self.ids_url+self.service, headers=headers)
		session = ''
		language = 'org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=zh_CN;'
		session += language
		for key, value in r.cookies.items():
			s = key + '=' + value + ';'
			session += s
		return session

	# 解析页面的参数
	def getPageParam(self):
		r = requests.get(self.ids_url+self.service, headers=headers)
		html = r.content
		doc = etree.HTML(html)

		params = dict()
		params['lt'] = doc.xpath('//*[@id="casLoginForm"]/input[1]/@value')[0]
		params['dllt'] = doc.xpath('//*[@id="casLoginForm"]/input[2]/@value')[0]
		params['execution'] = doc.xpath('//*[@id="casLoginForm"]/input[3]/@value')[0]
		params['_eventId'] = doc.xpath('//*[@id="casLoginForm"]/input[4]/@value')[0]
		params['rmShown'] = doc.xpath('//*[@id="casLoginForm"]/input[5]/@value')[0]
		params['pwdDefaultEncryptSalt'] = doc.xpath('//*[@id="pwdDefaultEncryptSalt"]/@value')[0]

		return params

	# 调用js文件加密
	def JSencryptAES(self, password, pwdDefaultEncryptSalt):
		with open('encryptAES.js', 'r', encoding='utf-8') as f:
			jstext = f.read()
		ctx = execjs.compile(jstext)
		result = ctx.call('encryptAES', password, pwdDefaultEncryptSalt)
		# print(result)
		return result

	# 用户登录1
	def authserviceLogin(self, d):
		r = requests.post(self.ids_url+self.service, headers=headers, data=d, verify=False)
		reditList = r.history #可以看出获取的是一个地址序列
		url302 = reditList[len(reditList)-1].headers["location"]
		return url302

	# 重定向后获取token和JSESSIONID
	def osshServer(self, url):
		headers2 = {
			'Connection': 'keep-alive',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Sec-Fetch-Site': 'cross-site',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-User': '?1',
			'Sec-Fetch-Dest': 'document',
			'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': '"Windows"',
			'Referer': 'http://ids.xust.edu.cn/',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
		}
		r = requests.get(url, headers=headers2, verify=False)
		reditList = r.history #可以看出获取的是一个地址序列

		# 正则匹配
		regex1 = r"\S[^;\s]+(?=;)"
		matches1 = re.search(regex1, reditList[0].headers['Set-Cookie'])
		jsessionid = matches1.group(0)

		regex2 = r"(?<=\?).*(?=\&)"
		matches2 = re.search(regex2, reditList[len(reditList)-1].headers["location"])
		token = matches2.group(0)

		self.JSESSIONID = jsessionid
		self.TOKEN = token

def idsLogin(username, password):
	ids = IDSLogin()

	ids.Session = ids.getSession() # 用户session
	headers['cookie'] = ids.Session
	Params = ids.getPageParam() # 页面参数
	# 构造post请求参数
	pwd = password
	pwdSalt = Params['pwdDefaultEncryptSalt']
	password = ids.JSencryptAES(pwd, pwdSalt)
	data = {
		'username': username,
		'password': password,
		'lt': Params['lt'],
		'dllt': Params['dllt'],
		'execution': Params['execution'],
		'_eventId': Params['_eventId'],
		'rmShown': Params['rmShown']
	}

	url1 = ids.authserviceLogin(data)
	ids.osshServer(url1) 
	return ids
