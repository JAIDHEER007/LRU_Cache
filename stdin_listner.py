import sys
from simulator import CacheSimulator

def process_trace_stream(cache_size, line_size, ways, replacement_policy):
    """
    Processes the memory trace stream from stdin and simulates the cache.

    Args:
        cache_size (int): Total cache size in bytes.
        line_size (int): Cache line size in bytes.
        ways (int): Number of associativity ways.
        replacement_policy (str): Cache replacement policy (e.g., "LRU", "FIFO", "LFU").
    """
    simulator = CacheSimulator(cache_size, line_size, ways, replacement_policy)

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fields = line.split()
            if len(fields) != 3:
                continue
            try:
                address = int(fields[2], 16)
                access_type = fields[1]
                if access_type not in ("R", "W"):
                    continue
                simulator.access_cache(address, access_type)
            except ValueError:
                continue
    except KeyboardInterrupt:
        pass  

    # Print final cache miss rate
    miss_rate = simulator.calculate_miss_rate()
    print("Cache miss rate: {miss_rate:.2f}%".format(miss_rate = miss_rate))

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 server.py <cache_size> <line_size> <ways> <replacement_policy>")
        sys.exit(1)

    try:
        # Parse command-line arguments
        cache_size = int(sys.argv[1])
        line_size = int(sys.argv[2])
        ways = int(sys.argv[3])
        replacement_policy = sys.argv[4]
    except ValueError:
        print("Error: cache_size, line_size, and ways must be integers.")
        sys.exit(1)

    print("Processing trace data from stdin...")
    print("Cache_size", cache_size)
    print("Line_size", line_size)
    print("ways", ways)
    print("Replacement_Policy", replacement_policy)

    process_trace_stream(cache_size, line_size, ways, replacement_policy)