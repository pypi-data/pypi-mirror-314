#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import traceback
import pytest
import json
import sqlite3
HOME_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'src/')
sys.path.append(HOME_PATH)
try:
    import psycopg2
except:
    psycopg2 = None
from dbpoolpy import with_connect_db, connect_db
from dbpoolpy import Select, Insert, Update, Delete

DATABASE = {
    'test':  {
        'engine': sqlite3,
        'database': 'testsqlite3.db',
        'maxconnections': 10
    }
}

from dbpoolpy import init_pool, connect_db
from dbpoolpy import settings
settings.DEBUG = True
settings.DB_TYPE = 'sqlite3'
init_pool(DATABASE)

test_db = "test"
test_table = "testtable"

def test_query():
    with connect_db('test') as db:
        graphs = db.query("select * from testtable")
        print(graphs)

def test_param():
    with connect_db('test') as db:
        graphs = db.query("select * from testtable where id=? limit 1", args=(1,))
        print(graphs)

def test_select():
    with connect_db('test') as db:
        testcompany=db.select('testtable').where(id=1).all()
        print(testcompany)

def test_wherein():
    with connect_db('test') as db:
        testcompany=db.select('testtable').where(id=("in", [1,2,3])).all()
        print(testcompany)
        # graphs = db.query("select * from testtable where id in (?) limit 1", args=(1,))
        # print(graphs)

def test_not_equal():
    with connect_db('test') as db:
        testcompany=db.select('testtable').where(id=("!=", 1)).all()
        print(testcompany)

def test_idus():
    # new_id = 107
    # 初始化测试数据
    test_table = "testtable"
    new_testcompany = dict(name='test', age=23)

    new_testcompany2 = dict(name='ttes', age=33)

    # 增
    new_id = Insert('test', test_table).values(**new_testcompany).execute() # 查
    new_testcompany_from_db = Select('test', test_table).where(id=new_id).first()
    assert new_testcompany_from_db['name'] == new_testcompany['name']
    assert new_testcompany_from_db['age'] == new_testcompany['age']

    # 改
    Update('test', test_table).where(id=new_id).values(**new_testcompany2).execute()
    # 查
    new_testcompany2_from_db = Select('test', test_table).where(id=new_id).first()
    assert new_testcompany2_from_db['name'] == new_testcompany2['name']
    assert new_testcompany2_from_db['age'] == new_testcompany2['age']
    # 删
    Delete('test', test_table).where(id=new_id).execute()
    new_testcompany = Select('test', test_table).where(id=new_id).first()
    assert not new_testcompany

def test_args():
    test_table = 'testtable'
    # 初始化测试数据
    new_testcompany = dict(name='ttes', age=23)

    new_testcompany2 = dict(name='ttes', age=33)

    # 增
    with connect_db('test') as db:
        new_id = db.insert(test_table).values(**new_testcompany).execute()
    # 查
    with connect_db('test') as db:
        new_testcompany_from_db = db.select(test_table).where(id=new_id).first()
    try:
        assert new_testcompany_from_db['name'] == new_testcompany['name']
        assert new_testcompany_from_db['age'] == new_testcompany['age']

        # 改
        with connect_db('test') as db:
            db.update(test_table).where(id=new_id).values(**new_testcompany2).execute()
            # 查
            new_testcompany2_from_db = db.select(test_table).where(id=new_id).first()
            assert new_testcompany2_from_db['name'] == new_testcompany2['name']
            assert new_testcompany2_from_db['age'] == new_testcompany2['age']
            # 删
            db.delete(test_table).where(id=new_id).execute()
            new_testcompany = db.select(test_table).where(id=new_id).first()
            assert not new_testcompany
    except Exception as e:
        Delete('test', test_table).where(id=new_id)

def test_transaction():
    '''测试事务'''
    new_testcompany = dict(name='测试transaction', age=24)
    new_testcompany2 = dict(name='测试transactionw', age=242, add_field='1234')
    with connect_db('test') as db:
        try:
            with db.transaction() as db_trans:
                new_id = db_trans.insert(test_table).values(**new_testcompany).execute()
                new_id2 = db_trans.insert(test_table).values(**new_testcompany2).execute()
            new_testcompany_from_db = db.select(test_table).where(id=new_id).first()
            assert new_testcompany_from_db
        except Exception as e:
            print(traceback.format_exc())
            new_testcompany_from_db = db.select(test_table).where(id=new_id).first()
            assert not new_testcompany_from_db
        if new_id:
            db.delete(test_table).where(id=new_id).execute()

def test_batch_success():
    '''测试批量插入'''
    data = [dict(name="batch", age=i) for i in range(500)]
    with connect_db('test') as db:
        try:
            db.insert_batch(test_table, data, batch=200)
            data_from_db = db.select(test_table).where(name="batch").all()
            assert len(data_from_db) == 500
        except Exception as e:
            raise e
        finally:
            db.delete(test_table).where(name="batch").execute()

def test_batch_exception():
    '''测试批量插入报错'''
    data = [dict(name="batch", age=i) for i in range(500)]
    data[400] = [dict(name="batch", age=2000, addfield=123)]
    with connect_db('test') as db:
        try:
            db.insert_batch(test_table, data, batch=200)
        except Exception:
            data_from_db = db.select(test_table).where(name="batch").all()
            print(len(data_from_db))
            assert len(data_from_db) == 0
        finally:
            db.delete(test_table).where(name="batch").execute()


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


def test_multi_connect():
    '''test select'''
    with connect_db('test') as db:
        with connect_db('test') as db:
            with connect_db('test') as db:
                one_graph = db.select('graphs', where={'id': 1020}).first
    with connect_db('test') as db:
        one_graph = db.select('graphs', where={'id': 1020}).first()
    with connect_db('test') as db:
        with connect_db('test') as db:
            one_graph = db.select('graphs', where={'id': 1020}).first()

def test_page():
    '''test page'''
    try:
        with connect_db('test') as db:
            page = db.select('schedule').page()
            print(page)
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
    one_graph = db.select('graphs', where={'id': 1020}).first()
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
    # test_query()
    # test_param()
    test_wherein()
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
    # test_batch_success()
