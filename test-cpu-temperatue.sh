#!/usr/bin/env bash
#matmul.py 后面是设置计算几次矩阵乘法，数值越大CPU满负载的时间越长
# control + z 可提前结本脚本
pip install --upgrade pip
pip install numpy > /dev/null
sudo -S apt-get install -y lm-sensors > /dev/null & /
python matmul.py 2000 & python cpu_frequency.py