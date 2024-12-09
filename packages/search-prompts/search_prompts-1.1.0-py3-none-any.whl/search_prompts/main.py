import psutil
import time
from memory_profiler import memory_usage
from datasets import load_dataset

def monitor_resources(duration, interval=1):
    process = psutil.Process()
    cpu_usage = []
    memory_usage = []
    network_before = psutil.net_io_counters()
    
    start_time = time.time()
    while time.time() - start_time < duration:
        cpu_usage.append(process.cpu_percent(interval=0))
        memory_usage.append(process.memory_info().rss / 1024 ** 2)
        time.sleep(interval)
    
    network_after = psutil.net_io_counters()
    sent_bytes = (network_after.bytes_sent - network_before.bytes_sent) / 1024 ** 2
    recv_bytes = (network_after.bytes_recv - network_before.bytes_recv) / 1024 ** 2
    
    return {
        "avg_cpu_usage": sum(cpu_usage) / len(cpu_usage),
        "peak_memory_usage": max(memory_usage),
        "network_sent_mb": sent_bytes,
        "network_recv_mb": recv_bytes,
    }

def validate_dataset(dataset_name, config_name):
    try:
        dataset = load_dataset(dataset_name, config_name, split="train", streaming=True)
        first_sample = next(iter(dataset))
        if "instruction" not in first_sample:
            raise ValueError("Dataset does not contain 'instruction' field.")
    except Exception as e:
        raise ValueError(f"Dataset validation failed: {str(e)}")

def search_prompts_with_monitoring(
    query,
    dataset_name,
    config_name,
    batch_size=1000,
    max_results=5,
    chunk_size=5000,
    monitor_interval=1,
):
    start_time = time.time()
    search_results = []
    monitor_duration = 0

    def target_function():
        nonlocal monitor_duration, search_results
        start_monitor = time.time()
        search_results = search_prompts_direct(
            query, dataset_name, config_name, batch_size, max_results, chunk_size
        )
        monitor_duration = time.time() - start_monitor

    memory_profile = memory_usage(target_function, interval=monitor_interval)
    resource_usage = monitor_resources(monitor_duration, interval=monitor_interval)

    end_time = time.time()
    resource_usage.update(
        {
            "total_execution_time": end_time - start_time,
            "memory_profile": memory_profile,
        }
    )

    return search_results, resource_usage

def search_prompts_direct(
    query,
    dataset_name,
    config_name,
    batch_size=1000,
    max_results=5,
    chunk_size=5000,
):
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
