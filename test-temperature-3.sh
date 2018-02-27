#!/bin/bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
./TFLOPS_temperature/TFLOPS_temperature -device 3 | tee gpu3_stress_test.txt
