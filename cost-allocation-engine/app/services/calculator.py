import pandas as pd
import numpy as np

class ReciprocalCalculator:
    def solve(self, external_df: pd.DataFrame, internal_df: pd.DataFrame):
        if external_df.empty:
            return {}
        
        all_ccs = sorted(
            list(set(external_df['cost_center']) | 
                 set(internal_df['source_cc']) | 
                 set(internal_df['target_cc']))
        )
        idx = {cc: i for i, cc in enumerate(all_ccs)}
        n = len(all_ccs)

        # Вектор внешних затрат C
        C = np.zeros(n)
        for _, row in external_df.iterrows():
            C[idx[row['cost_center']]] += float(row['amount'])

        # Матрица коэффициентов A
        A = np.zeros((n, n))
        source_totals = internal_df.groupby('source_cc')['amount'].sum()

        for _, row in internal_df.iterrows():
            s_idx = idx[row['source_cc']]
            t_idx = idx[row['target_cc']]
            total = source_totals[row['source_cc']]
            if total > 0:
                A[t_idx, s_idx] = float(row['amount']) / float(total)

        # Решение системы
        try:
            X = np.linalg.solve(np.eye(n) - A, C)
        except np.linalg.LinAlgError:
            raise ValueError("Матрица вырождена: проверьте циклы распределения.")
        
        return {all_ccs[i]: round(X[i], 2) for i in range(n)}