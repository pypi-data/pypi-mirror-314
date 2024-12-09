# coding: utf-8
import time
import random
import threading
import traceback
from contextlib import contextmanager
from dbpoolpy.dbconnect.sqlite3 import SQLite3Connection
from dbpoolpy.dbconnect.mysql import MySQLConnection
from dbpoolpy.dbconnect.postgresql import PostgreSQLConnection
from dbpoolpy.constants import DBTYPE
from dbpoolpy.config import settings
from dbpoolpy.utils import get_printer

dbpool = None

class DBPoolBase(object):
    def acquire(self, name):
        pass

    def release(self, name, conn):
        pass

class DBPool(DBPoolBase):
    def __init__(
            self, name, engine, dbtype=None,
            mincached=1, maxconnections=20, timeout=10,
            *args, **kwargs
        ):
        self._name = name                              # 数据库连接池名称
        self._engine = engine                          # 数据库连接引擎，满足DB API 2.0规范
        self._dbtype = dbtype or settings.DB_TYPE      # 连接池类型
        self._mincached = mincached                    # 连接池最小缓存个数
        self._maxconnections = maxconnections          # 连接池最大连接个数
        self._timeout = timeout                        # 连接不使用状态释放超时时间
        self._args, self._kwargs = args, kwargs        # 数据库连接所传参数
        self._idle_cache = []                          # 数据库缓存连接存储列表
        self._idle_using = []                          # 数据库正在使用连接列表
        self._connection_class = self.conn_cls()       # 数据库连接类
        self._lock = threading.Lock()                  # 线程锁
        self._cond = threading.Condition(self._lock)   # 条件锁
        self.open(self._mincached)
        self.printer = get_printer()

    def conn_cls(self):
        assert self._dbtype in DBTYPE.values(), 'DB_TYPE error'
        if self._dbtype == DBTYPE.MYSQL:
            return MySQLConnection
        elif self._dbtype == DBTYPE.POSTGRESQL:
            return PostgreSQLConnection
        elif self._dbtype == DBTYPE.SQLITE3:
            return SQLite3Connection

    def synchronize(func):
        """获取线程锁"""
        def _(self, *args, **kwargs):
            self._lock.acquire()
            x = None
            try:
                x = func(self, *args, **kwargs)
            finally:
                self._lock.release()
            return x
        return _

    def open(self, n=1):
        """增加新连接"""
        newconns = []
        for i in range(0, n):
            myconn = self._connection_class(
                self._name,
                self._engine,
                time.time(),
                0,
                *self._args,
                **self._kwargs)
            myconn.pool = self
            newconns.append(myconn)
        self._idle_cache += newconns

    def close_all(self):
        """释放所有的数据库连接"""
        allconn = self._idle_cache + self._idle_using
        for c in allconn:
            c.close()
        self._idle_cache = []
        self._idle_using = []


    def clear_timeout(self):
        """释放不使用超时的数据库连接"""
        # self.printer('try clear timeout conn ...')
        now = time.time()
        dels = []
        allconn = len(self._idle_cache) + len(self._idle_using)
        for c in self._idle_cache:
            if allconn == 1:
                break
            if now - c._lasttime > self._timeout:
                dels.append(c)
                allconn -= 1

        if dels:
            self.printer('close timeout db conn:%d' % len(dels))
        for c in dels:
            if c._conn:
                c.close()
            self._idle_cache.remove(c)

    @synchronize
    def acquire(self, timeout=10):
        """从连接池中获取一个连接"""
        start = time.time()
        while len(self._idle_cache) == 0:
            if len(self._idle_cache) + len(self._idle_using) < self._maxconnections:
                self.open()
                continue
            self._cond.wait(timeout)
            if int(time.time() - start) > timeout:
                self.printer('func=acquire|error=no idle connections')
                raise RuntimeError('no idle connections')

        conn = self._idle_cache.pop(0)
        conn.useit()
        self._idle_using.append(conn)

        if random.randint(0, 100) > 80:
            try:
                self.clear_timeout()
            except:
                self.printer(traceback.format_exc())

        return conn

    @synchronize
    def release(self, conn):
        """把数据库连接放回到数据库连接池中"""
        if conn:
            if conn._transaction:
                self.printer('realse close conn use transaction')
                conn.close()
                # conn.connect()

            self._idle_using.remove(conn)
            conn.releaseit()
            if conn._conn:
                self._idle_cache.insert(0, conn)
        self._cond.notify()

    @synchronize
    def alive(self):
        for conn in self._idle_cache:
            conn.alive()

    def size(self):
        """连接池的当前大小"""
        return len(self._idle_cache), len(self._idle_using)

def checkalive(name=None):
    global dbpool
    while True:
        if name is None:
            checknames = dbpool.keys()
        else:
            checknames = [name]
        for k in checknames:
            pool = dbpool[k]
            pool.alive()
        time.sleep(300)


def init_pool(db_conf):
    global dbpool
    if dbpool:
        printer = get_printer()
        printer("too many install db")
        return dbpool
    dbpool = {}
    for name, item in db_conf.items():
        item['name'] = name
        dbp = DBPool(**item)
        dbpool[name] = dbp
    return dbpool


def add_pool(db_conf):
    global dbpool
    dbpool = dbpool or {}
    for name, item in db_conf.items():
        item['name'] = name
        dbp = DBPool(**item)
        dbpool[name] = dbp
    return dbpool


def close_pool(name=None):
    global dbpool
    if dbpool:
        if name:
            for n, dbp in dbpool.items():
                if n == name:
                    dbp.close_all()
                    printer = get_printer()
                    printer("close pool %s" % name)
                    break
            else:
                printer = get_printer()
                printer("no this pool %s" % name)

        else:
            for n, dbp in dbpool.items():
                dbp.close_all()
            dbpool = None
            printer = get_printer()
            printer("close all pool")


def acquire(name, timeout=10):
    global dbpool
    # print("acquire:", name)
    pool = dbpool[name]
    con = pool.acquire(timeout)
    con.name = name
    return con


def release(conn):
    if not conn:
        return
    global dbpool
    pool = dbpool[conn.name]
    return pool.release(conn)


@contextmanager
def connect_without_exception(name):
    conn = None
    try:
        conn = acquire(name)
        yield conn
    except:
        printer = get_printer()
        printer("error=%s", traceback.format_exc())
    finally:
        if conn:
            release(conn)

@contextmanager
def connect_db(name):
    '''出现异常捕获后，关闭连接并抛出异常'''
    conn = None
    try:
        conn = acquire(name)
        yield conn
    except:
        printer = get_printer()
        printer("error=%s" % traceback.format_exc())
        raise
    finally:
        if conn:
            release(conn)

def with_connect_db(name):
    '''数据库连接装饰器,可以用在静态方法和类方法里
    name: 要连接的数据库：可以用tuple和list连接多个数据库
    静态方法：self必传值为None
    '''
    def f(func):
        def _(self, *args, **kwargs):
            assert isinstance(name, str)
            is_class_methed = str(type(self)).startswith("<class '__main__")
            if not is_class_methed and self is not None:
                raise Exception(
                    "with_connect_db在装饰静态方法时，方法调用传值首个必须为None, 而不是%s"
                    % str(self))
            if is_class_methed:
                if hasattr(self, 'dbo') and hasattr(self, 'dbo_name'):
                    if self.dbo_name != name:
                        raise Exception(
                            "不能重复使用with_connect_db连接"
                            "两个不同的数据库(%s,%s)" % self.db_name, name)
                else:
                    self.dbo, self.dbo_name = acquire(name), name
            else:
                self = acquire(name)

            res = None
            try:
                res = func(self, *args, **kwargs)
            except:
                raise Exception(traceback.format_exc())
            finally:
                release(self.db if is_class_methed else self)
                if is_class_methed:
                    self.db = None
                else:
                    self = None
            return res
        return _
    return f

# def with_connect_db(name, errfunc=None, errstr=''):
#     '''数据库连接装饰器,可以用在静态方法和类方法里
#     name: 要连接的数据库：可以用tuple和list连接多个数据库
#     静态方法：self必传值为None
#     '''
#     def f(func):
#         def _(self, *args, **kwargs):
#             multi_db = isinstance(name, (tuple, list))
#             is_class_methed = str(type(self)).startswith("<class '__main__")
#             if not is_class_methed and self is not None:
#                 raise Exception(
#                     "with_connect_db在装饰静态方法时，方法调用传值首个必须为None, 而不是%s"
#                     % str(self))
#             if multi_db:           # 连接多个数据库
#                 dbs = {}
#                 for dbname in name:
#                     dbs[dbname] = acquire(dbname)
#                 if is_class_methed:
#                     self.db = dbs
#                 else:
#                     self = dbs
#             else:
#                 if is_class_methed:
#                     self.db = acquire(name)
#                 else:
#                     self = acquire(name)
#
#             res = None
#             try:
#                 res = func(self, *args, **kwargs)
#             except:
#                 if errfunc:
#                     return getattr(self, errfunc)(error=errstr)
#                 else:
#                     raise Exception(traceback.format_exc())
#             finally:
#                 if multi_db:
#                     dbs = self.db if is_class_methed else self
#                     dbnames = list(dbs.keys())
#                     for dbname in dbnames:
#                         release(dbs.pop(dbname))
#                 else:
#                     release(self.db if is_class_methed else self)
#                 if is_class_methed:
#                     self.db = None
#                 else:
#                     self = None
#             return res
#         return _
#     return f
