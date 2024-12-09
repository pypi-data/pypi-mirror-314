from loguru import logger as log
import sys
from datetime import datetime
import time
import json
import hashlib
import base64
import hmac
import requests

class FeishuRobot(object):
    def __init__(self, webhook: str, secret: str = None) -> None:
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.webhook = webhook
        self.secret = secret
        self.time = str(int(time.time()))

    # 签名校验
    def get_sign(self, timestamp, secret):

        # 拼接timestamp和secret
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        hmac_code = hmac.new(string_to_sign.encode(
            "utf-8"), digestmod=hashlib.sha256).digest()

        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    # 封装 post 请求
    def post(self, data):
        webhook = self.webhook
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        if self.secret != None:
            data['timestamp'] = self.time
            data['sign'] = self.get_sign(secret=self.secret, timestamp=self.time)
        #log.info(data)
        data = json.dumps(data)
        try:
            response = requests.post(webhook, headers=headers, data=data)
        except requests.exceptions.HTTPError as exc:
            log.error("消息发送失败， HTTP error: %d, reason: %s" %
                          (exc.response.status_code, exc.response.reason))
            raise
        except requests.exceptions.ConnectionError:
            log.error("消息发送失败，HTTP connection error!")
            raise
        except requests.exceptions.Timeout:
            log.error("消息发送失败，Timeout error!")
            raise
        except requests.exceptions.RequestException:
            log.error("消息发送失败, Request Exception!")
            raise
        else:
            result = response.json()

            # 发送有错误 返回数据会携带code
            if result.get('code') != 0:
                log.error("消息发送失败，自动通知：%s" % result)
            # 发送成功 返回数据会有StatusCode
            if result.get('StatusCode') == 0:
                log.debug('发送成功')

    def send_text(self, text: str, is_at_all: bool = False) -> None:
        """
        文本类型
        :param text: 消息内容（必须是字符串，如果太长自动折叠）
        :param is_at_all: 是否艾特所有人，默认关闭；False：不艾特所有人；True：艾特所有人（默认加在文字最后面）
        """
        log.info(text)
        if is_at_all:
            text = text+'<at user_id="all">所有人</at> '
        data = {"msg_type": "text", "content": {"text": text}}        
        self.post(data)

    # 发送富文本消息
    def send_post(self, *args, title: str = None):
        """
        富文本类型
        :param *args:接受所有要发送的富文本，按照行数来，每一行都是列表 例如：
            firs_line = [content_text('wwwww'), content_a(
                href='baidu.com', text='百度')]
            second_line = [content_imag(
                'img_ecffc3b9-8f14-400f-a014-05eca1a4310g')]
            send_post(firs_line，second_line)
        :param title 标题，默认没有
        """
        content = []
        for arg in args:
            if type(arg) == list:
                content.append(arg)
        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": content
                    },
                }
            }
        }
        self.post(data)

    # 发送群名片
    def send_share_chat(self, share_chat_id: str):
        """
        分享群名片
        :param share_chat_id:群id 以 oc_开头 例：oc_f5b1a7eb27ae2c7b6adc2a74faf339ff
        """
        data = {
            "msg_type": "share_chat",
            "content": {
                "share_chat_id": share_chat_id
            }
        }
        self.post(data)

    def send_image(self, image_key: str):
        """
        发送图片
        :param image_key:图片key 例如：img_ecffc3b9-8f14-400f-a014-05eca1a4310g 如果想获取image_key 参考 https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create#362449eb
        """
        data = {
            "msg_type": "image",
            "content": {"image_key": image_key}
        }
        self.post(data)

    def send_interactive(self, card):
        """
        消息卡片
        :param card:消息卡片具体构造内容 具体参考文档 https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN （由于消息卡片复杂的逻辑性，暂时无法更好的封装）
        """
        data = {
            "msg_type": "interactive",
            "card": card
        }
        self.post(data)
    
if __name__ == '__main__':
    WEBHOOK_URL = "xx"
    WEBHOOK_SECRET = "xx"

    feishu = FeishuRobot(webhook=WEBHOOK_URL, secret=WEBHOOK_SECRET)

    # 发送文本消息并艾特全体（默认加在文本最后）：
    feishu.send_text(text="text content", is_at_all=True)

    # 发送文本消息不艾特全体(is_at_all=False 可以不写，默认是关闭艾特全体的)：
    feishu.send_text(text="text content", is_at_all=False)

    # # 发送富文本消息
    # # content_text 文本  content_a 超链接 content_image 图片 content_at 艾特某人 title 富文本标题，默认不填
    # # 代表第一行要发送的内容，以列表形式体现
    # first_line = [post.content_text('测试'), post.content_a(
    #     href='baidu.com', text='百度')]
    # # 第二行，以此类推
    # second_line = [post.content_imag(
    #     'img_ecffc3b9-8f14-400f-a014-05eca1a4310g')]

    # feishu.send_post(first_line, second_line,title='测试'))