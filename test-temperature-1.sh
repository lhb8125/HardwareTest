#!/bin/bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
./TFLOPS_temperature/TFLOPS_temperature -device 1 | tee ./result/gpu1_stress_test.txt
