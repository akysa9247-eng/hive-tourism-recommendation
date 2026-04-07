create database if not exists travel_db_ods;

use travel_db_ods;

show databases;
show tables;

-- 1.景点信息表
drop table if exists travel_db_ods.ods_travel_sight_info;
create external table travel_db_ods.ods_travel_sight_info(
    sight_id bigint comment "景点id",
    sight_name string comment "景点名称",
    province string comment "省份",
    city string comment "城市",
    tag_list string comment "标签列表",
    detail_url string comment "详情页网址",
    level string comment "景点等级",
    heat_score decimal(10,2) comment "景点热度",
    score decimal(10,2) comment "评分",
    comments_count bigint comment "点评数量",
    address string comment "地址",
    telephone string comment "官方电话",
    intro string comment "介绍",
    opening_time string comment "开放时间",
    img_list string comment "图片列表",
    cover string comment "封面"
) comment '景点信息表'
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
    stored as textfile
	location '/travel_db/ods/ods_travel_sight_info/'
    tblproperties ('skip.header.line.count'='1');

select count(1) from ods_travel_sight_info;
select count(1) from ods_travel_sight_info group by province, city;
-- 2.景点评论信息表
drop table if exists travel_db_ods.ods_travel_comment_info;
create external table travel_db_ods.ods_travel_comment_info(
    comment_id bigint comment "评论id",
    user_name string comment "用户名",
    sight_id bigint comment "景点id",
    content string comment "评论内容",
    score decimal(10,2) comment "评分",
    comment_date string comment '评论日期'
) comment '评论信息表'
    row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
    stored as textfile
	location '/travel_db/ods/ods_travel_comment_info/'
    tblproperties ('skip.header.line.count'='1');

select count(1) from travel_db_ods.ods_travel_sight_info;


select count(1) from travel_db_ods.ods_travel_comment_info;

select count(1) from travel_db_ods.ods_travel_comment_info as t where t.comment_date < '2023-01-01';
