import os
import time
import itertools
import csv
import matplotlib.pyplot as plt # type: ignore
from datetime import datetime
from simulator import CacheSimulator 

def create_dir():
    test_dir = "Test_Simulations"
    timestamp = datetime.now().strftime("%Y%m%d_%H_%M_%S_%f")[:-3]  
    sub_dir = os.path.join(test_dir, timestamp)

    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)

    return sub_dir

def save_metrics_to_csv(results, test_dir, trace_file):
    csv_file_path = os.path.join(test_dir, "simulation_metrics.csv")

    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write header
        writer.writerow(["Replacement Policy", "Cache Size", "Line Size", "Ways", "Miss Rate (%)", "Execution Time (seconds)", "Trace File"])
        
        # Write data for each policy
        for policy, data in results.items():
            for entry in data:
                writer.writerow([policy, entry[0], entry[1], entry[2], entry[3], entry[4], trace_file])

    print(f"Metrics saved to {csv_file_path}")


def test_cache_simulator(trace_file, cache_sizes, line_sizes, ways, replacement_policies):
    """
    Test CacheSimulator with all permutations of cache_sizes, line_sizes, and ways for multiple replacement policies.

    Args:
        trace_file (str): Path to the memory trace file.
        cache_sizes (list): List of cache sizes to test.
        line_sizes (list): List of line sizes to test.
        ways (list): List of associativities (ways) to test.
        replacement_policies (list): List of cache replacement policies to test.
    """
    # Prepare output directory
    test_dir = create_dir()

    results = {policy: [] for policy in replacement_policies}

    # Test all permutations for each replacement policy
    for replacement_policy in replacement_policies:
        print(f"Testing Replacement Policy: {replacement_policy}")
        for cache_size, line_size, way in itertools.product(cache_sizes, line_sizes, ways):
            print(f"Testing with Cache Size: {cache_size}, Line Size: {line_size}, Ways: {way}")
            try:
                start_time = time.time()
                simulator = CacheSimulator(cache_size, line_size, way, replacement_policy)
                simulator.simulate_cache(trace_file=trace_file)
                miss_rate = simulator.calculate_miss_rate()
                end_time = time.time()
            except FileNotFoundError:
                print(f"Error: File {trace_file} not found.")
                return
            except ValueError as exp:
                print(exp)
                continue

            exec_time = end_time - start_time
            results[replacement_policy].append((cache_size, line_size, way, miss_rate, exec_time))
            print(f"Miss Rate: {miss_rate:.2f}%, Time Taken: {exec_time:.2f} seconds")

    # Save metrics to CSV File
    save_metrics_to_csv(results, test_dir, trace_file)

    # Plot results
    plot_results(results, test_dir, trace_file)


def plot_results(results, test_dir, trace_file):
    """
    Plot cache miss rates and execution times for multiple replacement policies.

    Args:
        results (dict): Dictionary with replacement policies as keys and results as values.
        test_dir (str): Directory to save the plots.
    """
    # Plot Cache Miss Rates
    plt.figure(figsize=(12, 6))

    # Define a dictionary of markers for each policy
    policy_markers = {
        "LRU": "o",  # Circle
        "LFU": "s",  # Square
        "FIFO": "D",  # Diamond
        # Add more policies and markers as needed
    }

    # Plot the data with unique markers
    for policy, data in results.items():
        configs = ["Cache:{} Line:{} Ways:{}".format(r[0], r[1], r[2]) for r in data]
        miss_rates = [r[3] for r in data]
        marker = policy_markers.get(policy, "o")  # Default to 'o' if policy is not in dictionary
        plt.plot(configs, miss_rates, marker=marker, linestyle='-', label=f"{policy} Miss Rate")

    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Cache Configurations")
    plt.ylabel("Cache Miss Rate (%)")
    plt.title(f"Cache Miss Rates for Different Configurations ({trace_file})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(test_dir, "cache_miss_rate.png"))
    plt.close()

    # Plot Execution Times
    plt.figure(figsize=(12, 6))
    for policy, data in results.items():
        configs = ["Cache:{} Line:{} Ways:{}".format(r[0], r[1], r[2]) for r in data]
        exec_times = [r[4] for r in data]
        marker = policy_markers.get(policy, "o")  # Default to 'o' if policy is not in dictionary
        plt.plot(configs, exec_times, marker=marker, linestyle='-', label=f"{policy} Execution Time")

    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Cache Configurations")
    plt.ylabel("Execution Time (seconds)")
    plt.title(f"Execution Times for Different Configurations ({trace_file})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(test_dir, "execution_time.png"))
    plt.close()


if __name__ == "__main__":
    test_cases = [
        {
            "trace_file": "gcc.trace.txt",
            "cache_sizes": [1024, 2048, 32768, 4194304], 
            "line_sizes": [64, 32, 16], 
            "ways": [16, 8], 
            "replacement_policies": ["LRU", "FIFO", "LFU"]
        }
    ]

    for test_case_index, test_case in enumerate(test_cases):
        print(f"Test Case {test_case_index} Started")
        test_cache_simulator(**test_case)
        print(f"Test Case {test_case_index} Ended")
