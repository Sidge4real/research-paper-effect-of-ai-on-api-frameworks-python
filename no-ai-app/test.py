import httpx
import time
import psutil
from concurrent.futures import ThreadPoolExecutor
import threading
import matplotlib.pyplot as plt
import os
import asyncio

FRAMEWORK_PORTS = {
    'flask': 5000,
    'fastapi': 8001,
    'django': 8000
}

# Synchrone versie voor Flask en Django
def test_endpoint_sync(framework, endpoint, method='GET', payload=None):
    base_url = f"http://localhost:{FRAMEWORK_PORTS[framework]}/{endpoint}"
    
    try:
        with httpx.Client() as client:
            start = time.time()
            if method == 'GET':
                response = client.get(base_url)
            elif method == 'POST':
                response = client.post(base_url, json=payload)
            latency = (time.time() - start) * 1000  # ms
            
            return {
                'status': response.status_code,
                'latency': latency,
                'framework': framework,
                'success': True
            }
    except Exception as e:
        return {
            'status': None,
            'latency': None,
            'framework': framework,
            'success': False,
            'error': str(e)
        }

# Asynchrone versie voor FastAPI
async def test_endpoint_async(framework, endpoint, method='GET', payload=None):
    base_url = f"http://localhost:{FRAMEWORK_PORTS[framework]}/{endpoint}"
    
    try:
        async with httpx.AsyncClient() as client:
            start = time.time()
            if method == 'GET':
                response = await client.get(base_url)
            elif method == 'POST':
                response = await client.post(base_url, json=payload)
            latency = (time.time() - start) * 1000  # ms
            
            return {
                'status': response.status_code,
                'latency': latency,
                'framework': framework,
                'success': True
            }
    except Exception as e:
        return {
            'status': None,
            'latency': None,
            'framework': framework,
            'success': False,
            'error': str(e)
        }

# Functie voor het monitoren van de eigen Python-processen (CPU-gebruik)
def start_process_monitor(stop_event, interval=0.5):
    mem_samples = []
    process = psutil.Process()

    def monitor():
        while not stop_event.is_set():
            mem_samples.append(process.memory_info().rss / (1024 * 1024))
            time.sleep(interval)

    thread = threading.Thread(target=monitor)
    thread.start()
    return [], mem_samples, thread

# Run benchmark, aangepast voor FastAPI als asynchroon
def run_benchmark(concurrent_users=100, requests_per_user=10):
    results = {}
    for framework in ['flask', 'fastapi', 'django']:
        print(f"\nBenchmarking {framework}...")
        start_time = time.time()

        # Start monitoring van het proces
        stop_event = threading.Event()
        cpu_samples, mem_samples, monitor_thread = start_process_monitor(stop_event)

        if framework == 'fastapi':
            # Asynchrone benadering voor FastAPI
            loop = asyncio.get_event_loop()
            futures = [loop.create_task(test_endpoint_async(framework, 'posts')) 
                      for _ in range(requests_per_user * concurrent_users)]
            
            responses = loop.run_until_complete(asyncio.gather(*futures))
        else:
            # Synchrone benadering voor Flask en Django
            with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
                futures = [executor.submit(test_endpoint_sync, framework, 'posts') 
                          for _ in range(requests_per_user * concurrent_users)]
                
                responses = [f.result() for f in futures]
        
        stop_event.set()
        monitor_thread.join()

        total_time = time.time() - start_time
        
        # Filter succesvolle verzoeken
        successful_responses = [r for r in responses if r['success']]
        failed_responses = len(responses) - len(successful_responses)
        
        if successful_responses:
            latencies = [r['latency'] for r in successful_responses]
            results[framework] = {
                'requests_per_second': round(len(successful_responses) / total_time, 2),
                'avg_latency_ms': round(sum(latencies) / len(latencies), 2),
                'min_latency_ms': round(min(latencies), 2),
                'max_latency_ms': round(max(latencies), 2),
                'failed_requests': failed_responses,
                'memory_usage_mb': round(sum(mem_samples) / len(mem_samples), 2),
                'total_time': round(total_time, 2)
            }
        else:
            results[framework] = {
                'error': 'All requests failed',
                'failed_requests': failed_responses
            }
    
    return results

# Display the results
def display_results(results):
    print("\nBenchmark Results:") 
    print("-" * 80)
    
    # Maak map voor resultaten indien niet bestaand
    if not os.path.exists('results'):
        os.makedirs('results')

    # Verzameling van data voor grafieken
    frameworks = ['flask', 'fastapi', 'django']
    requests_per_second = [results[framework].get('requests_per_second', 0) for framework in frameworks]
    avg_latency_ms = [results[framework].get('avg_latency_ms', 0) for framework in frameworks]
    total_time = [results[framework].get('total_time', 0) for framework in frameworks]
    memory_usage_mb = [results[framework].get('memory_usage_mb', 0) for framework in frameworks]

    i = 0
    for f in frameworks:
        if i == 0:
            print("flask:")
        elif i == 1:
            print("fastapi:")
        elif i == 2:
            print("django:")
        
        print("req/s: " + str(requests_per_second[i]))
        print("latency: " + str(avg_latency_ms[i]) + "ms")
        print("total time: " + str(total_time[i]) + "s")
        print("memory: " + str(memory_usage_mb[i]) + "MB")
        print()
        
        i += 1

    # Sla gecombineerde grafieken op
    save_comparison_graph('Requests per second', frameworks, requests_per_second, 'requests_per_second')
    save_comparison_graph('Average Latency (ms)', frameworks, avg_latency_ms, 'avg_latency')
    save_comparison_graph('Total Time (s)', frameworks, total_time, 'total_time')
    save_comparison_graph('Memory Usage (MB)', frameworks, memory_usage_mb, 'memory_usage')

def save_comparison_graph(title, frameworks, data, filename):
    # Gecombineerde grafiek voor de drie frameworks
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.bar(frameworks, data, color=['skyblue', 'lightgreen', 'salmon'])
    ax.set_ylabel(title)
    ax.set_title(f'{title} Comparison')
    plt.tight_layout()
    plt.savefig(f"results/{filename}.png")
    plt.close(fig)

if __name__ == '__main__':
    results = run_benchmark(concurrent_users=50, requests_per_user=2)
    display_results(results)
