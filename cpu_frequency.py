#coding=utf-8
import os,commands,time,threading,argparse,re

def get_cpu_frequency():
    command = 'cat /proc/cpuinfo | grep MHz'
    raw_frequency = commands.getoutput(command).split("\n")
    frequency = []
    for i in raw_frequency:
        f = i.split(":")[-1].strip()
        frequency.append(int(f.split(".")[0]))
    t = 0
    for j in frequency:
        t += j
    return t/len(frequency)


def get_cpu_temperature():
    command = "sensors | grep Core"
    raw_temperature = commands.getoutput(command).split('\n')
    sum = 0
    count = 0
    for t in raw_temperature:
        sum += int(re.split(r"\+|\(",t)[1][:2])
        count += 1
    return sum/count

for i in range(90):
    frequency = get_cpu_frequency()
    temperature = get_cpu_temperature()
    print("CPU average frequency(MHz) round {} : {} , temperature(Celsius) : {}\n ".format(i,frequency,temperature))
    time.sleep(3)


