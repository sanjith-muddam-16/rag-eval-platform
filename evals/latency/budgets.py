from typing import Dict, Tuple


class LatencyBudgetViolation(Exception):
    """Raised when a latency budget is violated."""
    pass

class LatencyBudgets:
    """
        Example budgets (ms):
        {
            "preprocessing": 50,
            "retrieval": 300,
            "prompt_build": 100,
            "llm_inference": 1200,
            "total": 1800
        }

    """
    def __init__(self, budgets_ms: Dict[str, float], strict: bool = False):
                """Args:
                    budgets_ms (dict): stage -> max allowed latency in ms
                    strict (bool): if True, raise exception on violation;
                                if False, only report violations"""
                self.budgets_ms = budgets_ms
                self.strict = strict
    def check(self,latency_ms:Dict[str,float])->Tuple[bool,Dict[str,float]]:

        """Check latency against budgets.
        Args:latency_ms (dict): measured latencies from pipeline
        Returns:(ok, violations)
            ok (bool): True if no violations
            violations (dict): stage -> exceeded_by_ms"""
        violations = {}

        for stage,measured in latency_ms.items():
            budget = self.budgets_ms.get(stage)
            if budget is None:continue
            if measured>budget:
                violations[stage] = round(measured - budget, 2)
        if violations and self.strict:
              raise LatencyBudgetViolation(
                f"Latency budget violations: {violations}"
            )
        return len(violations) == 0, violations
            
            
        


