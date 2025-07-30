# db.py
import MySQLdb

def get_db_connection():
    return MySQLdb.connect(
        host='245124733172.mysql.pythonanywhere-services.com',
        user='245124733172',
        password='Nishita@25',
        database='245124733172$default'
    )