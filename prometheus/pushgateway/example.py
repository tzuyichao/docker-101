from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()
duration = Gauge('my_job_duration_seconds', 'Duration of my batch job in seconds', registry=registry)

if __name__ == '__main__':
    try:
        with duration.time():
            pass

        g = Gauge('my_job_last_success_seconds', 'Last time my batch job successfully finished', registry=registry)
        g.set_to_current_time()
    finally:
        push_to_gateway('localhost:9091', job='batchA', registry=registry)