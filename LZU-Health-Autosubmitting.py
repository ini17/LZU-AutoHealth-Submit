#!/usr/bin/env python3
#-*-coding:utf-8-*-

# @Python-Version : Python 3.7.2
# @Time    : 2021/01/09 14:08
# @Author  : Harter·Liang
# @FileName: LZU-Health-Autosubmitting.py
# @Software: Auto-Submit For LZU-Health
# @Version: 1.2
# @Description: A little script for submitting-LZU-Health
# @Updates: Add functions getting the tokens and cookies the function need,so that's the real automation
# @Comments: 大家还是最好每天如实填报，毕竟也是学校对我们的关心

import requests
from urllib.parse import quote
from urllib.parse import unquote
import json
from datetime import *
from time import *
from selenium import webdriver
#selenium是必须要安装的，具体的操作请参见互联网

socks = requests.session()

def getSubmit(seqNum,auToken,dailyCookie,cardID,province,city,district,name):
    #进行打卡签到的模块
    subApi = 'http://appservice.lzu.edu.cn/dailyReportAll/api/grtbMrsb/submit'

    subHeaders = {
    'Host': 'appservice.lzu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Android 9.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': str(auToken),#Auth-Token
    'Content-Length': '316',
    'Origin': 'http://appservice.lzu.edu.cn',
    'Connection': 'close',
    'Referer': 'http://appservice.lzu.edu.cn/dailyReportAll/',
    'Cookie': 'iPlanetDirectoryPro='+str(dailyCookie)#Cookie
    }

    payload = 'bh='+str(seqNum)+'&xykh='+str(cardID)+'&twfw=0&sfzx=0&sfgl=0&szsf='+str(province)+'\
            &szds='+str(city)+'&szxq='+str(district)+'&sfcg=0&cgdd=&gldd=&jzyy=\
                &bllb=0&sfjctr=0&jcrysm=&xgjcjlsj=&xgjcjldd=&xgjcjlsm=&zcwd=0.0&zwwd=0.0&wswd=0.0\
                    &sbr='+str(name)+'&sjd='#需要更改的也有序号
    try:
        res = socks.post(url=subApi,headers=subHeaders,data=payload).text

        result = json.loads(res)
        
        daySeq = datetime.now().strftime("%Y-%m-%d")

        if result['code'] == 1:
            #倘若打卡成功，那么返回的code的值为1
            print('[+] Auto Submit Successeed')
            with open(daySeq + '-Result.txt','a+',encoding='utf-8') as f:
                #保存记录
                f.writelines('[+] Current Time:'+str(datetime.now())+' submit successfully\n')
        else:
            print('[+] Auto Submit Failed')
            with open(daySeq + '-Result.txt','a+',encoding='utf-8') as f:
                f.writelines('[+] Current Time:'+str(datetime.now())+' submit failed\n')

    except:
        print('[+] Error Found!')


def getST(dailyCookie):
    #获取能够得到Auth-Token的ST-Token
    stApi = 'http://my.lzu.edu.cn/api/getST'
    
    stHeaders = {
        'Host': 'my.lzu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Android 9.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '30',
        'Origin': 'http://my.lzu.edu.cn',
        'Connection': 'close',
        'Referer': 'http://my.lzu.edu.cn/main',
        'Cookie' : 'iPlanetDirectoryPro='+str(dailyCookie)#Cookie
    }

    stPayload = 'service=http%3A%2F%2F127.0.0.1'
    
    try:
        stRes = socks.post(url=stApi,data=stPayload,headers=stHeaders)
        stDic = json.loads(stRes.text)

        if stDic['state'] == 1:
            #如果成功获取到ST-Token
            print('[+] Successfully getting ST-Token')
            return str(stDic['data'])
        else:
            print('[+] Getting ST-Token Failed')
    except:
        print('[+] Error Getting ST-Token!')

def getAuthToken(stToken,cardID,dailyCookie):
    #用来执行获得Auth-Token的步骤
    auApi = 'http://appservice.lzu.edu.cn/dailyReportAll/api/auth/login?st='+str(stToken)+'&PersonID='+str(cardID)#需要本人的校园卡号和ST-Token
    
    auHeader = {
        'Host': 'appservice.lzu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Android 9.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json; charset=UTF-8',
        'Connection': 'close',
        'Referer': 'http://appservice.lzu.edu.cn/dailyReportAll/',
        'Cookie': 'iPlanetDirectoryPro='+str(dailyCookie)#Cookie
    }

    try:
        auRes = socks.get(url=auApi,headers=auHeader)
        
        auDic = json.loads(auRes.text)

        if auDic['code'] == 1:
            #如果获取Auth-Token成功
            print('[+] Successfully getting Au-Token')
            return str(auDic['data']['accessToken'])
        else:
            print('[+] Getting AU-Token Failed')
    except:
        print('[+] Error Getting Au-Token!')

def getSeqMD5(cardID,auToken,dailyCookie):
    #获取校园卡号对应的加密数据
    seqMD5Api = 'http://appservice.lzu.edu.cn/dailyReportAll/api/encryption/getMD5'
    
    seqMD5Header = {
        'Host': 'appservice.lzu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Android 9.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': ''+str(auToken),#此处需要我们之前获得的Auth-Token
        'Content-Length': '19',
        'Origin': 'http://appservice.lzu.edu.cn',
        'Connection': 'close',
        'Referer': 'http://appservice.lzu.edu.cn/dailyReportAll/',
        'Cookie': 'iPlanetDirectoryPro='+str(dailyCookie)#Cookie
    }

    seqMD5Payload = 'cardId='+str(cardID)

    try:
        seqMD5Res = socks.post(url=seqMD5Api,data=seqMD5Payload,headers=seqMD5Header)
        
        seqMD5Dic = json.loads(seqMD5Res.text)
        
        if seqMD5Dic['code'] == 1:
            #如果成功获得了对应的加密数据
            print('[+] Successfully getting card-Enc-MD5')
            return str(seqMD5Dic['data'])
        else:
            print('[+] Getting card-Enc-MD5 Failed')
    except:
        print('[+] Error Getting card-Enc-MD5!')

def getSeqNum(cardID,cardMD5,auToken):
    #获取每一次打卡的序列号
    seqNumApi = 'http://appservice.lzu.edu.cn/dailyReportAll/api/grtbMrsb/getInfo'
    
    seqNumHeader = {
        'Host': 'appservice.lzu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Android 9.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Authorization': str(auToken),#此处需要我们之前获得的Auth-Token
        'Content-Length': '56',
        'Origin': 'http://appservice.lzu.edu.cn',
        'Connection': 'close',
        'Referer': 'http://appservice.lzu.edu.cn/dailyReportAll/'
    }

    seqNumPayload = 'cardId='+str(cardID)+'&md5='+str(cardMD5)

    try:
        seqNumRes = socks.post(url=seqNumApi,headers=seqNumHeader,data=seqNumPayload)
        
        seqNumDic = json.loads(seqNumRes.text)
        
        if seqNumDic['code'] == 1:
            #如果成功获得序列号
            print('[+] Successfully getting Sequence-Number')
            return str(seqNumDic['data']['list'][0]['bh'])
        else:
            print('[+] Getting Sequence-Number Failed')
    except:
        print('[+] Error Getting Sequence-Number')

def getDailyToken(user,password):
    #获取至关重要的Cookie的过程，此处我们模拟使用Chrome浏览器进行登录，然后拿到Cookie
    dayCokApi = 'http://my.lzu.edu.cn/login'
    
    option = webdriver.ChromeOptions()
    # 隐藏窗口
    option.add_argument('headless')
    # 防止打印一些无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])

    option.add_argument('--disable-gpu')
    
    browser = webdriver.Chrome(chrome_options=option)

    browser.get(url=dayCokApi)
    #打开网页
    browser.find_element_by_id('username').send_keys(user)
    #输入用户名
    browser.find_element_by_id('password').send_keys(password)
    #输入密码
    browser.find_element_by_class_name('g-recaptcha').click()
    #模拟登陆的点击

    sleep(1)
    cokList = browser.get_cookies()
    #获取Cookie
    browser.close()
    dayCok = cokList[2]['value']
    #提取我们需要的内容
    
    return dayCok


def submitCard():
    #这部分取决于你自己的校园卡号和信息门户的密码等信息
    card = '320**********'
    passwd = '************'
    province = quote('***')
    city = quote('***')
    district = quote('***')
    name = quote('***')

    dayCok = getDailyToken(card,passwd)
    #先拿到Cookie
    
    testST = getST(dayCok)
    #然后是ST-Token
    
    testAu = getAuthToken(testST,card,dayCok)
    #接下来是Auth-Token
    testMD5 = getSeqMD5(card,testAu,dayCok)
    #再往下是加密数据
    testSeq = getSeqNum(card,testMD5,testAu)
    #最后是每次打卡请求的序列号
    
    getSubmit(testSeq,testAu,dayCok,card,province,city,district,name)
    #进行打卡操作

if __name__ == "__main__":
    submitCard()
    #功能整合