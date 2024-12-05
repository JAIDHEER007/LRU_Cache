import os
import time
import itertools
import matplotlib.pyplot as plt
from datetime import datetime
from simulator import CacheSimulator  # Assuming CacheSimulator is in a file named cache_simulator.py

def create_img_dir():
    img_dir = "img"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sub_dir = os.path.join(img_dir, timestamp)

    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)

    return sub_dir

def test_cache_simulator(trace_file, cache_sizes, line_sizes, ways):
    """
    Test CacheSimulator with all permutations of cache_sizes, line_sizes, and ways.

    Args:
        trace_file (str): Path to the memory trace file.
        cache_sizes (list): List of cache sizes to test.
        line_sizes (list): List of line sizes to test.
        ways (list): List of associativities (ways) to test.
    """
    # Prepare output directory
    img_dir = create_img_dir()

    results = []

    # Test all permutations of cache sizes, line sizes, and ways
    for cache_size, line_size, way in itertools.product(cache_sizes, line_sizes, ways):
        print(f"Testing with Cache Size: {cache_size}, Line Size: {line_size}, Ways: {way}")
        start_time = time.time()
        try:
            simulator = CacheSimulator(cache_size, line_size, way)
            with open(trace_file, "r") as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("#") or line == "":
                        continue

                    fields = line.split()
                    if len(fields) != 3:
                        continue

                    try:
                        address = int(fields[2], 16)
                        access_type = fields[1]
                        if access_type not in ("R", "W"):
                            continue
                    except ValueError:
                        continue

                    simulator.access_cache(address, access_type)
        except FileNotFoundError:
            print(f"Error: File {trace_file} not found.")
            return
        except ValueError as exp:
            print(exp)
            continue

        end_time = time.time()

        miss_rate = simulator.calculate_miss_rate()
        exec_time = end_time - start_time
        results.append((cache_size, line_size, way, miss_rate, exec_time))
        print(f"Miss Rate: {miss_rate:.2f}%, Time Taken: {exec_time:.2f} seconds")

    # Plot results
    plot_results(results, img_dir, trace_file)


def plot_results(results, img_dir, trace_file):
    """
    Plot cache miss rates and execution times.

    Args:
        results (list): List of tuples with (cache_size, line_size, ways, miss_rate, exec_time).
        img_dir (str): Directory to save the plots.
    """
    # Prepare data for plotting
    configs = ["Cache Size:{} Line Size:{} Ways:{}".format(r[0], r[1], r[2]) for r in results]
    miss_rates = [r[3] for r in results]
    exec_times = [r[4] for r in results]

    # Plot Cache Miss Rates
    plt.figure(figsize=(12, 6))
    plt.plot(configs, miss_rates, marker='o', label="Cache Miss Rate")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Cache Configurations")
    plt.ylabel("Cache Miss Rate (%)")
    plt.title("Cache Miss Rates for Different Configurations for {trace_file}".format(trace_file = trace_file))
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, "cache_miss_rate.png"))
    plt.close()

    # Plot Execution Times
    plt.figure(figsize=(12, 6))
    plt.plot(configs, exec_times, marker='o', label="Execution Time", color="orange")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Cache Configurations")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time for Different Configurations for {trace_file}".format(trace_file = trace_file))
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, "execution_time.png"))
    plt.close()


if __name__ == "__main__":
  
    # test case 1

    trace_file = "1KB_64B"  
    cache_sizes = [1024, 2048, 4096]  
    line_sizes = [64]  
    ways = [16]  

    test_cache_simulator(trace_file, cache_sizes, line_sizes, ways)

    print("test case 1 success!")

    # test case 2

    trace_file = "32MB_4B"  
    cache_sizes = [1024, 2048, 4096, 4194304]  
    line_sizes = [64]  
    ways = [16]  

    test_cache_simulator(trace_file, cache_sizes, line_sizes, ways)

    print("test case 2 success!")

