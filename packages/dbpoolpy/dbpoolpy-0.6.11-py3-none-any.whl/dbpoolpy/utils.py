import time
import traceback
from dbpoolpy.constants import LOG_CONF
from dbpoolpy.config import settings

class DBFunc(object):
    def __init__(self, data):
        self.value = data


def get_printer():
    if settings.LOGGER is not None:
        if hasattr(settings.LOGGER,"info"):
            printer = settings.LOGGER.info
        else:
            printer = settings.LOGGER
    else:
        printer = print
    return printer


def timeit(func):
    def _(*args, **kwargs):
        starttm = time.time()
        ret = 0
        num = 0
        err = ''
        try:
            retval = func(*args, **kwargs)
            if isinstance(retval, list):
                num = len(retval)
            elif isinstance(retval, dict):
                num = 1
            elif isinstance(retval, int):
                ret = retval
            return retval
        except Exception as e:
            err = str(e)
            ret = -1
            raise e
        finally:
            endtm = time.time()
            conn = args[0]
            # dbcf = conn.pool.dbcf
            dbcf = conn.param
            sql = repr(args[1])
            if not LOG_CONF.get('log_allow_print_sql', True):
                sql = '***'

            printer = get_printer()

            printer(
                'server=%s|id=%d|name=%s|user=%s|addr=%s:%d|db=%s|idle=%d|busy=%d|max=%d|trans=%d|time=%d|ret=%s|num=%d|sql=%s|err=%s' % (
                conn.__dbtype__,
                conn.conn_id % 10000,
                conn.name,
                dbcf.get('user', ''),
                dbcf.get('host', ''),
                dbcf.get('port', 0),
                dbcf.get('database', ''),
                len(conn.pool.dbconn_idle),
                len(conn.pool.dbconn_using),
                conn.pool.max_conn,
                conn._transaction,
                int((endtm - starttm) * 1000000),
                str(ret),
                num,
                sql,
                err))
    return _

def timesql(func):
    def _(self, sql, *args, **kwargs):
        printer = get_printer()
        if settings.DEBUG:
            starttm = time.time()
            ret = 0
            num = 0
            err = ''
        try:
            for i in range(settings.RECONNECT_TIMES):
                try:
                    retval = func(self, sql, *args, **kwargs)
                    break
                except (self._engine.InterfaceError,
                        self._engine.InternalError) as e:  # 如果是连接错误
                    """
                    OperationalError:
                        对于与数据库操作相关且不一定在程序员控制下的错误所引发的异常，
                        例如意外断开连接、找不到数据源名称、事务无法处理、处理过程中发生内存分配错误等。
                    InterfaceError:
                        对于与数据库接口而非数据库本身相关的错误引发的异常
                    InternalError:
                        当数据库遇到内部错误时引发的异常，例如游标不再有效、事务不同步等。
                    """
                    if not self._transaction:
                        self.reconnect()
                        continue
                    printer(traceback.format_exc())
                    raise e
                except Exception as e:
                    printer(traceback.format_exc())
                    raise e
            else:
                retval = None
            if settings.DEBUG:
                if isinstance(retval, list):
                    num = len(retval)
                elif isinstance(retval, dict):
                    num = 1
                elif isinstance(retval, int):
                    ret = retval
            return retval
        except Exception as e:
            err = str(e)
            ret = -1
            raise e
        finally:
            if settings.DEBUG:
                endtm = time.time()
                # dbcf = conn.pool.dbcf
                dbcf = self._kwargs
                sql = repr(sql)
                args = repr(args[0]) if args else None
                if not LOG_CONF.get('log_allow_print_sql', True):
                    sql = '***'

                printer(
                    'server=%s|id=%d|name=%s|user=%s|addr=%s:%d|db=%s|idle=%d|busy=%d|max=%d|trans=%d|time=%d|ret=%s|num=%d|sql=%s|args=%s|err=%s' % (
                    self.__dbtype__,
                    self._conn_id % 10000,
                    self._name,
                    dbcf.get('user', ''),
                    dbcf.get('host', ''),
                    dbcf.get('port', 0),
                    dbcf.get('database', ''),
                    len(self.pool._idle_cache),
                    len(self.pool._idle_using),
                    self.pool._maxconnections,
                    1 if self._transaction else 0,
                    int((endtm - starttm) * 1000000),
                    str(ret),
                    num,
                    sql,
                    args,
                    err))
    return _


