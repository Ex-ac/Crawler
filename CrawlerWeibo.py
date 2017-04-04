from MySQL import *
from weibo import *
import datetime;


class CrawlerWeibo(MySqlDB):
    def __init__(self,  host = "localhost", user = "root", passwd = "1234", db = "baidu", headers = None, stepTime = None):
        super(CrawlerWeibo, self).__init__(host, user, passwd, db);

        self.stepTime = stepTime;
        self.headers = headers;

    def addWeiboTask(self, searchInfo):
        if "keyWord" not in searchInfo.keys():
            os._exit();

        self.addSerachInfo(searchInfo);
        print(u"成功添加关键词为： %s 的微博任务" % searchInfo["keyWord"]);

    
    
    def startTask(self):
        i = 1;
        searchTaskList = [];
        while True:
            searchInfoList = self.getUnfinishedTask();


            for searchInfo in searchInfoList:

                if searchInfo["runningTime"] < datetime.datetime.now():
                    searchTaskList.append(searchInfo);

            if len(searchTaskList) == 0:
                print(u"任务完成！")
                break;
            
            for searchInfo in searchTaskList:
                
                task = BaiduWeiboSearch(searchInfo, headers = self.headers, stepTime = self.stepTime, traget = self);
                print(u"NO: %d, Total: %d" % (i , len(searchTaskList)));
                print(searchInfo);
                task.run();
                i += 1;


     


if __name__ == "__main__":

    headers = {
    'Host': 'baidu.com',
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate'
    };

    stepTime = datetime.timedelta(seconds = 3600 * 24 * 30);

    db = CrawlerWeibo(db = "test", headers = headers, stepTime = stepTime);
    db.startTask();
'''
    searchInfo = {};
    searchInfo["keyWord"] = u"微软";
    searchInfo["startTime"] = datetime.datetime(2013, 1, 1);



    db.addWeiboTask(searchInfo);
'''