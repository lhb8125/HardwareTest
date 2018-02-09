#!/usr/bin/env bash
#本脚本用来测试硬盘顺序/随机读写
#root密码默认为tusimple2017
echo tusimple2017 | sudo -S apt-get update > /dev/null
echo tusimple2017 | sudo -S apt-get install -y fio > /dev/null
echo tusimple2017 | sudo -S dmidecode -t bios > log_bios
echo tusimple2017 | sudo -S fio fio.conf > fio.log