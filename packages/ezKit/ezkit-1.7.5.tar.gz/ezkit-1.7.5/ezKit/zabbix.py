import time
from copy import deepcopy

import requests
from loguru import logger

from . import utils


class Zabbix(object):
    """Zabbix"""

    api: str | None = None
    auth: str | None = None
    debug: bool = False

    def __init__(self, api: str, username: str, password: str, debug: bool = False):
        ''' Initiation '''
        self.api = api
        self.auth = self.login(username=username, password=password)
        self.debug = debug

    def request(
        self,
        method: str,
        params: dict,
        log_prefix: str = '',
        **kwargs
    ) -> dict | None:
        """
        Request API
        """

        try:

            log_prefix += f'[Request]({method})'

            logger.info(f'{log_prefix}......')

            '''
            https://www.zabbix.com/documentation/current/en/manual/api#performing-requests
            The request must have the Content-Type header set to one of these values:
                application/json-rpc, application/json or application/jsonrequest.
            '''
            headers = {'Content-Type': 'application/json-rpc'}

            # https://www.zabbix.com/documentation/6.0/en/manual/api#authentication
            # jsonrpc - the version of the JSON-RPC protocol used by the API; the Zabbix API implements JSON-RPC version 2.0
            # method - the API method being called
            # params - parameters that will be passed to the API method
            # id - an arbitrary identifier of the request (请求标识符, 这里使用UNIX时间戳作为唯一标示)
            # auth - a user authentication token; since we don't have one yet, it's set to null
            data: dict = {
                'jsonrpc': '2.0',
                'method': method,
                'params': params,
                'auth': self.auth,
                'id': int(time.time())
            }

            logger.info(f'{log_prefix}data: {data}') if utils.v_true(self.debug, bool) else next

            response = requests.post(self.api, headers=headers, json=data, timeout=10, **kwargs)

            if response.status_code == 200:
                logger.success(f'{log_prefix}success')
                return response.json()
            else:
                logger.error(f'{log_prefix}failed')
                return None

        except Exception as e:
            logger.error(f'{log_prefix}failed')
            logger.exception(e) if utils.v_true(self.debug, bool) else logger.error(f'{log_prefix}{e}')
            return None

    def login(self, username: str, password: str) -> dict:
        """User Login"""

        try:

            log_prefix = '[Login]'
            logger.info(f'{log_prefix}......')

            response = self.request(
                method='user.login',
                params={'username': username, 'password': password},
                log_prefix=log_prefix
            )

            if utils.v_true(response, dict) and response.get('result'):
                logger.success(f'{log_prefix}success')
                return response['result']
            else:
                logger.error(f'{log_prefix}failed')
                return None

        except Exception as e:
            logger.error(f'{log_prefix}failed')
            logger.exception(e) if utils.v_true(self.debug, bool) else logger.error(f'{log_prefix}{e}')
            return None

    def logout(self) -> bool:
        """User Logout"""

        try:

            log_prefix = '[Logout]'
            logger.info(f'{log_prefix}......')

            response = self.request(method='user.logout', params={}, log_prefix=log_prefix)

            match True:
                case True if utils.v_true(response, dict) and response.get('result'):
                    logger.success(f'{log_prefix}success')
                    return True
                case True if utils.v_true(response, dict) and response.get('error'):
                    logger.error(f"{log_prefix}failed: {response.get('error',{}).get('data')}")
                    return False
                case _:
                    logger.error(f"{log_prefix}failed")
                    return False

        except Exception as e:
            logger.error(f'{log_prefix}failed')
            logger.exception(e) if utils.v_true(self.debug, bool) else logger.error(f'{log_prefix}{e}')
            return False

    def logout_and_exit(self):
        '''Logout and Exit'''

        try:
            self.logout()
        except Exception as e:
            logger.exception(e)
        finally:
            exit()

    def get_ids_by_template_name(self, name: str) -> list | None:
        '''
        Get ids by template name

            name: string/array
            example: 'Linux by Zabbix agent' / ['Linux by Zabbix agent', 'Linux by Zabbix agent active']

            如果 name 为 '' (空), 返回所有 template id
        '''

        try:
            response = self.request('template.get', {'output': 'templateid', 'filter': {'name': name}})
            if utils.v_true(response, dict) and utils.v_true(response['result'], list):
                return [i['templateid'] for i in response['result']]
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return None

    def get_ids_by_hostgroup_name(self, name: str) -> list | None:
        '''
        Get ids by hostgroup name

            name: string/array
            example: 'Linux servers' / ['Linux servers', 'Discovered hosts']

            如果 name 为 '' (空), 返回所有 hostgroup id
        '''

        try:
            response = self.request('hostgroup.get', {'output': 'groupid', 'filter': {'name': name}})
            if utils.v_true(response, dict) and utils.v_true(response.get('result'), list):
                return [i['groupid'] for i in response['result']]
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return None

    def get_hosts_by_template_name(self, name: str, output: str = 'extend', **kwargs) -> list | None:
        '''
        Get hosts by template name

            name: string/array
            example: 'Linux by Zabbix agent' / ['Linux by Zabbix agent', 'Linux by Zabbix agent active']

            如果 name 为 '' (空), 返回所有 host
        '''
        try:
            response = self.request('template.get', {'output': ['templateid'], 'filter': {'host': name}})
            if utils.v_true(response, dict) and utils.v_true(response.get('result'), list):
                ids = [i['templateid'] for i in response['result']]
                hosts = self.request('host.get', {'output': output, 'templateids': ids, **kwargs})
                if utils.v_true(hosts, dict) and utils.v_true(hosts.get('result', []), list):
                    return hosts['result']
                else:
                    return None
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return None

    def get_hosts_by_hostgroup_name(self, name: str, output: str = 'extend', **kwargs) -> list | None:
        '''
        Get hosts by hostgroup name

            name: string/array
            example: 'Linux servers' / ['Linux servers', 'Discovered hosts']

            如果 name 为 '' (空), 返回所有 hosts
        '''
        try:
            ids = self.get_ids_by_hostgroup_name(name)
            if ids == []:
                return None
            hosts = self.request('host.get', {'output': output, 'groupids': ids, **kwargs})
            if utils.v_true(hosts, dict) and utils.v_true(hosts.get('result', []), list):
                return hosts['result']
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return None

    def get_interface_by_host_id(self, hostid: str, output: str = 'extend') -> list | None:
        '''
        Get interface by host id

            hostids: string/array
            example: '10792' / ['10792', '10793']
        '''

        try:
            response = self.request('hostinterface.get', {'output': output, 'hostids': hostid})
            if utils.v_true(response, dict) and utils.v_true(response.get('result'), list):
                return response['result']
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return None

    def available_hosts(self, hosts: list = []) -> tuple | None:
        '''可用服务器'''
        try:

            # 可用服务器, 不可用服务器
            available_hosts, unavailable_hosts = [], []

            # 服务器排查
            for host in hosts:
                if host['interfaces'][0]['available'] != '1':
                    unavailable_hosts.append(host['name'])
                else:
                    available_hosts.append(host)

            return available_hosts, unavailable_hosts

        except Exception as e:
            logger.exception(e)
            return None

    def get_history_by_item_key(
        self,
        hosts: list,
        time_from: int = 0,
        time_till: int = 0,
        item_key: str = '',
        data_type: int = 3
    ) -> list | None:
        '''
        1. 根据 item key 获取 item id, 通过 item id 获取 history
        2. 根据 host 的 item id 和 history 的 item id 将数据提取为一个 history list
        3. 根据 history list 中的 clock 排序, 然后将 history list 整合到 host 中
        4. 返回包含有 item key, item id 和 history list 的 host 的 host list

        通过 Item Key 获取 Item history

            hosts: 主机列表
            time_from: 开始时间
            time_till: 结束时间
            item_key: Item Key
            data_type: 数据类型

        参考文档:

            https://www.zabbix.com/documentation/6.0/en/manual/api/reference/history/get

        history

            0 - numeric float
            1 - character
            2 - log
            3 - numeric unsigned
            4 - text

            Default: 3

        默认数据类型是 numeric unsigned (整数), 如果 history.get 返回的数据为 None, 有可能是 data_type 类型不对
        '''

        try:

            match True:
                case True if not utils.v_true(hosts, list):
                    logger.error('ERROR!! hosts is not list or none')
                    return None
                case True if not utils.v_true(time_from, int):
                    logger.error('ERROR!! time_from is not integer or zero')
                    return None
                case True if not utils.v_true(time_till, int):
                    logger.error('ERROR!! time_till is not integer or zero')
                    return None
                case True if not utils.v_true(item_key, str):
                    logger.error('ERROR!! item_key is not string or none')
                    return None

            # 初始化变量
            # item_ids 获取历史数据时使用
            # item_history 历史数据集合, 最后返回
            item_ids: list = []
            item_history: list = []

            '''
            Deep Copy (拷贝数据)
            父函数的变量是 list 或者 dict 类型, 父函数将变量传递个子函数, 如果子函数对变量数据进行了修改, 那么父函数的变量的数据也会被修改
            为了避免出现这种问题, 可以使用 Deep Copy 拷贝一份数据, 避免子函数修改父函数的变量的数据
            '''
            hosts = deepcopy(hosts)

            # --------------------------------------------------------------------------------------

            # Get Item
            hostids = [i['hostid'] for i in hosts]
            item_params = {
                'output': ['name', 'itemid', 'hostid'],
                'hostids': hostids,
                'filter': {'key_': item_key}
            }
            items = self.request('item.get', item_params)

            # --------------------------------------------------------------------------------------

            # 因为 history 获取的顺序是乱的, 为了使输出和 hosts 列表顺序一致, 将 Item ID 追加到 hosts, 然后遍历 hosts 列表输出
            if utils.v_true(items, dict) and utils.v_true(items.get('result'), list):
                for host in hosts:
                    item: dict = next((item_object for item_object in items['result'] if host['hostid'] == item_object['hostid']), '')
                    if utils.v_true(item, dict) and item.get('itemid') != None:
                        host['itemkey'] = item_key
                        host['itemid'] = item['itemid']
                        item_ids.append(item['itemid'])
                        item_history.append(host)
            else:
                logger.error(f'ERROR!! item key {item_key} not find')
                return None

            # 如果 ID 列表为空, 则返回 None
            if not utils.v_true(item_ids, list):
                logger.error(f'ERROR!! item key {item_key} not find')
                return None

            # --------------------------------------------------------------------------------------

            # Get History
            history_params = {
                'output': 'extend',
                'history': data_type,
                'itemids': item_ids,
                'time_from': time_from,
                'time_till': time_till
            }
            history = self.request('history.get', history_params)

            # --------------------------------------------------------------------------------------------------

            if utils.v_true(history, dict) and utils.v_true(history.get('result'), list):

                for item in item_history:
                    # 根据 itemid 提取数据
                    item_history_data = [history_result for history_result in history['result'] if item['itemid'] == history_result['itemid']]
                    # 根据 clock 排序
                    item_history_data = utils.list_dict_sorted_by_key(item_history_data, 'clock')
                    # 整合数据
                    item['history'] = item_history_data

                return item_history

            else:

                logger.error('ERROR!! item history not find')
                return None

        except Exception as e:
            logger.exception(e)
            return None

    def get_history_by_interface(
        self,
        hosts: list,
        interfaces: list,
        time_from: int = 0,
        time_till: int = 0,
        direction: str = ''
    ) -> list | None:
        '''获取网卡历史数据'''

        try:

            match True:
                case True if not utils.v_true(hosts, list):
                    logger.error('ERROR!! hosts is not list or none')
                    return None
                case True if not utils.v_true(interfaces, list):
                    logger.error('ERROR!! interfaces is not list or none')
                    return None
                case True if not utils.v_true(time_from, int):
                    logger.error('ERROR!! time_from is not integer or zero')
                    return None
                case True if not utils.v_true(time_till, int):
                    logger.error('ERROR!! time_till is not integer or zero')
                    return None
                case True if not utils.v_true(direction, str):
                    logger.error('ERROR!! direction is not string or none')
                    return None

            # 创建一个只有 网卡名称 的 列表
            interfaces_names: set = set(interface['interface'] for interface in interfaces)

            # 创建一个 Key 为 网卡名称 的 dictionary
            interfaces_dict: dict = {key: [] for key in interfaces_names}

            # 汇集 相同网卡名称 的 IP
            for interface in interfaces:
                interfaces_dict[interface['interface']].append(interface['host'])

            # 获取历史数据
            history: list = []
            for key, value in interfaces_dict.items():
                hosts_by_ip = [host for v in value for host in hosts if v == host['interfaces'][0]['ip']]
                history += self.get_history_by_item_key(
                    hosts=hosts_by_ip,
                    time_from=time_from,
                    time_till=time_till,
                    item_key=f'net.if.{direction}["{key}"]',
                    data_type=3
                )

            # 根据 name 排序
            history = utils.list_dict_sorted_by_key(history, 'name')

            return history

        except Exception as e:
            logger.exception(e)
            return None

    def get_ips_by_hostgroup_name(self, hostgroup_name: str) -> list:
        try:
            hosts = self.get_hosts_by_hostgroup_name(hostgroup_name)
            if utils.v_true(hosts, utils.NoneType):
                return None
            hostids = [i['hostid'] for i in hosts]
            hostinterface = self.request(method='hostinterface.get', params={'hostids': hostids})
            return [i['ip'] for i in hostinterface.get('result', [])]
        except Exception as e:
            logger.exception(e)
            return None

    def create_object(
        self,
        ips: list,
        item: dict | None = None,
        trigger: dict | None = None,
        graph: bool | dict = False
    ) -> bool:
        """
        创建对象

            ips: IP列表

            item: 

                name
                key_

            trigger:

                description
                expression (必须包含 {host}, 用于定义HOST)
        """
        """
        参考文档:

            https://www.zabbix.com/documentation/6.0/en/manual/api/reference/item/object
            https://www.zabbix.com/documentation/6.0/en/manual/config/items/itemtypes/zabbix_agent
            https://www.zabbix.com/documentation/6.0/en/manual/api/reference/trigger/object

        type:

            0 - Zabbix agent
            2 - Zabbix trapper
            3 - Simple check
            5 - Zabbix internal
            7 - Zabbix agent (active)
            9 - Web item
            10 - External check
            11 - Database monitor
            12 - IPMI agent
            13 - SSH agent
            14 - Telnet agent
            15 - Calculated
            16 - JMX agent
            17 - SNMP trap
            18 - Dependent item
            19 - HTTP agent
            20 - SNMP agent
            21 - Script

        value_type:

            0 - numeric float
            1 - character
            2 - log
            3 - numeric unsigned
            4 - text
        
        priority (integer): Severity of the trigger

            0 - (default) not classified
            1 - information
            2 - warning
            3 - average
            4 - high
            5 - disaster
        """

        try:

            logger.info('mission running')

            match True:
                case True if not utils.v_true(ips, list):
                    logger.error('ERROR!! ips is not list')
                    return False
                case _:
                    next

            for ip in ips:

                # Host Object

                log_prefix = 'get host object'

                logger.info(f'{log_prefix} ......')

                response = self.request('hostinterface.get', {'filter': {'ip': ip}, 'selectHosts': ['host']})

                logger.warning(f'{log_prefix} hostinterface: {response}') if utils.v_true(self.debug, bool) else next

                match True:
                    case True if utils.v_true(response, dict) and utils.v_true(response.get('result'), list):
                        logger.success(f"{log_prefix} success: {response['result'][0]['hosts'][0]['host']}")
                    case True if utils.v_true(response, dict) and response.get('error'):
                        logger.error(f"{log_prefix} error: {response.get('error', {}).get('data')}")
                        continue
                    case True if utils.v_true(response, utils.NoneType):
                        logger.error(f"{log_prefix} error: {response.get('error', {}).get('data')}")
                        continue
                    case _:
                        logger.error(f"{log_prefix} error: {ip}")
                        continue

                host = response['result'][0]['hosts'][0]['host']
                host_id = response['result'][0]['hostid']
                interface_id = response['result'][0]['interfaceid']

                # ----------------------------------------------------------------------------------

                # Create Item

                if utils.v_true(item, dict):

                    log_prefix = 'create item'

                    logger.info(f'{log_prefix} ......')

                    params = {
                        # 'name': None,
                        # 'key_': None,
                        'hostid': host_id,
                        'type': 7,
                        'value_type': 3,
                        'interfaceid': interface_id,
                        'delay': '1m',
                        'history': '7d',
                        'trends': '7d'
                    } | item

                    response = self.request('item.create', params)

                    logger.warning(f'{log_prefix} response: {response}') if utils.v_true(self.debug, bool) else next

                    match True:
                        case True if utils.v_true(response, dict) and response.get('result'):
                            logger.success(f"{log_prefix} success: {response.get('result')}")
                        case True if utils.v_true(response, dict) and response.get('error'):
                            logger.error(f"{log_prefix} error: {response.get('error', {}).get('data')}")
                            continue
                        case True if utils.v_true(response, utils.NoneType):
                            logger.error(f"{log_prefix} error: {response.get('error', {}).get('data')}")
                            continue
                        case _:
                            logger.error(f"{log_prefix} error: {item.get('name')}")
                            continue

                    item_id = response['result']['itemids'][0]

                # ----------------------------------------------------------------------------------

                # Create Trigger

                if utils.v_true(trigger, dict):

                    log_prefix = 'create trigger'

                    logger.info(f'{log_prefix} ......')

                    params = {
                        # 'description': None,
                        'priority': '2',
                        # 'expression': None,
                        'manual_close': '1'
                    } | trigger

                    # Trigger 的 expression 需要指定 HOST, 例如:
                    #   'last(/DIYCL-110-30/system.uptime)<10m'
                    # DIYCL-110-30 就是 HOST
                    # 但是 HOST 是根据 IP 调用接口获取的, 所以可以写成动态的配置
                    #   'last(/{host}/system.uptime)<10m'.format(host='DIYCL-110-30')
                    # 所以, 传递参数的时候, expression 中就必须要有 {host}, 用于定义 HOST
                    # 如果传递参数的时候使用了 f-strings, 要保留 {host}, 再套一层 {} 即可
                    #   f'last(/{{host}}/system.uptime)<10m'
                    params['expression'] = f"{params['expression']}".format(host=host)

                    # 注意: create trigger 的 params 的类型是 list
                    response = self.request('trigger.create', [params])

                    logger.warning(f'{log_prefix} response: {response}') if utils.v_true(self.debug, bool) else next

                    match True:
                        case True if utils.v_true(response, dict) and response.get('result'):
                            logger.success(f"{log_prefix} success: {response.get('result')}")
                        case True if utils.v_true(response, dict) and response.get('error'):
                            logger.error(f"{log_prefix} error: {response.get('error', {}).get('data')}")
                            continue
                        case True if utils.v_true(response, utils.NoneType):
                            logger.error(f"{log_prefix} error: {response.get('error', {}).get('data')}")
                            continue
                        case _:
                            logger.error(f"{log_prefix} error: {trigger.get('name')}")
                            continue

                # ----------------------------------------------------------------------------------

                # Create Graph

                if utils.v_true(graph, bool) or utils.v_true(graph, dict):

                    log_prefix = 'create graph'

                    logger.info(f'{log_prefix} ......')

                    # Graph object:
                    #
                    #   https://www.zabbix.com/documentation/current/en/manual/api/reference/graph/object
                    #
                    # yaxismax (float) The fixed maximum value for the Y axis.
                    #   Default: 100.
                    # yaxismin (float) The fixed minimum value for the Y axis.
                    #   Default: 0.
                    # ymax_type (integer) Maximum value calculation method for the Y axis.
                    #   Possible values:
                    #   0 - (default) calculated;
                    #   1 - fixed;
                    #   2 - item.
                    # ymin_type (integer) Minimum value calculation method for the Y axis.
                    #   Possible values:
                    #   0 - (default) calculated;
                    #   1 - fixed;
                    #   2 - item.
                    #
                    # 'ymin_type': 2,
                    # 'ymin_itemid':item_id,
                    # 'ymax_type': 2,
                    # 'ymax_itemid':item_id,
                    params: dict = {
                        'name': item.get('name'),
                        'width': 900,
                        'height': 200,
                        'gitems': [{'itemid': item_id, 'color': '0040FF'}]
                    }

                    if utils.v_true(graph, dict):

                        params = params | graph

                        if utils.v_true(params.get('gitems'), list):
                            for gitem in params.get('gitems'):
                                if utils.v_true(gitem, dict) and gitem.get('itemid') == '{}':
                                    gitem['itemid'] = item_id

                    response = self.request('graph.create', params)

                    logger.warning(f'{log_prefix} response: {response}') if utils.v_true(self.debug, bool) else next

                    match True:
                        case True if utils.v_true(response, dict) and response.get('result'):
                            logger.success(f"{log_prefix} success: {response.get('result')}")
                        case True if utils.v_true(response, dict) and response.get('error'):
                            logger.error(f"{log_prefix} error: {response.get('error', {}).get('data')}")
                            continue
                        case True if utils.v_true(response, utils.NoneType):
                            logger.error(f"{log_prefix} error: {response.get('error', {}).get('data')}")
                            continue
                        case _:
                            logger.error(f"{log_prefix} error: {params.get('name')}")
                            continue

                # ----------------------------------------------------------------------------------

            return True

        except Exception as e:
            logger.exception(e) if utils.v_true(self.debug, bool) else logger.error(e)
            return False
        finally:
            logger.success('mission completed')
