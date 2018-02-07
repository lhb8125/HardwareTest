#coding=utf-8
import os,commands,time,threading,argparse




def get_cpu_frequency():
    command = 'cat /proc/cpuinfo | grep MHz'
    raw_frequency = commands.getoutput(command).split("\n")
    frequency = []
    for i in raw_frequency:
        f = i.split(":")[-1].strip()
        frequency.append(int(f.split(".")[0]))
    return frequency


def get_cpu_temperature():
    cammand = "sensors | grep Core"
standard = get_cpu_frequency()

for i in range(90):
    tmp = get_cpu_frequency()
    f = 0
    for j in tmp:
        f += j
    print("CPU average frequency(MHz) per core round {} : {}".format(i,f/len(tmp)))
    time.sleep(2)


