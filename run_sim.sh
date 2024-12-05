#!/bin/bash
sed -i 's/\r$//' run_sim.sh
if [ $1 = "1KB_64B" ]; then
    python3 simulator.py $1 1024 64 16
elif [ $1 = "4MB_4B" ]; then
    python3 simulator.py $1 4194304 64 16
elif [ $1 = "32MB_4B" ]; then
    python3 simulator.py $1 4194304 64 16
elif [ $1 = "bw_mem.traces.txt" ]; then
    python3 simulator.py $1 4194304 64 16
elif [ $1 = "ls.trace.txt" ]; then
    python3 simulator.py $1 32768 64 16
elif [ $1 = "gcc.trace.txt" ]; then
    python3 simulator.py $1 32768 64 16
elif [ $1 = "naive_dgemm.trace.txt" ]; then
    python3 simulator.py $1 262144 64 16
elif [ $1 = "naive_dgemm_full.trace.txt" ]; then
    python3 simulator.py $1 262144 64 16
elif [ $1 = "openblas_dgemm.trace.txt" ]; then
    python3 simulator.py $1 262144 64 16
elif [ $1 = "openblas_dgemm_full.trace.txt" ]; then
    python3 simulator.py $1 262144 64 16
else
    python3 simulator.py $1 1024 64 16
fi
