import pymysql;
import datetime;

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

    def addSerachInfo(self, searchInfo):

        if "startTime" not in searchInfo.keys():
            searchInfo["startTime"] = datetime.datetime(2010, 1, 1, 0, 0, 0);
        if "stopTime" not in searchInfo.keys():
            searchInfo["stopTime"] = datetime.datetime(year = 1990, month = 1, day = 1, hour = 0);
        if "runningTime" not in searchInfo.keys():
            searchInfo["runningTime"] = searchInfo["startTime"];
        try:
            sql = u"insert into searchInfo values('%s', '%s', '%s', '%s')" %(searchInfo["keyWord"], searchInfo["startTime"].strftime("%Y-%m-%d %H:%M:%S"), searchInfo["stopTime"].strftime("%Y-%m-%d %H:%M:%S"), searchInfo["runningTime"].strftime("%Y-%m-%d %H:%M:%S"));
            self.cursor.execute(sql.encode("utf-8"));
            self.connect.commit();
        except pymysql.Error as e:
            if str(e.args[1]).lower().find('primary') == -1:
                self.addErrorInfo(e);
            else:
                pass;

    def updateSearchInfo(self, data):
        try:
            sql = u"update searchInfo  set runningTime = '%s' where keyWord = '%s' and startTime = '%s' and stopTime = '%s'" %(data["runningTime"].strftime("%Y-%m-%d %H:%M:%S"), data["keyWord"], data["startTime"].strftime("%Y-%m-%d %H:%M:%S"), data["stopTime"].strftime("%Y-%m-%d %H:%M:%S"));
            
            #print(sql);
            self.cursor.execute(sql.encode("utf-8"));
            self.connect.commit();
        except pymysql.Error as e:
            self.addErrorInfo(e);
            raise;


    def getUnfinishedTask(self):
        sql = "select * from searchInfo where stopTime = '1990-01-01 00:00:00' or stopTime > runningTime";
        try:
            self.cursor.execute(sql.encode("utf-8"));
            return self.cursor.fetchall();
        except pymysql.Error as e:
            self.addErrorInfo(e);
            raise;

    def addErrorInfo(self, error):
        data = {};
        data["source"] = error.args[0];
        data["detaile"] = error.args[1];
        try:
            sql = u"insert into errorInfo values('%s', '%s')" % (data["source"], data["detaile"]);
            self.cursor.execute(sql.encode("utf-8"));
            self.connect.commit();
        except pymysql.Error as e:
            print(e.args[0], e.args[1]);
            raise;

               
    def addBaiduSerach(self, data):
        try:
            sql = u"insert into baiduSearch values('%s', '%s', 0)" %(data["keyWord"], data["url"]);
            self.cursor.execute(sql.encode("utf-8"));
            #self.connect.commit();
        except pymysql.Error as e:
            if str(e.args[1]).lower().find('primary') == -1:
                self.addErrorInfo(e);
            else:
                pass;


if __name__ == "__main__":
    import datetime;
    import time;
    startTime = datetime.datetime.now();
    stopTime = datetime.datetime.now();
    runningTime = datetime.datetime.now();
    keyWord = u"google";

    
    url = u"grrgergsdgfsdgregs";

    searchInfo = {};
    searchInfo["keyWord"] = keyWord;
    searchInfo["startTime"] = startTime;
    searchInfo["stopTime"] = stopTime;
    searchInfo["runningTime"] = runningTime;


    data = {};
    data["keyWord"] = keyWord;
    data["url"] = url;
    db = MySqlDB(db = "test");

    db.addSerachInfo(searchInfo);
    db.addBaiduSerach(data);

    searchInfo["runningTime"] = datetime.datetime(year = 2017, month = 2, day = 3, hour = 4);

    db.updateSearchInfo(searchInfo); 

