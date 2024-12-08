import requests
from tenacity import retry, stop_after_attempt, wait_fixed
import json


class Lark:
    webhook_url: str

    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    def send(self, msg: str):
        try:
            self.send_(msg=msg)
        except Exception as e:
            return f'{e}'
        finally:
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def send_(self, msg: str):
        json_data = {
            'msg_type': 'text',
            'content': {
                'text': msg,
            }
        }
        resp = requests.post(url=self.webhook_url, json=json_data)
        resp_data = json.loads(resp.text)
        if resp.status_code >= 200 and resp.status_code < 300:
            if resp_data['StatusCode'] != 0:
                raise ValueError(f'{resp_data["StatusMessage"]}')
        else:
            raise ValueError(f'status_code : {resp.status_code}')
