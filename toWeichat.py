#!/usr/bin/python
#coding:utf-8
import json,urllib2,sys
errMsg=sys.argv[1]
corpID='你的cropID'
secret='你的密码'
message={
"touser":"@all",
"msgtype":"text",
"agentid":"1",
"text":{
    "content":"Please replace this field"
},
"safe":"0"
}
message['text']['content']=errMsg

getAccessTokenUrl='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid='+corpID+'&corpsecret='+secret
msg = json.dumps(message,ensure_ascii=False)

accessToken = urllib2.urlopen(getAccessTokenUrl)
accessToken = json.loads(accessToken.read())['access_token']

sendMsgUrl='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+accessToken
req = urllib2.Request(sendMsgUrl,msg)
req.add_header('Content-Type','application/json')
response = urllib2.urlopen(req)
response.close()