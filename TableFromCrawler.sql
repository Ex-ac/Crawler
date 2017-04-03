use test;

drop table searchInfo;
drop table baiduSearch;
drop table errorInfo;

create table searchInfo
(
	keyWord varchar(25),
    startTime datetime,
    stopTime datetime,
    runningTime datetime,
    primary key (keyWord, startTime, stopTime)
);

create table baiduSearch
(
	keyWord varchar(25) references searchInfo(keyword) on delete cascade,
    url nvarchar(1024),
    hasGet boolean default false,
    primary key (url)
);

create table errorInfo
(
	ID int auto_increment,
	source varchar(128),
    detale varchar(512),
    primary key (ID)
);


    
    