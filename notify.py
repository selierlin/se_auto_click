import requests
import config

class Notify(object):
    @classmethod
    def sendPushPlus(self, title, content):
        url = 'https://www.pushplus.plus/send'
        body = {"token": config.conf().get('PUSH_PLUS_TOKEN'),
                "title": title,
                "content": content}
        p = requests.post(url, data=body)
        print(p.text)
        pass

    @classmethod
    def sendQywx(self, title, content):
        url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={config.conf().get("QYWX_KEY")}'
        body = {"msgtype": "text",
                "text": {"content": content}}
        p = requests.post(url, json=body)
        print(p.text)
        pass
