from idsLogin import *

stucode = '' # 学号
password = '' # 密码
sct_key = '' # SendKey

user = None
signAccount = None
cookie = None # 这是打卡页面的cookie
lastData = None # 上一次打卡的数据
nowData = None # 本次打卡数据
jkdkurl = 'https://ehallplatform.xust.edu.cn/default/jkdk/mobile/mobJkdkAdd_test.jsp?uid='


def getUserInfo(session, token):
	url = 'https://ehallnew.xust.edu.cn/ossh_server/getUser'
	headers = {
		'Host': 'ehallnew.xust.edu.cn',
		'Connection': 'keep-alive',
		'Content-Length': '0',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'X-Requested-With': 'XMLHttpRequest',
		'sec-ch-ua-mobile': '?0',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
		'token': token,
		'sec-ch-ua-platform': '"Windows"',
		'Origin': 'https://ehallnew.xust.edu.cn',
		'Sec-Fetch-Site': 'same-origin',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Dest': 'empty',
		'Referer': 'https://ehallnew.xust.edu.cn/ossh/',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		'Cookie': session
	}
	r = requests.post(url, headers=headers, verify=False).content
	# print(r.decode('unicode_escape').encode('latin1').decode())
	data = json.loads(r)
	return data

# 获取uid
def getSignAccount():
	global user
	global signAccount
	ids = idsLogin(stucode, password)
	regex = r"(?<=\=).*"
	matches1 = re.search(regex, ids.JSESSIONID)
	matches2 = re.search(regex, ids.TOKEN)
	sessionid = matches1.group(0)
	token = matches2.group(0)

	user = getUserInfo(sessionid, token)
	signAccount = user['data']['user']['signAccount']

# 获取打卡页面的cookie
def getJKDKcookie():
	global user
	global signAccount
	global cookie
	url = 'https://ehallplatform.xust.edu.cn/default/jkdk/mobile/mobJkdkAdd_test.jsp?uid=' + signAccount
	headers = {
		'Connection': 'keep-alive',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Sec-Fetch-Site': 'same-origin',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-User': '?1',
		'Sec-Fetch-Dest': 'document',
		'Referer': url,
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
	}

	r = requests.get(url, headers=headers, verify=False)

	for key, value in r.cookies.items():
			cookie = key + '=' + value

# 获取上一次打卡信息
# 啊，不对，学校的页面的异步注释是//判断是否当天已经打卡 start，但是从办事大厅中的数据来看就是上一次的，业务号procinstid 
def getLastTime():
	global cookie
	global lastData
	url = 'https://ehallplatform.xust.edu.cn/default/jkdk/mobile/com.primeton.eos.jkdk.xkdjkdkbiz.getJkdkRownum.biz.ext?gh=' + stucode
	headers = {
		'Connection': 'keep-alive',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Sec-Fetch-Site': 'none',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-User': '?1',
		'Sec-Fetch-Dest': 'document',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		'Cookie': cookie
	}
	# 改post
	r = requests.get(url, headers=headers, verify=False)
	data = json.loads(r.content)
	lastData = data

def getLastTime2():
	global cookie
	global lastData
	url = 'https://ehallplatform.xust.edu.cn/default/jkdk/mobile/com.primeton.eos.jkdk.xkdjkdkbiz.getJkdkRownum.biz.ext'
	headers = {
		'Host': 'ehallplatform.xust.edu.cn',
		'Connection': 'keep-alive',
		'Content-Length': '20',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
		'Accept': '*/*',
		'Content-Type': 'text/json',
		'X-Requested-With': 'XMLHttpRequest',
		'sec-ch-ua-mobile': '?0',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
		'sec-ch-ua-platform': '"Windows"',
		'Origin': 'https://ehallplatform.xust.edu.cn',
		'Sec-Fetch-Site': 'same-origin',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Dest': 'empty',
		'Referer': 'https://ehallplatform.xust.edu.cn/default/jkdk/mobile/mobJkdkAdd_test.jsp?uid='+signAccount,
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		'Cookie': cookie
	}
	data = json.dumps({"gh":"19408060130"})
	r = requests.post(url, headers=headers, data=data, verify=False)
	data = json.loads(r.content)
	lastData = data

# 构造打卡的数据
def structurData():
	global nowData
	global lastData
	d = lastData['list'][0]
	nowData = {
		"xkdjkdk": {
	        "procinstid": "",
	        "empid": d['EMPID'],
	        "shzt": d['SHZT'],
	        "id": "",
	        "jrrq1": d['JRRQ1'],
	        "sjh2": d['SJH2'],
	        "jrsfzx3": d['JRSFZX3'],
	        "szdd4": d['SZDD4'],
	        "xxdz41": d['XXDZ4_1'],
	        "jrtwfw5": d['JRTWFW5'],
	        "jrsfjgwh6": d['JRSFJGWH6'],
	        "jrsfjghb7": d['JRSFJGHB7'],
	        "jrsfcxfrzz8": d['JRSFCXFRZZ8'],
	        "jrsfywhrjc9": d['JRSFYWHRJC9'],
	        "jrsfyhbrjc10": d['JRSFYHBRJC10'],
	        "jrsfjcgrrq11": d['JRSFJCGRRQ11'],
	        "jssfyqzysgl12": d['JSSFYQZYSGL12'],
	        "sfcyglq13": d['SFCYGLQ13'],
	        "glkssj131": "",
	        "gljssj132": "",
	        "sfyyqxgzz14": d['SFYYQXGZZ14'],
	        "qtxx15": d['QTXX15'],
	        "gh": d['GH'],
	        "xm": d['XM'],
	        "xb": d['XB'],
	        "sfzh": d['SFZH'],
	        "szyx": d['SZYX'],
	        "xydm": d['XYDM'],
	        "zy": d['ZY'],
	        "zydm": d['ZYDM'],
	        "bj": d['BJ'],
	        "bjdm": d['BJDM'],
	        "jg": d['JG'],
	        "yx": d['YX'],
	        "sfxs": d['SFXS'],
	        "xslx": d['XSLX'],
	        "jingdu": d['JINGDU'],
	        "weidu": d['WEIDU'],
	        "guo": "中国",
	        "sheng": d['SHENG'],
	        "shi": d['SHI'],
	        "xian": d['XIAN'],
	        "sfncxaswfx16": d['SFNCXASWFX16'],
	        "dm": d['BJDM'],
	        "jdlx": d['JDLX'],
	        "tbsj": datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),
	        "fcjtgj17Qt": d['FCJTGJ17_QT'],
	        "fcjtgj17": d['FCJTGJ17'],
	        "hqddlx": d['HQDDLX'],
	        "ymtys": d['YMTYS'],
	        "time": datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d'),
    	}
	}


# 打卡提交
def mobJkdk():
	global cookie
	global nowData
	global jkdkurl
	global signAccount
	url = 'https://ehallplatform.xust.edu.cn/default/jkdk/mobile/com.primeton.eos.jkdk.xkdjkdkbiz.jt.biz.ext'
	# 'Content-Length': '940',
	headers = {
		'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/12.0 Mobile/15A372 Safari/604.1',
		'Accept': '*/*',
		'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate',
		'Content-Type': 'text/json',
		'X-Requested-With': 'XMLHttpRequest',
		'Origin': 'https://ehallplatform.xust.edu.cn',
		'Connection': 'close',
		'Referer': jkdkurl+signAccount,
		'Cookie': cookie,
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache'
	}
	# 提交的数据 进行json格式化
	data = json.dumps(nowData)
	# post 
	r = requests.post(url, headers=headers, data=data, verify=False)


# 打卡成功发送通知
def server_chan_push():
	global lastData
	arg = sct_key
	url = "https://sctapi.ftqq.com/{0}.send".format(arg)
	headers = {"Content-type": "application/x-www-form-urlencoded"}

	# 构造查看上一次打卡的链接
	link = "http://ehallplatform.xust.edu.cn:8080/default/jkdk/mobile/JkdkQuery.jsp?procinstId=" + str(lastData['list'][0]['PROCINSTID']) + "&uid=" + signAccount
	nowtime = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
	desp = "# 打卡成功！\n## 填报时间： {0} \n### [查看]({1}) \n#### `通知时间： {2}` \n#### `————自动打卡`".format(lastData['list'][0]['TBSJ'], link, nowtime)

	content = {"title": "西科大健康打卡", "desp": desp, "channel": "9|66"}
	ret = requests.post(url, headers=headers, data=content)
	print("ServerChan: " + ret.text)


def main_handler(event, context):
	getSignAccount()
	getJKDKcookie()
	getLastTime()
	structurData()
	# 提交打卡
	mobJkdk()
	# 再一次获取上一次打卡
	time.sleep(3)
	getLastTime()
	# 推送通知
	server_chan_push()

if __name__ == "__main__":
	main_handler("", "")

