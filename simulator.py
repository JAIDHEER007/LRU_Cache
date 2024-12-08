import sys
import math

class CLRP:
    @staticmethod
    def replacement_policy(policy, cache_set):
        if policy == "LRU":
            return min(cache_set, key=lambda x: x['last_access'] if x['valid'] else -1)
        elif policy == "LFU":
            return min(cache_set, key=lambda x: x['access_count'] if x['valid'] else -1)
        elif policy == "FIFO":
            return min(cache_set, key=lambda x: x['insert_time'] if x['valid'] else -1)
        else:
            raise ValueError("Unsupported replacement policy: {}".format(policy))

class CacheSimulator:
    def __init__(self, cache_size, line_size, ways, replacement_policy="LRU"):
        if cache_size <= 0 or line_size <= 0 or ways <= 0:
            raise ValueError("Cache size, line size, and ways must be positive integers.")
        if cache_size % line_size != 0:
            raise ValueError("Cache size must be a multiple of line size.")
        
        self.cache_size = cache_size
        self.line_size = line_size
        self.ways = ways
        self.replacement_policy = replacement_policy
        
        self.num_lines = cache_size // line_size
        if self.num_lines < ways:
            raise ValueError("Number of lines in cache cannot be less than the number of ways.")
        
        self.num_sets = self.num_lines // ways
        if self.num_sets <= 0:
            raise ValueError("Number of sets must be greater than zero.")
        
        self.lines_per_set = self.ways
        self.cache_block = self._create_cache()
        self.hit_count = 0
        self.miss_count = 0
        self.access_counter = 0  # For LRU
        self.global_insert_time = 0  # For FIFO

    def _create_cache(self):
        cache = []
        for _ in range(self.num_sets):
            cache.append([
                {
                    'tag': -1,
                    'valid': 0,
                    'last_access': -1,  # For LRU
                    'access_count': 0,  # For LFU
                    'insert_time': -1,  # For FIFO
                    'dirty': False      # For write-back policy
                } for _ in range(self.lines_per_set)
            ])
        return cache

    def _extract_fields(self, address):
        offset_bits = int(math.log2(self.line_size))
        index_bits = int(math.log2(self.num_sets))
        
        mem_offset = address & (self.line_size - 1)
        set_index = (address >> offset_bits) & (self.num_sets - 1)
        tag = address >> (offset_bits + index_bits)
        
        return tag, set_index, mem_offset

    def access_cache(self, address, access_type):
        tag, set_index, _ = self._extract_fields(address)
        cache_set = self.cache_block[set_index]
        
        # Check for a hit
        for line in cache_set:
            if line['valid'] and line['tag'] == tag:
                self.hit_count += 1
                line['last_access'] = self.access_counter  # Update for LRU
                line['access_count'] += 1  # Increment for LFU
                self.access_counter += 1

                if access_type == "W":
                    line['dirty'] = True
                return "HIT"
        
        # Handle a miss
        self.miss_count += 1

        # Find a line to replace using the specified replacement policy
        replacement_line = CLRP.replacement_policy(self.replacement_policy, cache_set)

        # Write-back policy: Write dirty data back to memory if replacing
        if replacement_line['valid'] and replacement_line['dirty']:
            self.write_back_to_memory(replacement_line)

        # Replace the cache line
        replacement_line['tag'] = tag
        replacement_line['valid'] = 1
        
        replacement_line['last_access'] = self.access_counter  # Update for LRU
        replacement_line['access_count'] = 1  # Reset for LFU
        replacement_line['insert_time'] = self.global_insert_time  # Update for FIFO

        self.access_counter += 1
        self.global_insert_time += 1

        if access_type == "W":
            replacement_line['dirty'] = True
        else:
            replacement_line['dirty'] = False

        return "MISS"

    def write_back_to_memory(self, cache_line):
        # Code to write to memory can be included here
        pass

    def calculate_miss_rate(self):
        """Calculates and returns the cache miss rate."""
        total_accesses = self.hit_count + self.miss_count
        if total_accesses == 0:
            return 0.0
        return (self.miss_count / total_accesses) * 100
    
    def simulate_cache(self, trace_file):
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
                
                self.access_cache(address, access_type)

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 cache_simulator.py <trace_file> <cache_size> <line_size> <ways> <replacement_policy>")
        sys.exit(1)
    try:
        trace_file = sys.argv[1]
        cache_size = int(sys.argv[2])
        line_size = int(sys.argv[3])
        ways = int(sys.argv[4])
        replacement_policy = sys.argv[5]
    except ValueError:
        print("Error: Cache size, line size, and ways must be integers.")
        sys.exit(1)

    # Ensure valid configurations
    if cache_size <= 0 or line_size <= 0 or ways <= 0 or cache_size % line_size != 0:
        print("Error: Invalid cache configuration.")
        sys.exit(1)
    
    try:
        simulator = CacheSimulator(cache_size, line_size, ways, replacement_policy)
        simulator.simulate_cache(trace_file = trace_file)
        miss_rate = simulator.calculate_miss_rate()
        print("Cache miss rate: {:.2f}%".format(miss_rate))
    except Exception as exp:
        print("Caught an Exception!", exp)
        sys.exit(1)
    
if __name__ == "__main__":
    main()
