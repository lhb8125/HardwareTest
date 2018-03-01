#!/usr/bin/env bash
#matmul.py 后面是设置计算几次矩阵乘法，数值越大CPU满负载的时间越长
# control + z 可提前结本脚本
#sudo apt-get update
#sudo -S apt-get install -y python-pip,cpufrequtils,stress,lm-sensors > /dev/null
stress -c 4 -t 60 & python cpu_frequency.py
sleep 3
stress -c 4 -t 60 & python cpu_frequency.py
sleep 3
stress -c 4 -t 60 & python cpu_frequency.py
sleep 3
stress -c 4 -t 60 & python cpu_frequency.py
sleep 3
stress -c 4 -t 60 & python cpu_frequency.py

