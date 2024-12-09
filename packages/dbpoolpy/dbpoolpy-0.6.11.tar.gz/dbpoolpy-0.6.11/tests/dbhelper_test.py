#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
HOME_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'src/')
sys.path.append(HOME_PATH)
from dbpoolpy.dbhelper import DBHelper

def test_field2sql():
    field1 = 'id'
    ret1 = DBHelper().field2sql(field1)
    assert ret1 == '`id`'
    field2 = 'a.id'
    ret2 = DBHelper().field2sql(field2)
    assert ret2 == '`a`.`id`'
    field3 = 'a.id as ai'
    ret3 = DBHelper().field2sql(field3)
    assert ret3 == '`a`.`id` as `ai`'

def test_fields2sql():
    fields1 = 'graphs, imlf.nodes, imlf.graphs as ig'
    ret1 = DBHelper().fields2sql(fields1)
    assert ret1 == '`graphs`,`imlf`.`nodes`,`imlf`.`graphs` as `ig`'
    fields2 = ['graphs', 'imlf.nodes', 'imlf.graphs as ig']
    ret2 = DBHelper().fields2sql(fields2)
    assert ret2 == '`graphs`,`imlf`.`nodes`,`imlf`.`graphs` as `ig`'
    fields3 = ('graphs', 'imlf.nodes', 'imlf.graphs as ig')
    ret3 = DBHelper().fields2sql(fields3)
    assert ret3 == '`graphs`,`imlf`.`nodes`,`imlf`.`graphs` as `ig`'

def test_now_time():
    time = datetime.datetime.now()
    print(str(time))


if __name__ == '__main__':
    test_field2sql()
    pass
