import os,commands,time,threading

def get_cpu_frequency():
    command = 'cat /proc/cpuinfo | grep MHz'
    raw_frequency = commands.getoutput(command).split("\n")
    frequency = []
    for i in raw_frequency:
        f = i.split(":")[-1].strip()
        frequency.append(int(f[:4]))
    return frequency

standard = get_cpu_frequency()

for i in range(90):
    tmp = get_cpu_frequency()
    for j in range(len(tmp)):
        if (tmp[j] != standard[j]):
            print("CPU frequency(MHz) round {}:{} ------- Failed".format(i,tmp))
    print("CPU frequency(MHz) round {}:{} ------- Still OK".format(i, tmp))
    time.sleep(5)

