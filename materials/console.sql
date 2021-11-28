-- #1 таблица с клиентами
create table clients
(
    id        serial primary key,
    login     char(64) not null,
    password  char(64) not null,
    full_name char(64) not null
);
drop table clients;


-- #2 справочник с валютами
create table currencies
(
    id   serial primary key,
    code char(3) not null -- ISO 4217
    -- country char(30) null
);
drop table currencies;


-- #3 таблица с курсами валют
create table courses
(
    id          bigserial primary key,
    currency    int       not null references currencies (id),
    course_buy  bigint    not null, -- in BYN  надо же
    course_sale bigint    not null, -- in BYN  процентики забирать
    change_time timestamp not null default now()
);
drop table courses;


-- #4 таблица со счетами
create table accounts
(
    id       serial primary key,
    currency int            not null references currencies (id),
    balance  decimal(15, 6) not null
);
drop table accounts;


-- #5 таблица доступа клиентов к счетам (для реализации many-to-many)
create table access
(
    person_id  int not null references clients (id),
    account_id int not null references accounts (id)
);
drop table access;


-- #6 таблица с картами
CREATE TABLE cards
(
    number          bigint primary key,
    cardholder_name char(30) not null,
    expiration_date date     not null,
    security_code   int      not null,
    account_id      int      not null references accounts (id),
    cardholder_id   int      not null references clients (id)
);
drop table cards;


-- #7 таблица с шаблонами операций
create table templates
(
    id          serial primary key,
    description char(50) not null,
    sender      int references clients (id),
    receiver    int references clients (id)
);
drop table templates;


-- #8 таблица с транзакциями
CREATE TABLE transactions
(
    id         serial primary key,
    time       timestamp      not null default now(),
    template   int references templates (id),
    sender     int            not null references clients (id),
    receiver   int            not null references clients (id),
    currency   char(3)        not null,
    value      decimal(15, 6) not null,
    commission decimal(15, 6) not null,
    is_active  bool           not null default true
);
drop table transactions;

SELECT username, password, is_superuser from auth_user;

delete from auth_user
where is_superuser = false;