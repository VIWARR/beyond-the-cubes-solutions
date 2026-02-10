import logging
from app.db.repository import TaskRepository, DataRepository
from app.services.calculator import ReciprocalCalculator

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self, db_session):
        self.db = db_session
        self.tasks = TaskRepository(db_session)
        self.data = DataRepository(db_session)
        self.calc = ReciprocalCalculator()

    def process_pending_tasks(self):
        task = self.tasks.get_next_pending()
        if not task:
            return
        
        try:
            logger.info(f"Начат расчет за {task.target_month}")
            self.tasks.update_status(task, 'processing')

            ext_costs = self.data.get_external_by_month(task.target_month)
            int_costs = self.data.get_internal_by_month(task.target_month)

            results = self.calc.solve(ext_costs, int_costs)

            self.data.save_results(task.target_month, results)
            self.tasks.update_status(task, 'completed')
            logger.info(f"Управленческая себестоимость расчитана за: {task.target_month}")

        except Exception as e:
            logger.exception("Ошибка в расчете")
            self.tasks.update_status(task, 'error', str(e))