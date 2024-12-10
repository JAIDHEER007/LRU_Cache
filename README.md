Group 9: Jaidheer Sirigineedi, Anshu Tripathi, G Mary Spandana

**Cache Simulator Project**


**Project Objective:**

This project aims to design and implement a cache simulator that models the behavior of set-associative caches using the Least Recently Used (LRU) replacement policy. The simulator provides an opportunity to understand the internal mechanisms of CPU caches and the design process in computer architecture. By simulating the memory access patterns from trace files, the project enables experimentation with various cache configurations, such as size and associativity, to analyze their impact on cache miss rates.


**Implementation:**

We developed a Bash script named “run_sim.sh” to allow input of the filename. This script enables the simulator to read various parameters, including numberOfWays, cacheLineSizeInBytes, and cacheSizeInBytes. During our experiments, we tested several cache sizes, with the default value for cacheSizeInBytes set to 32,768 bytes. However, this parameter can be adjusted to meet different requirements. The Bash script calls the Python-based simulator and passes the specified parameters, streamlining the configuration and execution processes.

