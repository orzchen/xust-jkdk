## 西安科技大学健康打卡自动脚本

#### 该脚本里的所有接口均来自学校官方的接口

通过模拟登录西科E站进行打卡，打卡成功后通过Server酱进行消息推送

填入你的学号和密码，指的是学校统一服务认证的账号密码，SendKey是Server酱消息推送的key

```python
stucode = '' # 学号
password = '' # 密码
sct_key = '' # SendKey
```

encryptAES.js文件是统一服务认证页面的前端密码加密。

主要文件就是main.py  idsLogin.py encryptAES.js三个，其余的依赖包可以不用，但是环境要有。

依赖包是为了方便部署到腾讯云函数和服务器来定时执行。

云函数部署会有奇奇怪怪的错误，比如cookie错误，但是终端里又是正常的，我解决不了，厚礼谢。

于是我用的服务器，使用[Crontab](https://www.cnblogs.com/dalianpai/p/11813950.html)来做定时任务，环境CentOS7

每天17:30进行打卡，注意在idsLogin.py中66行JSencryptAES函数中，读取encryptAES.js这个文件时文件的路径。

```
30 17 * * * /usr/bin/python3 /xust/main.py
```

