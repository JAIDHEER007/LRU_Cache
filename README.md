Group 9: Jaidheer Sirigineedi, Anshu Tripathi, G Mary Spandana

# Cache Simulator Project


**Project Objective:**

This project aims to design and implement a cache simulator that models the behavior of set-associative caches using the Least Recently Used (LRU) replacement policy. The simulator provides an opportunity to understand the internal mechanisms of CPU caches and the design process in computer architecture. By simulating the memory access patterns from trace files, the project enables experimentation with various cache configurations, such as size and associativity, to analyze their impact on cache miss rates.


**Implementation:**

We developed a Bash script named “run_sim.sh” to allow input of the filename. This script enables the simulator to read various parameters, including numberOfWays, cacheLineSizeInBytes, and cacheSizeInBytes. During our experiments, we tested several cache sizes, with the default value for cacheSizeInBytes set to 32,768 bytes. However, this parameter can be adjusted to meet different requirements. The Bash script calls the Python-based simulator and passes the specified parameters, streamlining the configuration and execution processes.

**Experiment:**

All trace files on the professor's SharePoint were extracted and utilized as part of the experimental process. We passed the file names of these trace files as parameters to the run_sim.sh Bash script to execute the cache simulator. For the experiments, various cache sizes and replacement policies (“LRU,” “FIFO,” and “LFU) were selected and tested.

**Result:**

Among the tested trace files, the gcc.trace.txt file achieved a commendable balance between performance and resource efficiency. With a cache size of 32 KB, line size of 64 bytes, and 16-way associativity, it achieved a cache miss rate of 1.89% and a total execution time of 0.368 seconds. Despite using a smaller cache size, this configuration demonstrated efficient memory access patterns and minimized execution overhead, making it a practical and resource-conscious choice.
