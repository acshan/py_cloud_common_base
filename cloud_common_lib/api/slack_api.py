# coding:utf-8
import logging
from io import BytesIO
import pycurl
import certifi
from simplejson import JSONEncoder

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SlackAPI:
    def __init__(self, access_token, robot_url):
        self.robot_url = access_token + robot_url

    def post_msg(self, text, emoji=None):
        self.curl_core(text, emoji)

    def curl_core(self, text, emoji=None):
        c = pycurl.Curl()
        c.setopt(pycurl.CAINFO, certifi.where())
        c.setopt(pycurl.URL, self.robot_url)
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
        if isinstance(text, str):
            msg = {
                'text': text,
                'icon_emoji': emoji
            }
        else:
            msg = text
        postfields = JSONEncoder().encode(msg)
        c.setopt(pycurl.POSTFIELDS, postfields)
        b = BytesIO()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.perform()
        logger.info('Message Send: %s', postfields)


if __name__ == '__main__':
    slack_client = SlackAPI()
    list = ['aaa', 'bbb']
    msg = ''
    for item in list:
        msg = msg + item + '\n'
        slack_client.post_msg(msg)
