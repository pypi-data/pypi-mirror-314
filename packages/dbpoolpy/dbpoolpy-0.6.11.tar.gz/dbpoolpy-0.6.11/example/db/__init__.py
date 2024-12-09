from dbpoolpy import init_pool, Table

init_pool(DATABASE)

class Server179:
    __server__ = "dbcon1"          # 数据库连接命名

class ImlfDB(Server179):
    __schema__ = "imlf"            # 库名: 和数据库名一样

class AlgoDB(Server179):           # 一个数据库服务下可以有多个数据库
    __schema__ = "imlf"            # 库名: 和数据库名一样

class TableName1TB(ImlfDB, Table):
    __table__ = "table_name1"      # 表名: 和数据库表名一样

class TableName2TB(AlgoDB, Table):
    __table__ = "table_name2"



