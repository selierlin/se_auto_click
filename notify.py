import requests
import config


class Notify(object):
    @classmethod
    def sendPushPlus(self, title, content):
        if content:

            url = 'https://www.pushplus.plus/send'
            body = {"token": config.get('PUSH_PLUS_TOKEN'),
                    "title": title,
                    "content": content}
            p = requests.post(url, data=body)
            print(p.text)
        else:
            print("发送内容为空")

    @classmethod
    def sendQywx(self, title, content):
        if content:
            url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={config.get("QYWX_KEY")}'
            body = {"msgtype": "text",
                    "text": {"content": content}}
            p = requests.post(url, json=body)
            print(p.text)
        else:
            print("发送内容为空")
