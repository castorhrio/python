import pymysql

class DBConn(object):
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.pwd = "wasd123"
    
    def InitDB(self,dbname):
        conn = ""
        cursor = ""
        try:
            conn = pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.pwd)
            cursor = conn.cursor()
            if dbname is not None:
                dbsql = "create database if not exists %(dbname)s default character set utf8 collate utf8_general_ci" %{'dbname':dbname}
                cursor.execute(dbsql)
            conn.commit()
        except Exception as ex:
            print("Init DB error:",ex)
        
        finally:
            cursor.close()
            conn.close()
    
    def InitTB(self,dbname,tbname):
        conn = ""
        cursor = ""
        try:
            conn = pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.pwd)
            conn.select_db(dbname)
            cursor = conn.cursor()
            
            if tbname is not None:
                if '66' in tbname:
                    tbsql = "create table if not exists %(tbname)s (id int (11) not null auto_increment, ip varchar(255) not null, port varchar(255) not null, addr varchar(255) not null, time varchar(255) not null, primary key (id)) default charset=utf8 auto_increment=0" %{'tbname':tbname}
            cursor.execute(tbsql)
            conn.commit()
        except Exception as ex:
            print("Init table %s error %s:" %(tbname,ex))
        finally:
            cursor.close()
            conn.close()
    
    def InsertToDB(self,data,dbname,tbname):
        conn = ""
        cursor = ""
        try:
            conn = pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.pwd,charset="utf8")
            cursor = conn.cursor()
            conn.select_db(dbname)
            if '66' in tbname:                
                sql = "insert into %(tbname)s(ip,port,addr,time)" %{'tbname':tbname}
                if data is not None:
                    cursor.execute(sql+"values(%s,%s,%s,%s)",data)
            conn.commit()    
        except Exception as ex:
            print("insert to table %s error: %s" %(tbname,ex))
        
        finally:
            cursor.close()
            conn.close()