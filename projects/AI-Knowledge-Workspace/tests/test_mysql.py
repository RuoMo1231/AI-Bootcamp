import pymysql

connection = pymysql.connect(
    host="localhost",
    port=33059,
    user="root",
    password="123456",
    database="ai_workspace",
)

print('MySQL 连接成功!')

connection.close()