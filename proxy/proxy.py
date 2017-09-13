from spide.spide import Proxy
from db.db import DBConn

if __name__ == "__main__":
    _proxy = Proxy()
    _db = DBConn()
    _db.InitDB("Proxy")
    _db.InitTB("Proxy","Proxy66")
    seed_url = 'http://www.66ip.cn/'
    _proxy.url = seed_url
    count = int(_proxy.get_count())
    for i in range(1,count+1):
        _proxy.url = seed_url + str(i) + '.html'
        datas = _proxy.get_data()
        print(i)
        if len(datas):
            for i in range(len(datas)):
                ip = datas[i][0]
                port = datas[i][1]

                _proxy.proxy = {
                    "http": "http://%s:%s" %(ip,port)
                }
                if(_proxy.verif_ip()):
                    print(datas[i])
                    _db.InsertToDB(datas[i],"Proxy","Proxy66")
