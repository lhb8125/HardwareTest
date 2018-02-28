#!/usr/bin/env bash
#matmul.py 后面是设置计算几次矩阵乘法，数值越大CPU满负载的时间越长
# control + z 可提前结本脚本
sudo apt-get update & /
sudo apt-get install -y python-pip,cpufrequtils,stress > /dev/null & /
sudo -S apt-get install -y lm-sensors > /dev/null & /
stress -c 56 & python cpu_frequency.py