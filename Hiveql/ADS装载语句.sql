-- 初始化设置

-- 1.景点数量统计表
insert overwrite table travel_db_ads.ads_sight_count_stats
select
    `current_date`(),
    sum(sight_count) as total_sight_count, -- 统计景点总数
    sum(sight_count_5a) as total_sight_count_5a, -- 统计5a级景点个数
    sum(sight_count_4a) as total_sight_count_4a -- 统计4a级景点个数
from
    travel_db_dws.dws_province_sight_a_stats;

-- 2.各省份景点信息统计
insert overwrite table travel_db_ads.ads_province_stats
select
    `current_date`(),
    psa.province,
    phs.province_heat_score,
    sum(psa.sight_count) as total_sight_count, -- 统计景点总数
    sum(psa.sight_count_5a) as total_sight_count_5a, -- 统计5a级景点个数
    sum(psa.sight_count_4a) as total_sight_count_4a -- 统计4a级景点个数
from
    travel_db_dws.dws_province_sight_a_stats as psa
left join
    travel_db_dws.dws_province_heat_score as phs
on
    psa.province = phs.province
group by
    psa.province,
    phs.province_heat_score;

-- 3.各城市景点信息统计
insert overwrite table travel_db_ads.ads_city_stats
select
    `current_date`(),
    csa.province,
    csa.city,
    chs.city_heat_score,
    csa.sight_count,
    csa.sight_count_5a,
    csa.sight_count_4a
from
    travel_db_dws.dws_city_sight_a_stats csa
left join
    travel_db_dws.dws_city_heat_score chs
on
    csa.city = chs.city;

-- 4.景点热度top10
select count(1) from travel_db_ads.ads_sight_heat_score_top_10_stats;
insert overwrite table travel_db_ads.ads_sight_heat_score_top_10_stats
SELECT
    `current_date`(),
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
FROM (
    SELECT
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
        ROW_NUMBER() OVER (PARTITION BY province, city ORDER BY heat_score DESC, score DESC) AS rank
    FROM
        travel_db_dwd.dwd_travel_sight_info
) t
WHERE
    t.rank <= 10;

-- 5.景点评分top10
insert overwrite table travel_db_ads.ads_sight_score_top_10_stats
SELECT
    `current_date`(),
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
FROM (
    SELECT
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
        ROW_NUMBER() OVER (PARTITION BY province, city ORDER BY score DESC, comments_count DESC) AS rank
    FROM
        travel_db_dwd.dwd_travel_sight_info
) t
WHERE
    t.rank <= 10;

-- select * from travel_db_dwd.dwd_travel_sight_info where sight_name = '故宫博物院';

-- 6.各城市景点评分占比统计  (5分制)  0-3分  3-3.5分  3.5-4分  4-4.5分  4.5-5分
insert overwrite table travel_db_ads.ads_sight_score_rate
select
    `current_date`(),
    province,
    city,
    count(1) as sight_count,
    sum(case when score >= 4.5 and score <= 5 then 1 else 0 end) as comment_score_count_4_5_to_5,
    sum(case when score >= 4 and score < 4.5 then 1 else 0 end) as comment_score_count_4_to_4_5,
    sum(case when score >= 3.5 and score < 4 then 1 else 0 end) as comment_score_3_5_to_4,
    sum(case when score >= 3 and score < 3.5 then 1 else 0 end) as comment_score_3_to_3_5,
    sum(case when score >= 0 and score < 3 then 1 else 0 end) as comment_score_0_to_3
from
    travel_db_dwd.dwd_travel_sight_info
group by
    province,
    city;

-- select * from travel_db_dwd.dwd_travel_sight_info where province='上海' and comment_score >= 4.5 and comment_score <= 5;

-- 7.各城市景点热度占比统计  (10分制)   0-6分  6-7分  7-8分  8-9分  9-10分
insert overwrite table travel_db_ads.ads_sight_heat_score_rate
select
    `current_date`(),
    province,
    city,
    count(1) as sight_count,
    sum(case when heat_score >= 9 and heat_score <= 10 then 1 else 0 end) as count_9_to_10,
    sum(case when heat_score >= 8 and heat_score < 9 then 1 else 0 end) as count_8_to_9,
    sum(case when heat_score >= 7 and heat_score < 8 then 1 else 0 end) as count_7_to_8,
    sum(case when heat_score >= 6 and heat_score < 7 then 1 else 0 end) as count_6_to_7,
    sum(case when heat_score >= 0 and heat_score < 6 then 1 else 0 end) as count_0_to_6
from
    travel_db_dwd.dwd_travel_sight_info
group by
    province,
    city;

-- select * from travel_db_ads.ads_city_sight_heat_score_rate;

-- select * from travel_db_dwd.dwd_travel_sight_info where province = '上海' and heat_score >=9 and comment_score <= 10;

-- 8.用户评分占比统计  (5分制)   1分  2分  3分  4分  5分
insert overwrite table travel_db_ads.ads_comment_sight_score_rate
select
    `current_date`(),
    tsi.province,
    tsi.city,
    count(1) as score_count,
    sum(case when tci.score == 5 then 1 else 0 end) as score_count_5,
    sum(case when tci.score == 4 then 1 else 0 end) as score_count_4,
    sum(case when tci.score == 3 then 1 else 0 end) as score_count_3,
    sum(case when tci.score == 2 then 1 else 0 end) as score_count_2,
    sum(case when tci.score == 1 then 1 else 0 end) as score_count_1
from
    travel_db_dwd.dwd_travel_comment_info  as tci
left join travel_db_dwd.dwd_travel_sight_info  as tsi
    on tci.sight_id = tsi.sight_id and tsi.province is not null
group by
    tsi.province,
    tsi.city;

-- select * from travel_db_ads.ads_comment_sight_score_rate;
