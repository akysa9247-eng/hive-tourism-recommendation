create database if not exists travel_db_ads;
use travel_db_ads;

show databases;
show tables;

-- 1.景点数量统计表
drop table if exists travel_db_ads.ads_sight_count_stats;
create external table travel_db_ads.ads_sight_count_stats(
    `dt` string COMMENT '统计日期',
    total_sight_count bigint comment "景点个数",
    total_sight_count_5a bigint comment "5a级景点个数",
    total_sight_count_4a bigint comment "4a级景点个数"
) comment '景点数量统计表'
    row format delimited fields terminated by '\t'
    location '/travel_db/ads/ads_sight_count_stats';

-- 2.各省份（景点）信息统计
drop table if exists travel_db_ads.ads_province_stats;
create external table travel_db_ads.ads_province_stats(
    `dt` string COMMENT '统计日期',
    province string comment "省份",
    heat_score bigint comment "省份热度",
    sight_count bigint comment "景点个数",
    sight_count_5a bigint comment "5a级景点个数",
    sight_count_4a bigint comment "4a级景点个数"
) comment '各省份景点信息统计'
    row format delimited fields terminated by '\t'
    location '/travel_db/ads/ads_province_stats';

-- 3.各城市（景点）信息统计
drop table if exists travel_db_ads.ads_city_stats;
create external table travel_db_ads.ads_city_stats(
    `dt` string COMMENT '统计日期',
    province string comment "省份",
    city string comment "城市",
    heat_score bigint comment "城市热度",
    sight_count bigint comment "景点个数",
    sight_count_5a bigint comment "5a级景点个数",
    sight_count_4a bigint comment "4a级景点个数"
) comment '各城市景点信息统计'
    row format delimited fields terminated by '\t'
    location '/travel_db/ads/ads_city_stats';

-- 4.景点热度top10
drop table if exists travel_db_ads.ads_sight_heat_score_top_10_stats;
create external table travel_db_ads.ads_sight_heat_score_top_10_stats(
    `dt` string COMMENT '统计日期',
    sight_id bigint comment "景点id",
    sight_name string comment "景点名称",
    province string comment "省份",
    city string comment "城市",
    tag_list string comment '标签列表',
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
) comment '景点热度top10'
    row format delimited fields terminated by '\t'
    location '/travel_db/ads/ads_sight_heat_score_top_10_stats';

-- 5.景点评分top10
drop table if exists travel_db_ads.ads_sight_score_top_10_stats;
create external table travel_db_ads.ads_sight_score_top_10_stats(
    `dt` string COMMENT '统计日期',
    sight_id bigint comment "景点id",
    sight_name string comment "景点名称",
    province string comment "省份",
    city string comment "城市",
    tag_list string comment '标签列表',
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
) comment '景点评分top10'
    row format delimited fields terminated by '\t'
    location '/travel_db/ads/ads_sight_score_top_10_stats';

-- 6.景点评分占比  (5分制)  0-3分  3-3.5分  3.5-4分  4-4.5分  4.5-5分
drop table if exists travel_db_ads.ads_sight_score_rate;
create external table travel_db_ads.ads_sight_score_rate(
    `dt` string COMMENT '统计日期',
    province string comment "省份",
    city string comment "城市",
    sight_count bigint comment "景点个数",
    score_count_4_5_to_5 bigint comment "4.5-5分景点个数",
    score_count_4_to_4_5 bigint comment "4-4.5分景点个数",
    score_count_3_5_to_4 bigint comment "3.5-4分景点个数",
    score_count_3_to_3_5 bigint comment "3-3.5分景点个数",
    score_count_0_to_3 bigint comment "0-3分景点个数"
) comment '各城市景点评分占比统计'
    row format delimited fields terminated by '\t'
    location '/travel_db/ads/ads_sight_score_rate';

-- 7.景点热度占比  (10分制)   0-6分  6-7分  7-8分  8-9分  9-10分
drop table if exists travel_db_ads.ads_sight_heat_score_rate;
create external table travel_db_ads.ads_sight_heat_score_rate(
    `dt` string COMMENT '统计日期',
    province string comment "省份",
    city string comment "城市",
    sight_count bigint comment "景点个数",
    heat_score_9_to_10 bigint comment "9-10分景点个数",
    heat_score_8_to_9 bigint comment "8-9分景点个数",
    heat_score_7_to_8 bigint comment "7-8分景点个数",
    heat_score_6_to_7 bigint comment "6-7分景点个数",
    heat_score_0_to_6 bigint comment "0-6分景点个数"
) comment '各城市景点热度占比统计'
    row format delimited fields terminated by '\t'
    location '/travel_db/ads/ads_sight_heat_score_rate';

-- 8.用户评分占比  (5分制)   1分  2分  3分  4分  5分
drop table if exists travel_db_ads.ads_comment_sight_score_rate;
create external table travel_db_ads.ads_comment_sight_score_rate(
    `dt` string COMMENT '统计日期',
    province string comment "省份",
    city string comment "城市",
    score_count bigint comment "评论个数",
    comment_score_count_5 bigint comment "5分评论个数",
    comment_score_count_4 bigint comment "4分评论个数",
    comment_score_count_3 bigint comment "3分评论个数",
    comment_score_count_2 bigint comment "2分评论个数",
    comment_score_count_1 bigint comment "1分评论个数"
) comment '用户评分占比统计'
    row format delimited fields terminated by '\t'
    location '/travel_db/ads/ads_comment_sight_score_rate';
