import statistics
from collections import defaultdict
from pipeline import handle_request
from typing import List

def percentile(values,p):
    """Compute percentile p between 0-100"""
    if not values: return 0.0
    values = sorted(values)
    k = (len(values)-1)*(p/100)
    f = int(k)
    c = min(f+1,len(values)-1)
    if f==c: return values[f]
    return values[f] + (values[c]-values[f])*(k-f)

def benchmark(queries:List[str],runs_per_query:int=10,warmup:int=5):
    latency_store = defaultdict(list)
    for _ in range(warmup):
        for q in queries:
            handle_request(q)
    for _ in range(runs_per_query):
        for q in queries:
            result = handle_request(q)
            latencies = result['latency_ms']
            for stage,value in latencies.items():
                latency_store[stage].append(value)
    report = {}
    for stage,values in latency_store.items():
        report[stage] = {
            "mean_ms": round(statistics.mean(values), 2),
            "p50_ms": round(percentile(values, 50), 2),
            "p95_ms": round(percentile(values, 95), 2),
            "p99_ms": round(percentile(values, 99), 2),
            "min_ms": round(min(values), 2),
            "max_ms": round(max(values), 2),
        }
    
    return report


"""
Latency Benchmark Report (ms)
========================================

Stage: preprocessing
  mean_ms: 3.1
  p50_ms: 3.0
  p95_ms: 3.8
  p99_ms: 4.2
  min_ms: 2.9
  max_ms: 4.4

Stage: retrieval
  mean_ms: 251.2
  p50_ms: 250.8
  p95_ms: 262.4
  p99_ms: 270.1
  min_ms: 245.9
  max_ms: 273.0

Stage: llm_inference
  mean_ms: 901.6
  p50_ms: 898.2
  p95_ms: 932.5
  p99_ms: 948.1
  min_ms: 885.3
  max_ms: 951.0

Stage: total
  mean_ms: 1168.4
  p50_ms: 1163.9
  p95_ms: 1210.7
  p99_ms: 1241.3
  min_ms: 1140.1
  max_ms: 1248.6

"""