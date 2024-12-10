#!/bin/bash
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    :
else
    sed -i 's/\r$//' run_sim.sh
fi
if [ $1 = "1KB_64B" ]; then
    python3 simulator.py $1 1048576 64 16 LRU
elif [ $1 = "4MB_4B" ]; then
    python3 simulator.py $1 1048576 64 16 LRU
elif [ $1 = "32MB_4B" ]; then
    python3 simulator.py $1 1048576 64 16 LRU
elif [ $1 = "bw_mem.traces.txt" ]; then
    python3 simulator.py $1 1048576 64 16 LRU
elif [ $1 = "ls.trace.txt" ]; then 
    python3 simulator.py $1 1048576 64 16 LRU
elif [ $1 = "gcc.trace.txt" ]; then
    python3 simulator.py $1 1048576 64 16 LRU
elif [ $1 = "naive_dgemm.trace.txt" ]; then
    python3 simulator.py $1 1048576 64 16 LRU
elif [ $1 = "naive_dgemm_full.trace.txt" ]; then
    python3 simulator.py $1 1048576 64 16 LRU
elif [ $1 = "openblas_dgemm.trace.txt" ]; then
    python3 simulator.py $1 1048576 64 16 LRU
elif [ $1 = "openblas_dgemm_full.trace.txt" ]; then
    python3 simulator.py $1 1048576 64 16 LRU
else
    python3 simulator.py $1 1048576 64 16 LRU
fi
