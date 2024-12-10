'''
Column, Table, MetaData API
    https://docs.sqlalchemy.org/en/14/core/metadata.html#column-table-metadata-api
CursorResult
    https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult
PostgreSQL 14 Data Types
    https://www.postgresql.org/docs/14/datatype.html
'''
import csv

from loguru import logger
from sqlalchemy import Index, create_engine, text

from . import utils


class Database(object):

    engine = create_engine('sqlite://')

    def __init__(self, engine_url=None, engine_options=None):
        '''Initiation'''
        if engine_url != None:
            if utils.v_true(engine_options, dict):
                self.engine = create_engine(engine_url, **engine_options)
            else:
                self.engine = create_engine(engine_url)

    def initializer(self):
        '''ensure the parent proc's database connections are not touched in the new connection pool'''
        self.engine.dispose(close=False)

    def connect_test(self):
        info = '数据库连接测试'
        try:
            logger.info(f'{info}......')
            self.engine.connect()
            logger.success(f'{info}[成功]')
            return True
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.exception(e)
            return False

    def metadata_init(self, base, **kwargs):
        # https://stackoverflow.com/questions/19175311/how-to-create-only-one-table-with-sqlalchemy
        info = '初始化表'
        try:
            logger.info(f'{info}......')
            base.metadata.drop_all(self.engine, **kwargs)
            base.metadata.create_all(self.engine, **kwargs)
            logger.success(f'{info}[成功]')
            return True
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.exception(e)
            return False

    def create_index(self, index_name, table_field):
        # 创建索引
        #   https://stackoverflow.com/a/41254430
        # 示例:
        #   index_name: a_share_list_code_idx1
        #   table_field: Table_a_share_list.code
        info = '创建索引'
        try:
            logger.info(f'{info}')
            idx = Index(index_name, table_field)
            try:
                idx.drop(bind=self.engine)
            except:
                pass
            idx.create(bind=self.engine)
            logger.success(f'{info}[成功]')
            return True
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.error(e)
            return False

    # 私有函数, 保存 execute 的结果到 CSV 文件
    def _result_save(self, file, data, echo=True):
        try:
            outcsv = csv.writer(file)
            outcsv.writerow(data.keys())
            outcsv.writerows(data)
            return True
        except Exception as e:
            logger.exception(e) if echo == True else next
            return False

    def execute(self, sql=None, sql_file=None, sql_file_kwargs=None, csv_file=None, csv_file_kwargs=None, echo=True):
        '''
        echo 是否打印日志
        某些情况下只需要结果, 不需要日志, 将 echo 设置为 False 即可
        '''

        info_prefix = '[执行SQL]'

        # ------------------------------------------------------------

        # 提取 SQL
        # 如果 sql 和 sql_file 同时存在, 优先执行 sql
        sql_object = None
        info = f'{info_prefix}提取SQL'
        try:
            logger.info(f'{info}......') if echo == True else next
            if utils.v_true(sql, str):
                sql_object = sql
            elif utils.v_true(sql_file, str):
                # 判断文件是否存在
                if utils.check_file_type(sql_file, 'file') == False:
                    logger.error(f'文件不存在: {sql_file}') if echo == True else next
                    return False
                # 读取文件内容
                if utils.v_true(sql_file_kwargs, dict):
                    with open(sql_file, 'r', **sql_file_kwargs) as _file:
                        sql_object = _file.read()
                else:
                    with open(sql_file, 'r') as _file:
                        sql_object = _file.read()
            else:
                logger.error(f'{info}[失败]') if echo == True else next
                logger.error(f'{info_prefix}SQL 或 SQL文件 错误') if echo == True else next
                return False
            logger.success(f'{info}[成功]') if echo == True else next
        except Exception as e:
            logger.error(f'{info}[失败]') if echo == True else next
            logger.exception(e) if echo == True else next
            return False

        # ------------------------------------------------------------

        # 执行 SQL
        info = f'{info_prefix}执行SQL'
        try:
            logger.info(f'{info}......') if echo == True else next
            with self.engine.connect() as connect:
                # 执行SQL
                result = connect.execute(text(sql_object))
                if csv_file == None:
                    # 如果 csv_file 没有定义, 则直接返回结果
                    logger.success(f'{info}[成功]') if echo == True else next
                    return result
                else:
                    # 如果 csv_file 有定义, 则保存结果到 csv_file
                    info_of_save = f'{info_prefix}保存结果到文件: {csv_file}'
                    logger.info(f'{info_of_save} .......') if echo == True else next
                    # 保存结果
                    if utils.v_true(csv_file_kwargs, dict):
                        with open(csv_file, 'w', **csv_file_kwargs) as _file:
                            result_of_save = self._result_save(_file, result, echo=echo)
                    else:
                        with open(csv_file, 'w') as _file:
                            result_of_save = self._result_save(_file, result, echo=echo)
                    # 检查保存结果
                    if result_of_save == True:
                        logger.success(f'{info_of_save} [成功]') if echo == True else next
                        logger.success(f'{info}[成功]') if echo == True else next
                        return True
                    else:
                        logger.error(f'{info_of_save} [失败]') if echo == True else next
                        logger.error(f'{info}[失败]') if echo == True else next
                        return False
        except Exception as e:
            logger.error(f'{info}[失败]') if echo == True else next
            logger.exception(e) if echo == True else next
            return False
