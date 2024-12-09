.. currentmodule:: dbpoolpy
Version 0.6.11
-------------

Released on 2024-12-09

- mysql去掉self._server_id

Version 0.6.10
-------------

Released on 2024-12-05

- 增加add_pool功能
- close_pool可以传单个name,释放单个name的pool

Version 0.6.9
-------------

Released on 2024-08-14

- 在fetchall和fetchone之前做rowcount>0的判断

Version 0.6.8
-------------

Released on 2024-07-09

- where中增加_and和_or功能
- where中同字段可以重复定义key__1, key__2, key__3 ...  实现对一个字段的多个约束

Version 0.6.7
-------------

Released on 2023-11-22

- 增加close_pool功能

Version 0.6.6
-------------

Released on 2023-05-16

- 修复postgresql的page无法使用的bug

Version 0.6.5
-------------

Released on 2022-12-07

- 完善markdown文件

Version 0.6.4
-------------

Released on 2022-08-16

- 修复page无法使用的问题

Version 0.6.3
-------------

Released on 2022-08-03

- 去掉clear timeout的打印

Version 0.6.2
-------------

Released on 2022-08-02

- 优化table在使用时执行两次open_conn的问题
- 把print改成printer

Version 0.6.1
-------------

Released on 2022-07-27

- 增加update_batch,add_batch,manysql功能

Version 0.5.12
-------------

Released on 2022-07-18

- 修复add_batch

Version 0.5.11
-------------

Released on 2022-07-18

- 修复add_batch

Version 0.5.10
-------------

Released on 2022-07-07

- 去掉OperateError的拦截

Version 0.5.9
-------------

Released on 2022-06-27

- table增加map和map_one方法优化

Version 0.5.8
-------------

Released on 2022-06-27

- table增加map和map_one方法

Version 0.5.7
-------------

Released on 2022-05-27

- postgresql 修复使用in传参不能使用列表的问题

Version 0.5.6
-------------

Released on 2022-04-16

- 增加dbtype每个连接池的传值

Version 0.5.5
-------------

Released on 2022-03-28

- 修复Table中的一些bug

Version 0.5.4
-------------

Released on 2022-03-04

- 加入Table的功能

Version 0.5.3
-------------

Released on 2022-02-01

- 修复sqlite3 where中不能使用in的问题

Version 0.5.2
-------------

Released on 2022-01-22

- 加入insert_batch功能

Version 0.5.1
-------------

Released on 2022-01-22

- 加入sqlite3兼容
- 修复where中的!=不能传int的问题
- select 方法中加入page功能

Version 0.4.6
-------------

Released on 2021-11-15

- 断开重连时不会再打印错误日志

Version 0.4.5
-------------

Released on 2021-11-12

- 去掉pymysql的依赖

Version 0.4.3
-------------

Released on 2021-10-18

- 修复一些bug

Version 0.4.2
-------------

Released on 2021-10-11

- 去掉psycopg2的强依赖

Version 0.4.1
-------------

Released on 2021-10-08

-  mysql and postgresql add transaction function

Version 0.4.0
-------------

Released on 2021-09-29

-  make postgresql engine available

Version 0.3.6
-------------

Released on 2021-09-17

-  add Select, Insert, Update, Delete

Version 0.3.5
-------------

Released on 2021-09-15

-  steady use dbo

Version 0.3.4
-------------

Released on 2021-09-10

-  insert return lastrowid

Version 0.3.3
-------------

Released on 2021-09-04

-  fix the print bug

Version 0.3.2
-------------

Released on 2021-09-04

-  changes log to print

Version 0.3.1
-------------

Released on 2021-09-03

-  changes settings import from imlf

Version 0.3.0
-------------

Released on 2021-09-03

-  add settings functions

Version 0.2.0
-------------

Released on 2021-08-25

-  加dbo，模仿sqlalchemy操作

Version 0.1.17
-------------

Released on 2021-08-20

-  修复clear_timeout找到不conn的bug

Version 0.1.16
-------------

Released on 2021-08-11

-  修复断开重连不可用的bug

Version 0.1.15
-------------

Released on 2021-08-10

-  去掉fields的处理,使得可以支持count和max

Version 0.1.14
-------------

Released on 2021-08-06

-  simple加入数据库连接断后重新连接功能，最多重新连3次

Version 0.1.13
-------------

Released on 2021-08-02

-  修复valuestosql不能同时拼接两个的bug

Version 0.1.11
-------------

Released on 2021-08-02

-  修复to_list bug

Version 0.1.10
-------------

-  配置is_old改成ptype，默认使用simple

Version 0.1.9
-------------

Released on 2021-08-01

-  修复旧版连接池
-  统一新旧两版的变量命名

Version 0.1.8
-------------

Released on 2021-07-30

-  加入debug配置，debug为False时不打引sql语句

Version 0.1.7
-------------

Released on 2021-07-29

-  重写DBHelper

Version 0.1.6
-------------

Released on 2021-07-27

-  增加get_one方法
-  把select_join_one改成select_one_join
-  增加get_join_one方法
-  改进select_page,使得select_page可以直接返回page数据

Version 0.1.5
-------------

Released on 2021-07-21

-  使用escape_string对sql语句中的字符串做一次转换，转义字符的优化

Version 0.1.4
-------------

Released on 2021-07-20

-  执行sql命令报错时抛出异常，并将异常信息写入日志里
-  pooled_db部分英文汉化

Version 0.1.3
-------------

Released on 2021-07-19

-  init_db 改成init_pool

Version 0.1.2
-------------

Released on 2021-07-19

-  输出日志信息，连接池数量及数据库连接信息等 

Version 0.1.1
-------------

Released on 2021-07-18

-   把连接池更换成pooled_db, 参考dbutils
