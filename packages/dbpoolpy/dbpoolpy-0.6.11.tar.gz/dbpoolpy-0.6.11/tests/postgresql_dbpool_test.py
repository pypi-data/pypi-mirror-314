#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import traceback
HOME_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'src/')
sys.path.append(HOME_PATH)
try:
    import psycopg2
except:
    psycopg2 = None
from dbpoolpy import connect_db
from dbpoolpy import Select, Insert, Update, Delete

DATABASE = {
    # 'test':  {
    #     'engine': psycopg2,
    #     'database': 'test',
    #     'host': '',
    #     'port': 5432,
    #     'user': 'ap-dev',
    #     'password': '',
    #     # 'charset': 'utf8',
    #     'maxconnections': 10
    # },
    'test2':  {
        'engine': psycopg2,
        'dbtype': 'postgresql',
        'database': 'dev',
        'host': '',
        'port': 5439,
        'user': 'read_only',
        'password': '',
        'maxconnections': 10
    }
}

from dbpoolpy import init_pool, connect_db
from dbpoolpy import settings
settings.DEBUG = True
init_pool(DATABASE)

def test_redshift_in():
     with connect_db('test2') as db:
        thirdpower_data = db.select("ods_forecast.ods_short_forecast_di").where(
            wfid='152901',
            dtime=("between", ['2022-04-01', '2022-05-01']),
            mark='06',
            forecast_source=("in", ["third_ML", "third_XZ", "third_MF"]),
            day_flag = ("in", [1,2,3])
            ).first()
        print(thirdpower_data)

def test_redshift():
    with connect_db('test2') as db:
        graphs = db.query("select * from ods_nwp.ods_nwp_150904 limit 1")
        print(graphs)


def test_query():
    with connect_db('test') as db:
        graphs = db.query("select id, name, address from testcompany limit 1")
        print(graphs)

def test_param():
    with connect_db('test') as db:
        graphs = db.query("select %s, %s, %s from testcompany limit 1", param=('count(id)', 'name', 'address'))
        print(graphs)

def test_select():
    with connect_db('test') as db:
        testcompany=db.select('testcompany').where(id=1).all()
        print(testcompany)

def test_idus():
    # new_id = 107
    # 初始化测试数据
    new_testcompany = dict(name='ttes', age=23, address='beijing', salary=10200)

    new_testcompany2 = dict(name='ttes', age=33, address='shaing', salary=12200)

    # 增
    new = Insert('test', 'testcompany').values(**new_testcompany).other('returning *').execute() # 查
    new_id = new['id']
    new_testcompany_from_db = Select('test', 'testcompany').where(id=new_id).first()
    assert new_testcompany_from_db['name'] == new_testcompany['name']
    assert new_testcompany_from_db['age'] == new_testcompany['age']
    assert new_testcompany_from_db['address'] == new_testcompany['address']
    assert new_testcompany_from_db['salary'] == new_testcompany['salary']

    # 改
    Update('test', 'testcompany').where(id=new_id).values(**new_testcompany2).execute()
    # 查
    new_testcompany2_from_db = Select('test', 'testcompany').where(id=new_id).first()
    assert new_testcompany2_from_db['name'] == new_testcompany2['name']
    assert new_testcompany2_from_db['age'] == new_testcompany2['age']
    assert new_testcompany2_from_db['address'] == new_testcompany2['address']
    assert new_testcompany2_from_db['salary'] == new_testcompany2['salary']
    # 删
    Delete('test', 'testcompany').where(id=new_id).execute()
    new_testcompany = Select('test', 'testcompany').where(id=new_id).first()
    assert not new_testcompany

def test_args():
    test_table = 'testcompany'
    # 初始化测试数据
    new_testcompany = dict(name='ttes', age=23, address='beijing', salary=10200)

    new_testcompany2 = dict(name='ttes', age=33, address='shaing', salary=12200)

    # 增
    with connect_db('test') as db:
        new = db.insert(test_table).values(**new_testcompany).execute()
        new_id = new['id']
    # 查
    with connect_db('test') as db:
        new_testcompany_from_db = db.select(test_table).where(id=new_id).first()
    try:
        assert new_testcompany_from_db['name'] == new_testcompany['name']
        assert new_testcompany_from_db['age'] == new_testcompany['age']
        assert new_testcompany_from_db['address'] == new_testcompany['address']
        assert new_testcompany_from_db['salary'] == new_testcompany['salary']

        # 改
        with connect_db('test') as db:
            db.update(test_table).where(id=new_id).values(**new_testcompany2).execute()
            # 查
            new_testcompany2_from_db = db.select(test_table).where(id=new_id).first()
            assert new_testcompany2_from_db['name'] == new_testcompany2['name']
            assert new_testcompany2_from_db['age'] == new_testcompany2['age']
            assert new_testcompany2_from_db['address'] == new_testcompany2['address']
            assert new_testcompany2_from_db['salary'] == new_testcompany2['salary']
            # 删
            db.delete(test_table).where(id=new_id).execute()
            new_testcompany = db.select(test_table).where(id=new_id).first()
            assert not new_testcompany
    except Exception as e:
        Delete('test', test_table).where(id=new_id)

def test_sql():
    new_testcompany = dict(name='测试sql', age=24, address='ijing', salary=1000)
    test_table = 'testcompany'
    with connect_db('test') as db:
        new_id = db.insert(test_table).values(**new_testcompany).execute()
        sql = db.select(test_table).where(name=new_testcompany['name']).sql()
        print(sql)
        assert sql.startswith('select')
        db.delete(test_table).where(id=new_id)

def test_transaction():
    '''测试事务'''
    test_table = 'testcompany'
    new_testcompany = dict(name='测试transaction', age=24, address='ijing', salary=1000)
    new_testcompany2 = dict(name='测试transactionw', age=242, address='jing', salary=1000, add_field='123')
    with connect_db('test') as db:
        try:
            with db.transaction() as db_trans:
                new_id = db_trans.insert(test_table).values(**new_testcompany).execute()
                new_id2 = db_trans.insert(test_table).values(**new_testcompany2).execute()
            new_testcompany_from_db = db.select(test_table).where(id=new_id['id']).first()
            assert new_testcompany_from_db
        except Exception as e:
            print(traceback.format_exc())
            new_testcompany_from_db = db.select(test_table).where(id=new_id['id']).first()
            assert not new_testcompany_from_db
        if new_id:
            db.delete(test_table).where(id=new_id['id']).execute()

def test_one():
    '''test select'''
    with connect_db('test') as db:
        one_graph = db.select('graphs').first()
        print(one_graph)

def test_get_one():
    '''test get one'''
    with connect_db('test') as db:
        one_graph = db.select('graphs', where={'id': 1020}, fields='name').first()
        print(one_graph)

def test_join():
    '''test select join'''
    with connect_db('test') as db:
        join_name = db.select_join('graphs', 'nodes', on={'graphs.id': 'nodes.graph_id'}, where={'nodes.id': 4006})
        print(join_name)

def test_get_one_join():
    '''test select join'''
    with connect_db('test') as db:
        join_name = db.get_one_join('graphs', 'nodes', on={'graphs.id': 'nodes.graph_id'}, where={'nodes.id': 4006}, fields='username')
        print(join_name)

def test_multi_connect():
    '''test select'''

def test_page():
    '''test page'''
    try:
        with connect_db('test') as db:
            sql = db.select_sql('schedule')
            page_datas = db.select_page(sql)
            print(page_datas)
            pass
    except Exception as e:
        print(e)

def test_like():
    '''test like'''
    with connect_db('test') as db:
        graphs = db.select(
            'graphs',
            where={
                'username': '郑水清',
                'name': ('like', '%默认光伏%'),
                })
        print(graphs)

@with_connect_db('test')
def test_with_connect_db(db):
    one_graph = db.slect('graphs', where={'id': 1020}).first()
    print(one_graph)

class WithTest():
    @with_connect_db('test')
    def test_with_class_method(self):
        one_graph = self.db.select('graphs', where={'id': 1020}).first()
        print(one_graph)

@with_connect_db(['test', 'wind'])
def test_with_connect_list_db(db):
    one_graph = db['test'].select('graphs', where={'id': 1020}).first()
    print(one_graph)

class WithlistTest():
    @with_connect_db(['test', 'wind'])
    def test_with_class_list_method(self):
        one_graph = self.db['test'].select('graphs', where={'id': 1020}).first()
        print(one_graph)

@with_connect_db('test')
def test_cross_db(db):
    data = db.get('select * from jobs.schedule limit 1')
    with db.connect_cur as cur:
        cur.execute('select * from jobs.schedule')
        data = cur.fetchall()
    print(data)

if __name__ == '__main__':
    test_redshift_in()
    # test_redshift()
    # test_query()
    # test_param()
    # test_idus()
    # test_args()
    # test_sql()
    # test_transaction()
    # test_select_one()
    # test_dbo_select()
    # test_select_page()
    # test_select_like()
    # test_with_connect_db(None)
    # WithTest().test_with_class_method()
    # test_select_page()
    # test_cross_db(None)
