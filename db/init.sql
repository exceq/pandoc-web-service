-- auto-generated definition
create table users
(
    id      bigserial
        constraint users_pk
            primary key,
    username varchar(255) unique not null,
    created timestamp default now()
);

alter table users
    owner to myuser;
