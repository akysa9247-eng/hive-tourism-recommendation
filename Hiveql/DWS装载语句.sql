
-- 1.各城市热度表
insert overwrite table travel_db_dws.dws_city_heat_score
select
    t.province,
    t.city,
    cast(round(avg(t.heat_score) * 1000) as bigint)
from
    (
        select
            province,
            city,
            heat_score,
            row_number() over (partition by city order by heat_score desc) as rank
        from
            travel_db_dwd.dwd_travel_sight_info
    ) as t
where t.rank <= 20
group by
    t.province,
    t.city;

-- select * from travel_db_dws.dws_city_heat_score;

-- 2.各省份热度表
insert overwrite table travel_db_dws.dws_province_heat_score
select
    t.province,
    cast(round(avg(t.city_heat_score))  as bigint) as avg_top_10_heat_score
from
    (
        select
            province,
            city_heat_score,
            row_number() over (partition by province order by city_heat_score desc) as rank
        from
            travel_db_dws.dws_city_heat_score
    ) as t
where
    t.rank <= 5
group by
    t.province;

-- select * from travel_db_dws.dws_province_heat_score;

-- 3.各城市a级景区信息表
insert overwrite table travel_db_dws.dws_city_sight_a_stats
select
    province,
    city,
    count(1) as sight_count, -- 统计景点总数
    sum(case when level = '5A' then 1 else 0 end) as sight_5a_count, -- 统计5a级景点个数
    sum(case when level = '4A' then 1 else 0 end) as sight_4a_count -- 统计4a级景点个数
from
    travel_db_dwd.dwd_travel_sight_info
group by
    province,
    city;


-- select * from travel_db_dws.dws_city_sight_a_stats;

-- 4.各省份a级景区信息表
insert overwrite table travel_db_dws.dws_province_sight_a_stats
select
    province,
    cast(sum(sight_count) as bigint) as sight_count, -- 统计景点总数
    cast(sum(sight_count_5a) as bigint) as sight_5a_count,  -- 统计5a级景点个数
    cast(sum(sight_count_4a) as bigint) as sight_4a_count   -- 统计4a级景点个数
from
    travel_db_dws.dws_city_sight_a_stats
group by
    province;

-- select * from travel_db_dws.dws_province_sight_a_stats;