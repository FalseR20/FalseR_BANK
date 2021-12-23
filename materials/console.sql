-- select
select id, username, is_superuser, password
from auth_user;

select *
from mainapp_clients;

select *
from mainapp_currencies;

select *
from mainapp_courses;

select *
from mainapp_accounts;

select *
from mainapp_accounts_clients;

select *
from mainapp_cards;

-- insert currencies
insert into mainapp_currencies(id, code)
values (1, 'BYN'),
       (2, 'USD'),
       (3, 'EUR');

insert into mainapp_courses(course_buy, course_sale, currency_id, change_time)
values (1000000, 1000000, 1, now()),
       (2515000, 2525000, 2, now()),
       (2845000, 2855000, 3, now());


insert into mainapp_templates(description, other_iban, info_label)
values ('Send to account МТС', 'BY51MMBN30120086600109330000', 'Number of phone'),
       ('Send to other account', null, 'Message');


-- delete
delete
from mainapp_cards;

delete
from mainapp_accounts_clients;

delete
from mainapp_accounts;

-- delete
-- from mainapp_courses;
--
-- delete
-- from mainapp_currencies;

delete
from mainapp_clients;

delete
from auth_user
where is_superuser = false;

