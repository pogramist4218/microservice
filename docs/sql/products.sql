-- auto-generated definition
create table products
(
    id    serial           not null
        constraint products_pk
            primary key,
    name  varchar(500)     not null,
    price double precision not null
);

alter table products
    owner to pogramist;

create unique index products_id_uindex
    on products (id);

