#!/usr/bin/env bash
#matmul.py 后面是设置计算几次矩阵乘法，数值越大CPU满负载的时间越长
pip install numpy
echo "tusimple2018" | sudo -S apt-get install lm-sensors
python matmul.py 10 & python cpu_frequency.py