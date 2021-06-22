create table if not exists purchase
(
	id serial not null
		constraint purchase_pk
			primary key,
	user_id integer not null
		constraint purchase_users_id_fk
			references users
				on update cascade on delete cascade,
	product_id integer not null
		constraint purchase_products_id_fk
			references products
				on update cascade on delete cascade,
	purchase_date date not null
);

alter table purchase owner to pogramist;

create unique index if not exists purchase_id_uindex
	on purchase (id);

