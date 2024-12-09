try:
    import psycopg2
except:
    psycopg2 = None

conn = psycopg2.connect(database="test", user="ap-dev", password="ap_etL123", host="10.32.29.228", port="5432")
print("Opened database successfully")
# from psycopg2 import extensions
# print(extensions.adapt('j"fd"'))

cur = conn.cursor()
print(cur.mogrify("%s", ('f"d',)))

cur.execute(
    '''CREATE TABLE TESTCOMPANY
       (ID SERIAL PRIMARY KEY     NOT NULL,
       NAME           VARCHAR(50)    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        VARCHAR(50),
       SALARY         REAL);'''
       )
print("Table created successfully")

conn.commit()
conn.close()