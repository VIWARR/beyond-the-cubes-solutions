import pandas as pd
from sqlalchemy import select, update, text, func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.db.models import CalculationTask, AllocatedCost

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_next_pending(self) -> CalculationTask | None:
        stmt = select(CalculationTask).where(CalculationTask.status == 'pending').limit(1)
        return self.session.execute(stmt).scalar_one_or_none()
    
    def update_status(self, task: CalculationTask, status: str, error_msg: str = None):
        task.status = status
        task.error_message = error_msg
        self.session.add(task)
        self.session.flush()

class DataRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_external_by_month(self, month) -> pd.DataFrame:
        query = "select cost_center, amount from v_external_costs where date_trunc('month', transaction_date) = date_trunc('month', cast(:m as date))"
        return pd.read_sql(text(query), self.session.bind, params={'m': month})
    
    def get_internal_by_month(self, month) -> pd.DataFrame:
        query = "select source_cc, target_cc, amount from v_internal_costs where date_trunc('month', transaction_date) = date_trunc('month', cast(:m as date))"
        return pd.read_sql(text(query), self.session.bind, params={"m": month})
    
    def save_results(self, month, results: dict):
        if not results:
            return
        
        data_to_insert = [
            {
                'month': month,
                'cost_center': cc,
                'total_cost': float(total)
            }
            for cc, total in results.items()
        ]

        stmt = insert(AllocatedCost)

        upsert_stmt = stmt.on_conflict_do_update(
            index_elements=['month', 'cost_center'],
            set_={
                'total_cost': stmt.excluded.total_cost,
                'updated_at': func.now()
            }
        )

        self.session.execute(upsert_stmt, data_to_insert)