create table public.cost_transactions (
	transaction_id bigserial primary key,
	transaction_date date not null,
	cost_center varchar(100) not null,
	cost_object varchar(100) not null,
	cost_type varchar(10) not null check (cost_type in ('Internal', 'External')),
	cost_category varchar(50),
	amount numeric(14, 2) not null check (amount >= 0),
	allocation_basis varchar(50),
	created_at timestamp not null default now()
);

create table cost_center_allocated(
	month date not null,
	cost_center varchar(100) not null,
	total_cost numeric(14,2) not null,
	updated_at timestamp not null default now()
	primary key(month, cost_center)
);