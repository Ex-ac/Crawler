# -*- coding:utf-8-*-

from lxml import etree;
import re;
import os;
import datetime;
import time;
from math import ceil;
import codecs;
import requests;
import codecs;
import math;


from MySQL import *;

class BaiduSpider(object):
    def __init__(self, keyWord, headers = None, startTime = None, timeStep = None, stopTime = None, traget = None):
        super(BaiduSpider, self).__init__();
        self.keyWord = keyWord;

        self.headers = headers;
        self.traget = traget;

        self.timeStep = timeStep;

        if self.timeStep == None:
            self.timeStep = datetime.timedelta(seconds = 3600);

        self.startTime = startTime;
        if self.startTime == None:
            self.startTime = datetime.datetime(2010, 1, 1);
        
        self.stopTime = stopTime;
        
        self.runningTime = self.startTime;
        

    def searchWthinTheTimePeriod(keyWord, startTime, step = datetime.timedelta(seconds = 3600), headers = None,traget = None):

        strStartTime = int(time.mktime(startTime.timetuple()));
        strEndTime = int(time.mktime((startTime + step).timetuple())) - 2;
        url = u"https://www.baidu.com/s?ie=utf-8&word=%s&rn=20" % keyWord + "&si=weibo.com&ct=2097152"
        pn = 0;
        gpc = "&gpc=stf%3D" + str(strStartTime) + "%2C" + str(strEndTime) + "%7Cstftype%3D2";
        searchURL = url + gpc;
        
        print('\n\r' * 2);
        print('*' * 100 );
        print(searchURL);

        numPages = BaiduSpider.getPages(BaiduSpider.getData(searchURL, headers));
        p = 1;
        print(str(startTime), '~', str((startTime + step)));
        time.sleep(2);
        while pn < numPages:
            
            print("开始下载第%d页，共计%d页" % (p, math.ceil(numPages / 20)));
            html = BaiduSpider.getData(searchURL, headers);
            pagesResult = BaiduSpider.getBox(html);

            for each in pagesResult:
                result = BaiduSpider.getResult(each);
                result["keyWord"] = keyWord;
                BaiduSpider.saveData(result, traget);


            pn += 20;
            p += 1;
            searchURL += "&pn=" + str(pn);
            time.sleep(2);
            
        return startTime + step;

    def run(self):
        searchInfo = {};
        searchInfo["keyWord"] = self.keyWord;
        searchInfo["startTime"] = self.startTime;
        if self.stopTime == None:
            self.stopTime = datetime.datetime(year = 1990, month = 1, day = 1, hour = 0);
        searchInfo["stopTime"] = self.stopTime;
        searchInfo["runningTime"] = self.startTime;
        self.traget.addSerachInfo(searchInfo);
        if self.stopTime == datetime.datetime(year = 1990, month = 1, day = 1, hour = 0):
            while self.runningTime < datetime.datetime.now():
                self.runningTime = BaiduSpider.searchWthinTheTimePeriod(self.keyWord, self.runningTime, self.timeStep, self.headers, self.traget);
                searchInfo["runningTime"] = self.runningTime;
                self.traget.updateSearchInfo(searchInfo);

        else:
            while self.runningTime < self.stopTime:
                self.runningTime = BaiduSpider.searchWthinTheTimePeriod(self.keyWord, self.runningTime, self.timeStep, self.headers, self.traget);
                searchInfo["runningTime"] = self.runningTime;
                self.traget.updateSearchInfo(searchInfo);



    def saveData(result, traget = None):
        if traget == None:
            print("URL:", result['url']);
            print("title:", result['title']);
        else:
            traget.addBaiduSerach(result);


    def getData(searchURL, headers = None, retryNum = 5):

        try:
            data = requests.get(searchURL, headers = headers);
            if data.status_code == 503:
                print("[!] An error occurred! Please check whether any verification code");
                os._exit(0);
            else:
                return data.text;

        except requests.exceptions.Timeout as e:
            if retryNum > 0:
                return getData(searchURL, headers, retryNum - 1);
            else:
                e = Exception();
                e.args[0] = "getData()";
                e.args[1] = "TimeoutError";
                raise e;
        
    
    def getPages(data):
        selector = etree.HTML(data);

        numstr = selector.xpath('//div[@class="nums"]/text()')[0];

        print(numstr);
        s = filter(str.isdigit, numstr);
        number = int("".join(list(s)));
        
        return number;




    def getBox(data):
        selector = etree.HTML(data);
        boxField = selector.xpath('//div[@class="result c-container "]');
        return boxField;

    def getResult(eachData):
        result = {};
        try:

            url = eachData.xpath('h3[@class="t"]/a/@href')[0];
            str = eachData.xpath('h3[@class="t"]/a//text()');
        except:
            url = eachData.xpath('h3[@class="t"]/a/@href')[0];
            str = eachData.xpath('h3[@class="t"]/a//text()');
        '''
        time = eachData.xpath('.//p[@class="c-author"]/text()')[0];

        source = time.split()[0];
        timeStr = time.split()[1:];
        timeStr = "".join(timeStr);
        date = BaiduSpider.getTime(timeStr);
        '''
        result["url"] = url;
        result["title"] = "".join(str);
        #result["source"] = source;
        #result["date"] = date;

        return result;
    
    def getTime(timeStr):

        format = r"\d{4}年\d{2}月\d{2}日\d{2}:\d{2}";

        pattern = re.compile(format);
        match = pattern.match(timeStr);

        if match:
            unifidatime = datetime.datetime.strptime(timeStr, "%Y年%m月%d日%H:%M");
            return unifidatime;

        else:
            format = r"(\d{1,2})小时前";
            pattern = re.compile(format);
            match = pattern.match(timeStr);

            if match:

                hourStr = int(match.group(1));
                hour = datetime.timedelta(hours = hourStr);
                unifidatime = now - hour;
                return unifidatime;

            else:

                format = r"(\d{1,2}分钟前)";

                pattern = re.compile(format);
                match = pattern.match(timeStr);

                if match:
                    minStr = int(match.group(1));
                    minutes = datetime.timedelta(minutes = minStr);
                    unifidatime = now - minutes;
                    return unifidatime;
                
                else:
                    raise Exception("未找的具体时间");



if __name__ == "__main__":
    headers = {
    'Host': 'baidu.com',
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate'
    };

    db = MySqlDB(db = "test");
    
#    f = codecs.open("data.html", "w", "utf-8");

    startTime = datetime.datetime(2016, 2, 1);
 
    timeStep = datetime.timedelta(seconds = 3600 * 24);


    
    keyWord = u"魏则西";
    try:
        search = BaiduSpider(keyWord, headers, startTime, timeStep, traget = db);
        search.run();
    except Exception as e:
        db.addErrorInfo(e);
        raise;

    

        
