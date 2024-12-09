#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
HOME_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'src/')
sys.path.append(HOME_PATH)
import pymysql
from dbpoolpy import connect_db
from dbpoolpy import Select, Insert, Update, Delete
from dbpoolpy import Table

DATABASE = {
    'imlf':  {
        'engine': pymysql,
        'database': 'imlf',
        'host': '',
        'port': 51000,
        'user': 'atpdev',
        'password': '',
        'charset': 'utf8',
        'maxconnections': 10
    }
}

from dbpoolpy import init_pool, connect_db
from dbpoolpy import settings
settings.DEBUG = True
settings.DB_TYPE = 'mysql'
init_pool(DATABASE)

class GraphsTB(Table):
    __server__ = 'imlf'
    __schema__ = 'imlf'
    __table__ = 'graphs'

class Group(Table):
    __server__ = 'imlf'
    __schema__ = 'imlf'
    __table__ = 'users_group'

def test_update_many():
    Update("imlf", "imlf.users_group").many([{"name":"temp111"},{"name": "temp222"}], [{"id":12},{"id":14}]).execute()

def test_update_many_batch():
    Group.set_batch([{"name":"temp1"},{"name": "temp2"}], [{"id":12},{"id":14}])


def test_update_one():
    Update("imlf", "imlf.users_group").values(name="temp11").where(id=12).execute()

def test_param():
    with connect_db('imlf') as db:
        graphs1 = db.query("select * from graphs where username=%s limit 1", args=("郑水清",))
        graphs2 = db.select("graphs").where(username="郑水清").first()
        print(graphs1)
        print(graphs2)
    graphs3 = Select("imlf", "graphs").where(username="郑水清").first()
    print(graphs3)

def test_table():
    graphs = GraphsTB.find(username='郑水清')
    print(graphs)

def test_table_map():
    ids = GraphsTB.map("id").where(username='郑水清')
    print(ids)

def test_idus():
    # 初始化测试数据
    new_custom = dict(name='test_mysql', mod_id=123, code='print')

    new_custom2 = dict(name='test_mysql', mod_id=1234, code='print2')

    # 增
    new_id = Insert('imlf', 'imlf.custom').values(**new_custom).execute()
    # 查
    new_custom_from_db = Select('imlf', 'imlf.custom').where(id=new_id).first()
    try:
        assert new_custom_from_db['name'] == new_custom['name']
        assert new_custom_from_db['mod_id'] == new_custom['mod_id']
        assert new_custom_from_db['code'] == new_custom['code']

        # 改
        Update('imlf', 'imlf.custom').where(id=new_id).values(**new_custom2).execute()
        # 查
        new_custom2_from_db = Select('imlf', 'imlf.custom').where(id=new_id).first()
        assert new_custom2_from_db['name'] == new_custom2['name']
        assert new_custom2_from_db['mod_id'] == new_custom2['mod_id']
        assert new_custom2_from_db['code'] == new_custom2['code']

        # 删
        Delete('imlf', 'imlf.custom').where(id=new_id).execute()
        new_custom = Select('imlf', 'imlf.custom').where(id=new_id).first()
        assert not new_custom
    except Exception as e:
        Delete('imlf', 'imlf.custom').where(name=new_custom['name'])
        raise e

def test_args():
    # 初始化测试数据
    new_custom = dict(name='test_mysql', mod_id=123, code='print')

    new_custom2 = dict(name='test_mysql', mod_id=1234, code='print2')

    # 增
    with connect_db('imlf') as db:
        new_id = db.insert('custom').values(**new_custom).execute()
    # 查
    with connect_db('imlf') as db:
        new_custom_from_db = db.select('custom').where(id=new_id).first()
    try:
        assert new_custom_from_db['name'] == new_custom['name']
        assert new_custom_from_db['mod_id'] == new_custom['mod_id']
        assert new_custom_from_db['code'] == new_custom['code']

        # 改
        with connect_db('imlf') as db:
            db.update('custom').where(id=new_id).values(**new_custom2).execute()
        # 查
        with connect_db('imlf') as db:
            new_custom2_from_db = db.select('custom').where(id=new_id).first()
            assert new_custom2_from_db['name'] == new_custom2['name']
            assert new_custom2_from_db['mod_id'] == new_custom2['mod_id']
            assert new_custom2_from_db['code'] == new_custom2['code']

        # 删

        with connect_db('imlf') as db:
            db.delete('custom').where(id=new_id).execute()

        with connect_db('imlf') as db:
            new_custom = db.select('custom').where(id=new_id).first()
            assert not new_custom
    except Exception as e:
        Delete('imlf', 'imlf.custom').where(name=new_custom['name'])
        raise e

def test_sql():
    new_custom = dict(name='test_sql', mod_id=20, code='234')
    with connect_db('imlf') as db:
        new_id = db.insert('custom').values(**new_custom).execute()
        sql = db.select('custom').where(name=new_custom['name']).sql()
        print(sql)
        assert sql.startswith('select')
        db.delete('custom').where(id=new_id)

def test_transaction():
    '''测试事务'''
    new_custom = dict(name='test_sql2', mod_id=20, code='234')
    new_custom2 = dict(name='test_sql3', mod_id=22, code='235', add_field='1234')
    with connect_db('imlf') as db:
        try:
            with db.transaction() as db_trans:
                new_id = db_trans.insert('custom').values(**new_custom).execute()
                new_id2 = db_trans.insert('custom').values(**new_custom2).execute()
            new_custom_from_db = db.select('custom').where(id=new_id).first()
            assert new_custom_from_db
        except:
            new_custom_from_db = db.select('custom').where(id=new_id).first()
            assert not new_custom_from_db
        if new_id:
            db.delete('custom').where(id=new_id).execute()
        if new_id2:
            db.delete('custom').where(id=new_id2).execute()


def test_escape():
    '''测试str使用escape来转换成sql可运行的字符串, 主要是使用一些转义字符'''
    try:
        with connect_db('imlf') as db:
            graph_id = 1056
            graph_info = db.select('graphs', where={'id':graph_id}).first()
            new_graph_info = {
                "username": graph_info["username"],
                "name":"测试可删",
                "biz_id": graph_info["biz_id"],
                "biz_type": graph_info["biz_type"],
                "entity_id": graph_info["entity_id"],
                "category": graph_info["category"],
                "data": graph_info["data"],
                "model_status": graph_info["model_status"],
                "desc": graph_info["desc"],
                # "available": graph_info["available"],
                }
            db.insert("graphs").values(**new_graph_info).execute()
            # 验证
            graph_from_db = db.select("graphs").where(name="测试可删").all()
            assert len(graph_from_db) == 1
            pass
    except Exception as e:
        raise e
    finally:
        with connect_db("imlf") as db:
            db.delete("graphs").where(name="测试可删").execute()


def test_query():

    with connect_db('imlf') as db:
        # graphs = db.query("select id, name from graphs where username='郑水清'")
        # graphs = db.query("select id, name from graphs where username=%s", param=('郑水清',))
        # graphs = db.query("select id, name from graphs where id in %s", args=([23266, 23276],))
        # graphs = db.query("select id, name from graphs where id between %s and %s", args=(23260, 23277))
        graphs = db.query("select id, name from graphs where username like %s", args=('%郑水清%', ))
        print(graphs)

def test_select_join():
    '''test select join'''
    with connect_db('imlf') as db:
        join_name = db.select_join('graphs', 'nodes', on={'graphs.id': 'nodes.graph_id'}, where={'nodes.id': 4006})
        print(join_name)

def test_get_one_join():
    '''test select join'''
    with connect_db('imlf') as db:
        join_name = db.get_one_join('graphs', 'nodes', on={'graphs.id': 'nodes.graph_id'}, where={'nodes.id': 4006}, fields='username')
        print(join_name)


def test_multi_connect():
    '''test select'''
    with connect_db('imlf') as db:
        with connect_db('imlf') as db:
            with connect_db('imlf') as db:
                one_graph = db.select('graphs', where={'id': 1020}).first()
    with connect_db('imlf') as db:
        one_graph = db.select('graphs', where={'id': 1020}).first()
    with connect_db('imlf') as db:
        with connect_db('imlf') as db:
            one_graph = db.select('graphs', where={'id': 1020}).first()

def test_select_page():
    '''test page'''
    try:
        with connect_db('imlf') as db:
            page = db.select("graphs").fields("id, name").where(username='郑水清').page(page=3, size=10, isdict=False)
            print(page)
            pass
    except Exception as e:
        print(e)

def test_select_like():
    '''test like'''
    with connect_db('imlf') as db:
        graphs = db.select(
            'graphs',
            where={
                'username': '郑水清',
                'name': ('like', '%默认光伏%'),
                })
        print(graphs)

@with_connect_db('imlf')
def test_with_connect_db(db):
    one_graph = db.select('graphs', where={'id': 1020}).first()
    print(one_graph)

class WithTest():
    @with_connect_db('imlf')
    def test_with_class_method(self):
        one_graph = self.db.select('graphs', where={'id': 1020}).first()
        print(one_graph)

@with_connect_db(['imlf', 'wind'])
def test_with_connect_list_db(db):
    one_graph = db['imlf'].select('graphs', where={'id': 1020}).first()
    print(one_graph)

class WithlistTest():
    @with_connect_db(['imlf', 'wind'])
    def test_with_class_list_method(self):
        one_graph = self.db['imlf'].select('graphs', where={'id': 1020}).first()
        print(one_graph)

@with_connect_db('imlf')
def test_cross_db(db):
    data = db.get('select * from jobs.schedule limit 1')
    with db.connect_cur as cur:
        cur.execute('select * from jobs.schedule')
        data = cur.fetchall()
    print(data)

if __name__ == '__main__':
    # test_query()
    # test_args()
    # test_sql()
    # test_transaction()
    # test_select_one()
    # test_dbo_select()
    # test_select_page()
    # test_select_like()
    # test_with_connect_db(None)
    # WithTest().test_with_class_method()
    # test_cross_db(None)
    # test_escape()
    # test_param()
    # test_table()
    # test_table_map()
    # test_update_many()
    # test_update_one()
    test_update_many_batch()
