import psutil
import time
from datasets import load_dataset
from threading import Thread


def monitor_resources_during_execution(func, interval=1):
    """
    Monitors resources during the execution of a function in the same process.

    Args:
        func (callable): Function to execute and monitor.
        interval (int): Interval in seconds for resource monitoring.

    Returns:
        result: Result of the executed function.
        resource_usage: Dictionary with monitored resource usage stats.
    """
    process = psutil.Process()
    cpu_usage = []
    memory_usage = []
    network_before = psutil.net_io_counters()

    def resource_monitor():
        while not stop_monitoring:
            cpu_usage.append(process.cpu_percent(interval=0))
            memory_usage.append(process.memory_info().rss / 1024 ** 2)
            time.sleep(interval)

    # Start resource monitoring in a separate thread
    stop_monitoring = False
    monitor_thread = Thread(target=resource_monitor)
    monitor_thread.start()

    # Execute the function
    start_time = time.time()
    result = func()
    execution_time = time.time() - start_time

    # Stop monitoring and wait for the thread to finish
    stop_monitoring = True
    monitor_thread.join()

    network_after = psutil.net_io_counters()
    sent_bytes = (network_after.bytes_sent - network_before.bytes_sent) / 1024 ** 2
    recv_bytes = (network_after.bytes_recv - network_before.bytes_recv) / 1024 ** 2

    resource_usage = {
        "avg_cpu_usage": sum(cpu_usage) / len(cpu_usage) if cpu_usage else 0,
        "peak_memory_usage": max(memory_usage) if memory_usage else 0,
        "network_sent_mb": sent_bytes,
        "network_recv_mb": recv_bytes,
        "total_execution_time": execution_time,
    }

    return result, resource_usage


def validate_dataset(dataset_name, config_name):
    try:
        dataset = load_dataset(dataset_name, config_name, split="train", streaming=True)
        first_sample = next(iter(dataset))
        if "instruction" not in first_sample:
            raise ValueError("Dataset does not contain 'instruction' field.")
    except Exception as e:
        raise ValueError(f"Dataset validation failed: {str(e)}")


def search_prompts_direct(query, dataset_name, config_name, batch_size=1000, max_results=5, chunk_size=5000):
    validate_dataset(dataset_name, config_name)
    results = []
    seen_instructions = set()
    dataset = load_dataset(dataset_name, config_name, split="train", streaming=True)

    batch_instructions = []
    total_processed = 0
    chunk_processed = 0

    for sample in dataset:
        instruction = sample.get("instruction", None)
        if instruction:
            batch_instructions.append(instruction)
            total_processed += 1
            chunk_processed += 1

        if len(batch_instructions) >= batch_size or chunk_processed >= chunk_size:
            for instruction in batch_instructions:
                if query.lower() in instruction.lower() and instruction not in seen_instructions:
                    results.append(instruction)
                    seen_instructions.add(instruction)
                    if len(results) >= max_results:
                        return results

            batch_instructions = []
            chunk_processed = 0

    return results


def search_prompts_with_monitoring(
    query,
    dataset_name,
    config_name,
    batch_size=1000,
    max_results=5,
    chunk_size=5000,
    monitor_interval=1,
):
    def target_function():
        return search_prompts_direct(query, dataset_name, config_name, batch_size, max_results, chunk_size)

    results, resource_usage = monitor_resources_during_execution(target_function, interval=monitor_interval)
    return results, resource_usage


