from pymysql import cursors,connect

conn=connect (
    host="127.0.0.1",
    user="root",
    password="1234",
    db="guest",
    charset="utf8mb4",
    cursorclass=cursors.DictCursor)
try:
    with conn.cursor() as cursor:
        sql="insert into sign_guest (realname,phone,email,sign,event_id,create_time)\
        values ('tom',15330235989,'tom.@mail.com',0,1, NOW ());"
        cursor.execute(sql)
        conn.commit()
    with conn.cursor() as cursor:
        sql ="select realname,phone,email,sign from sign_guest where phone=%S"
        cursor.execute(sql,('15330235989'))
        result=cursor.fetchone()
        print(result)
finally:
    conn.close()


