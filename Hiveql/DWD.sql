create database if not exists travel_db_dwd;

drop database travel_db_dwd;

use travel_db_dwd;

-- 1.景点信息事实表
drop table travel_db_dwd.dwd_travel_sight_info;
create external table travel_db_dwd.dwd_travel_sight_info(
    sight_id bigint comment "景点id",
    sight_name string comment "景点名称",
    province string comment "省份",
    city string comment "城市",
    tag_list string comment "标签列表",
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
    stored as orc
    location '/travel_db/dwd/dwd_travel_sight_info'
    tblproperties('orc.compress' = 'snappy');


create external table travel_db_dwd.dwd_travel_sight_info(
    `sight_id` bigint comment "景点id",
    `sight_name` string comment "景点名称",
    `tag_list` string comment "标签列表",
    `level` string comment "景点等级",
    `heat_score` decimal(10,2) comment "景点热度",
    `score` decimal(10,2) comment "评分",
    `comments_count` bigint comment "点评数量",
    `address` string comment "地址",
    `telephone` string comment "官方电话",
    `intro` string comment "介绍",
    `opening_time` string comment "开放时间",
    `img_list` string comment "图片列表",
    `cover` string comment "封面"
) comment '景点信息表'
    partitioned by (`province` string comment "省份", `city` string comment "城市")
    stored as orc
    location '/travel_db/dwd/dwd_travel_sight_info'
    tblproperties('orc.compress' = 'snappy');

select count(1) from dwd_travel_sight_info group by province, city;

-- 2.评论信息事实表
drop table if exists travel_db_dwd.dwd_travel_comment_info;
create external table travel_db_dwd.dwd_travel_comment_info(
    comment_id bigint comment "评论id",
    user_name string comment "用户名",
    sight_id bigint comment "景点id",
    content string comment "评论内容",
    score decimal(10,2) comment "评分"
) comment '评论信息表'
    partitioned by (comment_date string comment '评论日期')
    stored as orc
    location '/travel_db/dwd/dwd_travel_comment_info/'
    tblproperties('orc.compress' = 'snappy');

select count(1) from travel_db_dwd.dwd_travel_comment_info;

-- 3.评论信息事实表_inflct
drop table if exists travel_db_dwd.dwd_travel_comment_info_mapping;
create external table travel_db_dwd.dwd_travel_comment_info_mapping(
    comment_id bigint comment "评论id",
    user_name string comment "用户名",
    sight_id bigint comment "景点id",
    content string comment "评论内容",
    score decimal(10,2) comment "评分",
    comment_date string comment '评论日期'
) comment '评论信息表'
    row format delimited fields terminated by '\t'
    location '/travel_db/dwd/dwd_travel_comment_info_mapping/'



