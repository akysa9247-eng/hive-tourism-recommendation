
-- 初始化设置
set hive.exec.dynamic.partition=true;	//开启动态分区功能（默认true，开启）
set hive.exec.dynamic.partition.mode=nonstrict;	//设置为非严格模式（动态分区的模式，默认strict，表示必须指定至少一个分区为静态分区，nonstrict模式表示允许所有的分区字段都可以使用动态分区。）
set hive.exec.max.dynamic.partitions.pernode=10000;
set hive.exec.max.dynamic.partitions=10000;
set hive.exec.max.created.files=10000;

-- 1.景点信息事实表
insert overwrite table travel_db_dwd.dwd_travel_sight_info partition (province, city)
select
    sight_id,
    sight_name,
    tag_list,
    detail_url,
    level,
    heat_score,
    score,
    comments_count,
    address,
    telephone,
    intro,
    opening_time,
    img_list,
    cover,
    province,
    city
from (select
          sight_id,
          sight_name,
          province,
          city,
          detail_url,
          level,
          heat_score,
          score,
          comments_count,
          address,
          telephone,
          intro,
          opening_time,
          img_list,
          cover,
          row_number() over (partition by sight_id order by sight_id desc) rank
      from travel_db_ods.ods_travel_sight_info) as t
where t.rank=1
    and t.heat_score > 0
    and t.score > 0
    and t.comments_count >= 30;

insert overwrite table travel_db_dwd.dwd_travel_sight_info
select
    sight_id,
    sight_name,
    province,
    city,
    tag_list,
    detail_url,
    level,
    heat_score,
    score,
    comments_count,
    address,
    telephone,
    intro,
    opening_time,
    img_list,
    cover
from (select
          sight_id,
          sight_name,
          province,
          city,
          tag_list,
          detail_url,
          level,
          heat_score,
          score,
          comments_count,
          address,
          telephone,
          intro,
          opening_time,
          img_list,
          cover,
          row_number() over (partition by sight_id order by sight_id desc) rank
      from travel_db_ods.ods_travel_sight_info) as t
where t.rank=1
    and t.heat_score > 0
    and t.score > 0
    and t.comments_count >= 30;

select * from travel_db_dwd.dwd_travel_sight_info where province = '台湾' limit 10;

-- 2.评论信息事实表
insert overwrite table travel_db_dwd.dwd_travel_comment_info partition (comment_date)
select
    comment_id,
    user_name,
    sight_id,
    content,
    score,
    comment_date
from
    (select
        comment_id,
        user_name,
        sight_id,
        content,
        score,
        comment_date,
        row_number() over (partition by user_name,sight_id,comment_date order by comment_date desc) rank
    from
        travel_db_ods.ods_travel_comment_info
    where
        comment_id > 0
    ) as t
where t.rank=1
    and t.score > 0
    and to_date(t.comment_date) >=  '2018-01-01';

insert overwrite table travel_db_dwd.dwd_travel_comment_info_mapping
select
    comment_id,
    user_name,
    sight_id,
    content,
    score,
    comment_date
from
    (select
        comment_id,
        user_name,
        sight_id,
        content,
        score,
        comment_date,
        row_number() over (partition by user_name,sight_id,comment_date order by comment_date desc) rank
    from
        travel_db_ods.ods_travel_comment_info
    where
        comment_id > 0
    ) as t
where t.rank=1
    and t.score > 0
    and to_date(t.comment_date) >=  '2018-01-01';


select add_months(trunc(current_date(),'YY'),-24);


select count(1) from travel_db_dwd.dwd_travel_comment_info_mapping;