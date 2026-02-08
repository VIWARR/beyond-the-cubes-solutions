create or replace function notify_new_transaction()
returns trigger as $$
begin
	perform pg_notify('transactions_channel', row_to_json(NEW)::text);
return new;
end;
$$ language plpgsql;


create trigger trg_transaction_inseinsert 
after insert on cost_transactions
for each row
execute function notify_new_transaction();