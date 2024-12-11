## Using the Demo

以下是一个使用 `hupipay_sdk` 的示例代码，展示了如何使用虎皮椒支付SDK进行支付操作：

```python
import json
import time

from hupipay_sdk import hupi_pay

def test_hupi_pay_sdk(fee):
    """
    使用虎皮椒支付SDK进行支付测试。
    
    :param fee: 支付金额（单位：元）
    """
    # 初始化Hupi实例并发起支付请求
    r = hupi_pay.Hupi(
        appid='201906124557',
        appsecret='35e717b331196138a1340e6c4da0b508',
        notify_url='https://demo.cc/paynotify',
        return_url='https://demo.cc/payreturn',
        callback='https://demo.cc',
        headers='https://demo.cc',
        payment_api='https://go.vrmrgame.com/payment/do.html'
    ).Pay(total_fee=fee)

    # 将支付结果转换为格式化的JSON字符串，中文字符不转义
    r = json.dumps(r, indent=4, ensure_ascii=False)
    print(r)

if __name__ == '__main__':
    test_hupi_pay_sdk(fee=0.01)

