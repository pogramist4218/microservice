create table if not exists users
(
	id serial not null
		constraint users_pk
			primary key,
	name varchar(255) not null,
	surname varchar(255) not null,
	sex varchar(1) not null,
	birth_date date not null
);

alter table users owner to pogramist;

create unique index if not exists users_id_uindex
	on users (id);