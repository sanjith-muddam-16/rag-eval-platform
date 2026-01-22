import time
from contextlib import contextmanager
from typing import Dict

@contextmanager
def latency_timer(stage:str,metrics:Dict[str,float]):
    """
    Context manager to measure latency(in ms) for the 
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        metrics[stage] = round((end-start)*1000,2)