drop database if exists travel_db_dws;
create database if not exists travel_db_dws;

show create database travel_db_dws;

use travel_db_dws;

show databases;
show tables;

-- 1.各城市热度表
drop table if exists travel_db_dws.dws_city_heat_score;
create external table travel_db_dws.dws_city_heat_score(
    province string comment "省份",
    city string comment "城市",
    city_heat_score bigint comment "城市热度"
) comment '各城市热度表'
    stored as orc
    location '/travel_db/dws/dws_city_heat_score'
    tblproperties('orc.compress' = 'snappy');

-- 2.各省份热度表
drop table travel_db_dws.dws_province_heat_score;
create external table travel_db_dws.dws_province_heat_score(
    province string comment "省份",
    province_heat_score bigint comment "省份热度"
) comment '各省份热度表'
    stored as orc
    location '/travel_db/dws/dws_province_heat_score'
tblproperties('orc.compress' = 'snappy');

-- 3.各城市A级景区信息表
drop table travel_db_dws.dws_city_sight_a_stats;
create external table travel_db_dws.dws_city_sight_a_stats(
    province string comment "省份",
    city string comment "城市",
    sight_count bigint comment "景点个数",
    sight_count_5a bigint comment "5a级景点个数",
    sight_count_4a bigint comment "4a级景点个数"
) comment '各城市A级景区信息表'
    stored as orc
    location '/travel_db/dws/dws_city_sight_a_stats/'
    tblproperties('orc.compress' = 'snappy');

-- 4.各省份A级景区信息表
drop table travel_db_dws.dws_province_sight_a_stats;
create external table travel_db_dws.dws_province_sight_a_stats(
    province string comment "省份",
    sight_count bigint comment "景点个数",
    sight_count_5a bigint comment "5a级景点个数",
    sight_count_4a bigint comment "4a级景点个数"
  ) comment '各省份A级景区信息表'
    row format delimited fields terminated by '\t'
    location '/travel_db/dws/dws_province_sight_a_stats';
