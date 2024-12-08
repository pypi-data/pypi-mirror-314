from lark import Lark
from sms import SMS
from voice import Voice
import json
from dotenv import dotenv_values


class Notice:
    lark_: Lark
    sms_: SMS
    voice_: Voice
    mobile_num: str
    voice_content: str

    def __init__(self, env_file_path: str):
        dict = dotenv_values(dotenv_path=env_file_path)
        print(f'notice env loaded. {dict}')
        self.mobile_num = dict['mobile_num']
        self.voice_content = dict['voice_content']

        if 'bot_webhook_url' in dict:
            bot_webhook_url = dict['bot_webhook_url']
            self.lark_ = Lark(webhook_url=bot_webhook_url)

        if 'sms_access_key_id' in dict and 'sms_access_key_secret' in dict:
            sms_access_key_id = dict['sms_access_key_id']
            sms_access_key_secret = dict['sms_access_key_secret']
            self.sms_ = SMS(access_key_id=sms_access_key_id,
                            access_key_secret=sms_access_key_secret)

        if 'voice_account' in dict and 'voice_password' in dict:
            voice_account = dict['voice_account']
            voice_password = dict['voice_password']
            self.voice_ = Voice(account=voice_account, password=voice_password)

    def send_lark(self, msg: str):
        return self.lark_.send(msg=msg)

    def send_lark_and_voice(self, msg: str, voice_first: bool = True):
        msg = '【电话消息】 ' + msg
        if voice_first:
            voice_resp = self.voice_.send(mobile_num=self.mobile_num,
                                          content=self.voice_content)
            lark_resp = self.lark_.send(msg=msg)
        else:
            lark_resp = self.lark_.send(msg=msg)
            voice_resp = self.voice_.send(mobile_num=self.mobile_num,
                                          content=self.voice_content)
        resp = {}
        if lark_resp is not None:
            resp['lark_resp'] = lark_resp
        if voice_resp is not None:
            resp['voice_resp'] = voice_resp
        if len(resp) > 0:
            return json.dumps(resp)
        return None


if __name__ == '__main__':
    notice_ = Notice(env_file_path='/xxx/.env')
    notice_.send_lark_and_voice(msg='just a test', voice_first=True)
