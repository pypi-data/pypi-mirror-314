import hashlib, time
import requests
from urllib.parse import urlencode, unquote_plus
from random import choice
from string import digits, ascii_letters


def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]


class Hupi(object):
    def __init__(self, appid, appsecret, notify_url, return_url, callback, headers, payment_api):
        """
        :param appid (虎皮椒微信支付appid):
        :param appsecret (虎皮椒支付签名):
        :param notify_url (虎皮椒支付通知地址):
        :param return_url (虎皮椒支付返回地址):
        :param callback (虎皮椒手机支付返回地址):
        :param headers (商户自身主域名):
        :param payment_api (虎皮椒支付api地址):
        """
        self.appid = appid
        self.AppSecret = appsecret
        self.notify_url = notify_url
        self.return_url = return_url
        self.callback_url = callback
        self.headers = headers
        self.paymenty_api = payment_api

    def curl(self, data, url):
        data['hash'] = self.sign(data)
        headers = {"Referer": "%s" % self.headers}
        r = requests.post(url, data=data, headers=headers).json()
        r.update(
            {
                "trade_order_id": data["trade_order_id"]
            }
        )
        return r

    def sign(self, attributes):
        attributes = ksort(attributes)
        m = hashlib.md5()
        m.update((unquote_plus(urlencode(attributes)) + self.AppSecret).encode(encoding='utf-8'))
        sign = m.hexdigest()
        return sign

    def orderID(self):
        order_id = ''.join(choice(digits + ascii_letters) for i in range(20))
        return order_id

    def Pay(self, total_fee):
        url = self.paymenty_api
        data = {
            "version": "1.1",
            "lang": "zh-cn",
            "plugins": "flask",
            "appid": self.appid,
            "trade_order_id": self.orderID(),
            "payment": "WeChat",
            "is_app": "Y",
            "total_fee": total_fee,
            "title": "PullCar Accelerator",
            "description": "",
            "time": str(int(time.time())),
            "notify_url": self.notify_url,
            "return_url": self.return_url,
            "callback_url": self.callback_url,
            "nonce_str": str(int(time.time())),
            "wap_url": self.headers,
            "wap_name": "Member service fee",
            "type": "WAP"
        }

        return self.curl(data, url)
