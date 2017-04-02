import requests;
import codecs;

if __name__ == "__main__":
    f = codecs.open("data.html", "w", "utf-8");
    f.write(requests.get("https://www.baidu.com/s?ie=utf-8&word=github&rn=20&si=weibo.com&ct=2097152&gpc=stf%3D1454256000%2C1459439998%7Cstftype%3D2").text);
    f.close();