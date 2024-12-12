import json
import time

import requests
from loguru import logger

from . import utils


class QYWX(object):
    """企业微信"""

    """
    企业微信开发者中心

        https://developer.work.weixin.qq.com/
        https://developer.work.weixin.qq.com/document/path/90313 (全局错误码)

    参考文档:

        https://www.gaoyuanqi.cn/python-yingyong-qiyewx/
        https://www.jianshu.com/p/020709b130d3
    """

    url_prefix = 'https://qyapi.weixin.qq.com'
    work_id: str | None = None
    agent_id: str | None = None
    agent_secret: str | None = None
    access_token: str | None = None

    def __init__(self, work_id: str | None, agent_id: str | None, agent_secret: str | None):
        """Initiation"""
        self.work_id = work_id
        self.agent_id = agent_id
        self.agent_secret = agent_secret

        """获取 Token"""
        self.getaccess_token()

    def getaccess_token(self) -> str | None:
        try:
            response = requests.get(f'{self.url_prefix}/cgi-bin/gettoken?corpid={self.work_id}&corpsecret={self.agent_secret}')
            if response.status_code == 200:
                result: dict = response.json()
                self.access_token = result.get('access_token')
            else:
                self.access_token = None
            return result.get('access_token')
        except:
            return None

    def get_agent_list(self) -> dict | str | None:
        try:
            self.getaccess_token() if self.access_token == None else next
            response = requests.get(f'{self.url_prefix}/cgi-bin/agent/list?access_token={self.access_token}')
            if response.status_code == 200:
                response_data: dict = response.json()
                if response_data.get('errcode') == 42001:
                    self.getaccess_token()
                    time.sleep(1)
                    self.get_agent_list()
                return response_data
            return response.text
        except:
            return None

    def get_department_list(self, id) -> dict | str | None:
        try:
            self.getaccess_token() if self.access_token == None else next
            response = requests.get(f'{self.url_prefix}/cgi-bin/department/list?access_token={self.access_token}&id={id}')
            if response.status_code == 200:
                response_data: dict = response.json()
                if response_data.get('errcode') == 42001:
                    self.getaccess_token()
                    time.sleep(1)
                    self.get_department_list(id)
                return response_data
            return response.text
        except:
            return None

    def get_user_list(self, id) -> dict | str | None:
        try:
            self.getaccess_token() if self.access_token == None else next
            response = requests.get(f'{self.url_prefix}/cgi-bin/user/list?access_token={self.access_token}&department_id={id}')
            if response.status_code == 200:
                response_data: dict = response.json()
                if response_data.get('errcode') == 42001:
                    self.getaccess_token()
                    time.sleep(1)
                    self.get_user_list(id)
                return response_data
            return response.text
        except:
            return None

    def get_user_id_by_mobile(self, mobile) -> dict | str | None:
        try:
            self.getaccess_token() if self.access_token == None else next
            json_string = json.dumps({'mobile': mobile})
            response = requests.post(f'{self.url_prefix}/cgi-bin/user/getuserid?access_token={self.access_token}', data=json_string)
            if response.status_code == 200:
                response_data: dict = response.json()
                if response_data.get('errcode') == 42001:
                    self.getaccess_token()
                    time.sleep(1)
                    self.get_user_id_by_mobile(id)
                return response_data
            return response.text
        except:
            return None

    def get_user_info(self, id) -> dict | str | None:
        try:
            self.getaccess_token() if self.access_token == None else next
            response = requests.get(f'{self.url_prefix}/cgi-bin/user/get?access_token={self.access_token}&userid={id}')
            if response.status_code == 200:
                response_data: dict = response.json()
                if response_data.get('errcode') == 42001:
                    self.getaccess_token()
                    time.sleep(1)
                    self.get_user_info(id)
                return response_data
            return response.text
        except:
            return None

    def send_message_by_mobile(self, mobile: str | list, message: str, debug: bool = False) -> bool:
        """发送消息"""
        """
        参考文档:

            https://developer.work.weixin.qq.com/document/path/90235
        """
        try:
            self.getaccess_token() if self.access_token == None else next

            users: list = []

            match True:
                case True if utils.v_true(mobile, list):
                    users = mobile
                case True if utils.v_true(mobile, str):
                    users.append(mobile)
                case _:
                    return None

            for user in users:
                user_object = self.get_user_id_by_mobile(user)
                json_dict = {
                    'touser': user_object.get('userid'),
                    'msgtype': 'text',
                    'agentid': self.agent_id,
                    'text': {'content': message},
                    'safe': 0,
                    'enable_id_trans': 0,
                    'enable_duplicate_check': 0,
                    'duplicate_check_interval': 1800
                }
                json_string = json.dumps(json_dict)
                response = requests.post(f'{self.url_prefix}/cgi-bin/message/send?access_token={self.access_token}', data=json_string)
                if response.status_code == 200:
                    response_data: dict = response.json()
                    if response_data.get('errcode') == 42001:
                        self.getaccess_token()
                        time.sleep(1)
                        self.send_message_by_mobile(mobile, message)

            return True

        except Exception as e:
            logger.exception(e) if utils.v_true(debug, bool) else next
            return False
