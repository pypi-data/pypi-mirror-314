import requests
from tenacity import retry, stop_after_attempt, wait_fixed
import json

voice_url = "http://api.vm.ihuyi.com/webservice/voice.php?method=Submit"
voice_headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/plain"
}


class Voice:

    def __init__(self, account: str, password: str) -> None:
        self.account = account
        self.password = password

    def send(self, mobile_num, content: str, format: str = 'json'):
        try:
            self.send_(mobile_num=mobile_num, content=content, format=format)
        except Exception as e:
            return f'{e}'
        finally:
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def send_(self, mobile_num, content: str, format: str = 'json'):
        data = {
            'account': self.account,
            'password': self.password,
            'mobile': str(mobile_num),
            'content': content,
            'format': format,
        }

        response = requests.post(url=voice_url,
                                 headers=voice_headers,
                                 data=data)
        resp_data = json.loads(response.text)
        if resp_data['code'] != 2:
            raise ValueError(f'{resp_data["msg"]}')
