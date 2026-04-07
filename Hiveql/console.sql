drop table test;
create table test(
    dt STRING,
    a STRING
);

insert into test (dt, a)
values ('2015-10-16', '2');

insert into test (dt, a)
values ('2024-10-13', '0');

insert into test (dt, a)
values ('2024-1-12', '2.5');

insert into test (dt, a)
values ('2023-1-12', '0.1');

select * from test where dt >= add_months(trunc(current_date(),'YY'),-12);
select * from test where a > 0;
select add_months(trunc(current_date(),'YY'),-12);