create or replace view v_external_costs as
select 
	transaction_date,
	cost_center,
	cost_object,
	amount
from cost_transactions
where cost_type = 'External';

create or replace view v_internal_costs as
select
	transaction_date,
	cost_center,
	cost_object,
	amount,
	allocation_basis
from cost_transactions
where cost_type = 'Internal';
