from alibabacloud_dysmsapi20170525.models import SendSmsRequest
from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi.models import Config
import json


class SMS:
    client: Client

    def __init__(self,
                 access_key_id: str,
                 access_key_secret: str,
                 region_id: str = 'dysmsapi.aliyuncs.com') -> None:
        config = Config(access_key_id=access_key_id,
                        access_key_secret=access_key_secret,
                        region_id=region_id)
        self.client = Client(config=config)

    def send(self, phone_num, sign_name: str, template_code: str,
             params: dict):
        req = SendSmsRequest(phone_numbers=str(phone_num),
                             sign_name=sign_name,
                             template_code=template_code,
                             template_param=json.dumps(params))
        try:
            res = self.client.send_sms(request=req)
            data = res.to_map()
            if data['statusCode'] >= 200 and data['statusCode'] < 300 and data[
                    'body']['Code'] == 'OK':
                return None
            return data['body']['Message']
        except Exception as e:
            return f'{e}'
