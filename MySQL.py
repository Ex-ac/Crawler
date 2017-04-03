import pymysql;

class MySqlDB(object):
    def __init__(self, host = "localhost", user = "root", passwd = "1234", db = "baidu"):
        self.connect = None;
        self.cursor = None;
        try:
            self.connect = pymysql.connect(host = host, user = user, passwd = passwd, db = db, charset='utf8');
            self.cursor = self.connect.cursor(pymysql.cursors.DictCursor);
            print("Successful!");
        except pymysql.Error as e:
            print(e.args[0], e.args[1]);
            print("Faile!");
            raise;

    def addSerachInfo(self, data):
        try:
            sql = u"insert into searchinfo values('%s', '%s', '%s', '%s')" %(data["keyword"], data["starttime"].strftime("%Y-%m-%d %H:%M:%S"), data["stoptime"].strftime("%Y-%m-%d %H:%M:%S"), data["runningtime"].strftime("%Y-%m-%d %H:%M:%S"));
            self.cursor.execute(sql.encode("utf-8"));
            self.connect.commit();
        except pymysql.Error as e:
            if str(e.args[1]).lower().find('primary') == -1:
                self.addErrorInfo(e);
            else:
                pass;

    def updateSearchInfo(self, data):
        try:
            sql = u"update searchinfo  set runningtime = '%s' where keyword = '%s' and starttime = '%s' and stoptime = '%s'" %(data["runningtime"].strftime("%Y-%m-%d %H:%M:%S"), data["keyword"], data["starttime"].strftime("%Y-%m-%d %H:%M:%S"), data["stoptime"].strftime("%Y-%m-%d %H:%M:%S"));
            
            #print(sql);
            self.cursor.execute(sql.encode("utf-8"));
            self.connect.commit();
        except pymysql.Error as e:
            self.addErrorInfo(e);
            raise;

    def addBaiduSerach(self, data):
        try:
            sql = u"insert into baidusearch values('%s', '%s', 0)" %(data["keyword"], data["url"]);
            self.cursor.execute(sql.encode("utf-8"));
            #self.connect.commit();
        except pymysql.Error as e:
            if str(e.args[1]).lower().find('primary') == -1:
                self.addErrorInfo(e);
            else:
                pass;
        

    def addErrorInfo(self, error):
        data = {};
        data["source"] = error.args[0];
        data["detaile"] = error.args[1];
        try:
            sql = u"insert into errorinfo values('%s', '%s')" % (data["source"], data["detaile"]);
            self.cursor.execute(sql.encode("utf-8"));
            self.connect.commit();
        except pymysql.Error as e:
            print(e.args[0], e.args[1]);
            raise;


if __name__ == "__main__":
    import datetime;
    import time;
    starttime = datetime.datetime.now();
    stoptime = datetime.datetime.now();
    runningtime = datetime.datetime.now();
    keyword = u"google";

    
    url = u"grrgergsdgfsdgregs";

    searchInfo = {};
    searchInfo["keyword"] = keyword;
    searchInfo["starttime"] = starttime;
    searchInfo["stoptime"] = stoptime;
    searchInfo["runningtime"] = runningtime;


    data = {};
    data["keyword"] = keyword;
    data["url"] = url;
    db = MySqlDB(db = "test");

    db.addSerachInfo(searchInfo);
    db.addBaiduSerach(data);

    searchInfo["runningtime"] = datetime.datetime(year = 2017, month = 2, day = 3, hour = 4);

    db.updateSearchInfo(searchInfo); 

