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

-- insert
insert into auth_user (id, password,
                       last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active,
                       date_joined)
values (2, 'pbkdf2_sha256$260000$YkxSHJo8XMWgo7J4eaQG8a$cypE3PjwEw2HIrmphX/vStANs3a5HJH2L7/fwOEkagk=',
        '2021-11-28 17:53:02.911059 +00:00', false, 'user-test', '', '', '', false, true,
        '2021-11-28 17:29:46.858871 +00:00');

insert into mainapp_clients (id, fullname, user_id)
values (1, 'user-test', 2);

insert into mainapp_currencies(id, code)
values (1, 'BYN'),
       (2, 'USD');

insert into mainapp_courses(id, course_buy, course_sale, change_time, currency_id)
values (1, 1000000, 1000000, now(), 1),
       (2, 2500000, 2500000, now(), 2);

insert into mainapp_accounts (id, currency_id, balance)
values (1, 1, 1000);

insert into mainapp_accounts_clients (id, accounts_id, clients_id)
values (1, 1, 1);

insert into mainapp_cards (number, cardholder_name, expiration_date, security_code, account_id, client_id)
values (4000000000000001, 'user-test-cardholder', now(), 123, 1, 1);

insert into mainapp_cards (number, cardholder_name, expiration_date, security_code, account_id, client_id)
values (4000000000000002, 'user-test-cardholder', now(), 123, 1, 1);

-- delete
delete
from mainapp_cards;

delete
from mainapp_accounts_clients;

delete
from mainapp_accounts;

delete
from mainapp_courses;

delete
from mainapp_currencies;

delete
from mainapp_clients;

delete
from auth_user
where is_superuser = false;

