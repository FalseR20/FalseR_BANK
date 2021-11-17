-- #1 таблица с клиентами
create table clients
(
    id       serial primary key,
    login    char(64) not null,
    password char(64) not null,
    name     char(30) not null
);
drop table clients;


-- #2 справочник с валютами
create table currencies
(
    code   char(3) primary key, -- ISO 4217
    name   char(30) null,
    symbol char     null
        check (name notnull or symbol notnull)
);
drop table currencies;


-- #3 таблица с курсами валют
create table courses
(
    id          bigserial primary key,
    currency    char(3)   not null REFERENCES currencies (code),
    course_buy  bigint    not null, -- in BYN  надо же
    course_sale bigint    not null, -- in BYN  процентики забирать
    change_time timestamp not null
);
drop table courses;


-- #4 таблица со счетами
create table accounts
(
    id       serial primary key,
    currency char(3)        not null references currencies (code),
    balance  decimal(20, 2) not null
);
drop table accounts;


-- #5 таблица доступа клиентов к счетам (для реализации many-to-many)
create table access
(
    person_id  serial not null references clients (id),
    account_id serial not null references accounts (id)
);
drop table access;


-- #6 таблица с картами
CREATE TABLE cards
(
    number          bigint primary key,
    cardholder_name char(30) not null,
    expiration_date date     not null,
    security_code   int      not null,
    account_id      serial   not null references accounts (id),
    cardholder_id   serial   not null references clients (id)
);
drop table cards;


-- #7 таблица с транзакциями
CREATE TABLE transactions
(
    id            serial primary key,
    description   char(50)       not null,
    time          timestamp      not null,
    sender        serial         not null references clients (id),
    receiver      serial         not null references clients (id),
    currency      char(3)        not null,
    value         decimal(20, 2) not null,
    commission    decimal(20, 2) not null,
    is_successful bool           not null default true
);
drop table transactions;
