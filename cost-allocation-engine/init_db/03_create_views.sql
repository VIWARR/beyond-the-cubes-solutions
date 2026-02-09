-- Представление для внешних расходов
create or replace view v_external_costs as
select transaction_date, cost_center, amount
from cost_transactions where cost_type = 'External';

-- Представление для внутренних расчетов между объектами затрат
create or replace view v_internal_costs as
select transaction_date, cost_center as source_cc, cost_object as target_cc, amount
from cost_transactions where cost_type = 'Internal';