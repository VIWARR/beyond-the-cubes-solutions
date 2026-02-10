-- Плоская таблица факта
create table public.cost_transactions (
	transaction_id bigserial primary key,
	transaction_date date not null,
	cost_center varchar(100) not null,
	receiver_cost_center varchar(100) not null,
	cost_object varchar(100) not null,
	cost_type varchar(10) not null check (cost_type in ('Internal', 'External')),
	cost_category varchar(50),
	amount numeric(14, 2) not null check (amount >= 0),
	allocation_basis varchar(50),
	created_at timestamp not null default now()
);

-- Индекс для cost_transactions
create index idx_transactions_date on cost_transactions(transaction_date);

-- Служебная таблица
create table calculation_tasks (
	id serial primary key,
	target_month date not null unique,
	status varchar(20) not null default 'pending',
	error_message text,
	updated_at timestamp default now()
);

-- Таблица с управленческой себестоимостью
create table cost_center_allocated(
	month date not null,
	cost_center varchar(100) not null,
	total_cost numeric(14,2) not null,
	updated_at timestamp not null default now(),
	primary key(month, cost_center)
);