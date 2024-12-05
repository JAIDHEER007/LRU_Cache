import sys
import math

class CacheSimulator:
    def __init__(self, cache_size, line_size, ways):
        if cache_size <= 0 or line_size <= 0 or ways <= 0:
            raise ValueError("Cache size, line size, and ways must be positive integers.")
        if cache_size % line_size != 0:
            raise ValueError("Cache size must be a multiple of line size.")
        
        self.cache_size = cache_size
        self.line_size = line_size
        self.ways = ways
        
        self.num_lines = cache_size // line_size
        if self.num_lines < ways:
            raise ValueError("Number of lines in cache cannot be less than the number of ways.")
        
        self.num_sets = self.num_lines // ways
        if self.num_sets <= 0:
            raise ValueError("Number of sets must be greater than zero.")
        
        self.lines_per_set = self.ways
        self.simulator = self._create_cache()
        self.hit_count = 0
        self.miss_count = 0
        self.access_counter = 0  

    def _create_cache(self):
        cache = []
        for _ in range(self.num_sets):
            cache.append([
                {'tag': -1, 'valid': 0, 'last_access': -1, 'dirty': False} for _ in range(self.lines_per_set)
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
        cache_set = self.simulator[set_index]
        
        # Check for a hit
        for line in cache_set:
            if line['valid'] and line['tag'] == tag:
                self.hit_count += 1
                line['last_access'] = self.access_counter
                self.access_counter += 1

                # Handle write operation for a write-back policy
                if access_type == "W":
                    line['dirty'] = True  # Mark the line as modified
                return "HIT"
        
        # Handle a miss
        self.miss_count += 1
        # Find an empty line or the least recently used line
        lru_line = min(cache_set, key=lambda x: x['last_access'] if x['valid'] else -1)
        
        # Write-back policy: Write dirty data back to memory if replacing
        if lru_line['valid'] and lru_line['dirty']:
            self.write_back_to_memory(lru_line)  # Placeholder for memory write-back logic
        
        # Replace the cache line
        lru_line['tag'] = tag
        lru_line['valid'] = 1
        lru_line['last_access'] = self.access_counter
        self.access_counter += 1

        # Handle write operation
        if access_type == "W":
            lru_line['dirty'] = True  # Mark the line as modified
        else:
            lru_line['dirty'] = False  # Not dirty for read operations

        return "MISS"

    def write_back_to_memory(self, cache_line):
        
        print("Writing back dirty data for tag {} to memory.".format(cache_line['tag']))

    def calculate_miss_rate(self):
        total_accesses = self.hit_count + self.miss_count
        if total_accesses == 0:
            return 0.0
        return (self.miss_count / total_accesses) * 100


def main():
    if len(sys.argv) < 5:
        print("Usage: python3 cache_simulator.py <trace_file> <cache_size> <line_size> <ways>")
        sys.exit(1)
    try:
        trace_file = sys.argv[1]
        cache_size = int(sys.argv[2])
        line_size = int(sys.argv[3])
        ways = int(sys.argv[4])
    except ValueError:
        print("Error: Cache size, line size, and ways must be integers.")
        sys.exit(1)

    # Ensure valid configurations
    if cache_size <= 0 or line_size <= 0 or ways <= 0 or cache_size % line_size != 0:
        print("Error: Invalid cache configuration.")
        sys.exit(1)
    
    simulator = CacheSimulator(cache_size, line_size, ways)
    
    try:
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
        print("Error: File {} not found.".format(trace_file))
        sys.exit(1)

    miss_rate = simulator.calculate_miss_rate()
    print("Cache miss rate: {:.2f}%".format(miss_rate))

if __name__ == "__main__":
    main()
