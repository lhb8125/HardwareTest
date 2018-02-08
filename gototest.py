#coding=utf-8
################################################################################
# This script is created by Guancheng Wang, HPC department of Tusimple.
# If any problem occurs, please be free to contact guancheng.wang@tusimple.com
################################################################################
import commands
import os
from sets import Set
import sys,commands,decimal,time

password = 'tusimple2017'

def profile_gpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "CUDA Driver Version / Runtime Version" in lines[cnt]:
            driver_runtime_version.append(lines[cnt].split("Version")[-1].strip()[6:])
        # if "CUDA Capability Major" in lines[cnt]:
        #     capability_M_version.append(lines[cnt].split(":")[-1].strip())
        if "Total amount of global memory" in lines[cnt]:
            memory_size.append(str(round(float(lines[cnt].split(":")[-1].strip()[0:4]) / 1024.0,3)))
        if "Multiprocessors," in lines[cnt] and "CUDA Cores/MP" in lines[cnt]:
            cuda_cores.append(lines[cnt].split(":")[-1].strip()[0:4])
        if "GPU Max Clock rate" in lines[cnt]:
            gpu_mainclock.append(str(round(float(lines[cnt].split(":")[-1].strip()[0:4]) / 1024.0,3)))
        if "GeForce" in lines[cnt] and "Device" in lines[cnt] and len(lines[cnt]) < 35:
            gpu_name.append(lines[cnt].split("Version")[-1].strip())
        # if "Memory Bus Width" in lines[cnt]:
        #     memory_bus_w.append(lines[cnt].split(":")[-1].strip())

    fopen.close()

def check_gpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    global std_device_number
    for cnt in range(len(lines)):
        if "CUDA Driver Version / Runtime Version" in lines[cnt]:
            check_driver_runtime_version.append(lines[cnt].split("Version")[-1].strip()[6:])
        # if "CUDA Capability Major" in lines[cnt]:
        #     check_capability_M_version.append(lines[cnt].split(":")[-1].strip())
        if "Total amount of global memory" in lines[cnt]:
            check_memory_size.append(str(round(float(lines[cnt].split(":")[-1].strip()[0:4]) / 1024.0,3)))
        if "Multiprocessors," in lines[cnt] and "CUDA Cores/MP" in lines[cnt]:
            check_cuda_cores.append(lines[cnt].split(":")[-1].strip()[0:4])
        if "GPU Max Clock rate" in lines[cnt]:
            check_gpu_mainclock.append(str(round(float(lines[cnt].split(":")[-1].strip()[0:4]) / 1024.0,3)))
        if "GPU Device Number" in lines[cnt]:
            std_device_number = int(lines[cnt].split(":")[-1].strip())
        # if "Memory Bus Width" in lines[cnt]:
        #     check_memory_bus_w.append(lines[cnt].split(":")[-1].strip())
    fopen.close()


def profile_bandwidthlog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Host to Device" in lines[cnt]:
            h2d.append(str(round(float(lines[cnt + 3].split()[-1].strip()) / 1024.0, 3)))
        if "Device to Host" in lines[cnt]:
            d2h.append(str(round(float(lines[cnt + 3].split()[-1].strip()) / 1024.0, 3)))
        if "Device to Device" in lines[cnt]:
            d2d.append(str(round(float(lines[cnt+3].split()[-1].strip()) / 1024.0,3)))
    fopen.close()

def check_bandwidthlog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Host to Device" in lines[cnt]:
            check_h2d.append(str(round(float(lines[cnt + 3].split()[-1].strip()) / 1024.0, 3)))
        if "Device to Host" in lines[cnt]:
            check_d2h.append(str(round(float(lines[cnt + 3].split()[-1].strip()) / 1024.0, 3)))
        if "Device to Device" in lines[cnt]:
            check_d2d.append(str(round(float(lines[cnt + 3].split()[-1].strip()) / 1024.0, 3)))
    fopen.close()

def profile_flopslog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Running N=10 batched" in lines[cnt]:
            single_f.append(str(round(float(lines[cnt+5].split("=")[-1].strip()) / 1000.0,3)))
            double_f.append(str(round(float(lines[cnt+10].split("=")[-1].strip()) / 1000.0,3)))
    fopen.close()

def check_flopslog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Running N=10 batched" in lines[cnt]:
            check_single_f.append(str(round(float(lines[cnt+1].split("=")[-1].strip()) / 1000.0,3)))
            check_double_f.append(str(round(float(lines[cnt+2].split("=")[-1].strip()) / 1000.0,3)))
    fopen.close()


def profile_cpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Model name" in lines[cnt]:
            cpuinfo_list.append(lines[cnt].split(":")[-1].strip())
        if "CPU(s):" in lines[cnt]:
            cpuinfo_list.append(lines[cnt].split(":")[-1].strip())
        if "Thread(s) per core" in lines[cnt]:
            cpuinfo_list.append(lines[cnt].split(":")[-1].strip())
        if "L1d cache" in lines[cnt]:
            local_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])
        if "L2 cache" in lines[cnt]:
            local_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])
        if "L3 cache" in lines[cnt]:
            local_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])

    fopen.close()

def check_cpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    global cpu_model_name
    global std_os_version
    global std_cpu_number
    for cnt in range(len(lines)):
        if "Model name" in lines[cnt]:
            cpu_model_name.add(lines[cnt].split(":")[-1].strip())
        if "CPU(s):" in lines[cnt]:
            check_cpuinfo_list.append(lines[cnt].split(":")[-1].strip())
        if "Thread(s) per core" in lines[cnt]:
            check_cpuinfo_list.append(lines[cnt].split(":")[-1].strip())
        if "CPU physical number" in lines[cnt]:
            std_cpu_number = int(lines[cnt].split(":")[-1].strip())
        if "OS Version" in lines[cnt]:
            std_os_version = lines[cnt].split(":")[-1].strip().split(" ")[1]
        if "L1d cache" in lines[cnt]:
            std_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])
        if "L2 cache" in lines[cnt]:
            std_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])
        if "L3 cache" in lines[cnt]:
            std_cache_size.append(lines[cnt].split(":")[-1].strip()[:-1])
        if "error_range" in lines[cnt]:
            error_range = int(lines[cnt].split(":")[-1].strip())
    fopen.close()


def concatelist(sample):
    res = ""
    for cnt in range(len(sample)-1):
        res = res + sample[cnt] + ","
    res = res + sample[-1] + "\n"
    return res

def check(sample,standard):
    res = ""
    flag = True
    if(len(sample) > 0):
        if(sample[0] == standard[0]):
            res = res + sample[0]+","+standard[0]+",Pass,"
        else:
            res = res + sample[0]+","+standard[0]+",Failed,"
            flag = False

        del sample[0]
    res = res + "\n"
    return res


#仅用于check CPU cache size
def check_parallel(sample,standard):
    res = ""
    flag = True
    if(len(sample) > 0):
        if(sample[0] == standard[0]):
            res = res + sample[0]+","+standard[0]+",Pass,"
        else:
            res = res + sample[0]+","+standard[0]+",Failed,"
            flag = False

        del sample[0]
        del standard[0]
    res = res + "\n"
    return res

def check_bw_flops(sample,standard):
    res = ""
    if(len(sample) > 0 ):
        if((float(standard[0]) - float(sample[0]))/float(standard[0]) < error_range):
            res = res + sample[0] + "," + str(int(standard[0]) * (1 - error_range)) +"~"+str(int(standard[0]) * (1 + error_range)) + ",Pass,"
        else:
            res = res + sample[0] + "," + standard[0] + ",Failed,"

        del sample[0]
    res = res + "\n"
    return res



def base_info_print():
    fout = open("out.csv", 'w')
    fout.write("测试项目,测试值,标准值,通过/失败\n")
#-------------------------------OUTPUT BASIC-------------------------------#
    command = 'echo ' + password + ' | sudo -S dmidecode -s baseboard-serial-number'
    serial_number = commands.getoutput(command).split("\n")[0].strip()
    fout.write("Motherboard serial number,"+serial_number+"\n")
    fout.write("OS version," + op_release_info +","+std_os_version)
    if(op_release_info == std_os_version):
        fout.write(",Pass\n")
    else:
        fout.write(",Failed\n")
    fout.write("number of CPU," + str(cpu_number) + "," + str(std_cpu_number))
    if (cpu_number == std_cpu_number):
        fout.write(",Pass\n")
    else:
        fout.write(",Failed\n")
    fout.write("number of GPU," + str(device_number) +","+ str(std_device_number))
    if(device_number == std_device_number):
        fout.write(",Pass\n")
    else:
        fout.write(",Failed\n")
    fout.write("\n")
#-------------------------------OUTPUT BASIC END-------------------------------#
#-------------------------------OUTPUT CPU-------------------------------#
    fout.write("CPU\n")
    cpu_model = ""
    if(len(cpu_model_name) == 1):
        for i in cpu_model_name:
            for j in range(cpu_number):
                cpu_model += "CPU {} name,".format(j)
                cpu_tmp_info = i.split(" ")
                cpu_model += cpu_tmp_info[2]  +',\n'
    else:
        count = 0
        for i in cpu_model_name:
            cpu_model += "CPU {} name,".format(count)
            cpu_tmp_info = i.split(" ")
            cpu_model += cpu_tmp_info[2] + ',\n'
            count += 1

    cpu_core = "CPU core(s),"+cpuinfo_list[0]

    if(cpuinfo_list[0] == check_cpuinfo_list[0]):
        cpu_core += "," + check_cpuinfo_list[0] + ",Pass,"   + '\n'
    else:
        cpu_core += "," + check_cpuinfo_list[0] + ",Failed," + '\n'
    cpu_threadpercore = "CPU hyperthreading,"
    if(cpuinfo_list[1] > 1):
        cpu_threadpercore += "True," + "True" + ",Pass," + '\n'
    else:
        cpu_threadpercore += "False," + "True"+ ",Failed," + '\n'

    L1_cache = "L1 cache(K)," + check_parallel(local_cache_size,std_cache_size)
    L2_cache = "L2 cache(K)," + check_parallel(local_cache_size,std_cache_size)
    L3_cache = "L3 cache(K)," + check_parallel(local_cache_size,std_cache_size)

    fout.write(cpu_model)
    fout.write(cpu_core)
    fout.write(cpu_threadpercore)
    fout.write(L1_cache)
    fout.write(L2_cache)
    fout.write(L3_cache)
    fout.write("\n")
#-------------------------------OUTPUT CPU END-------------------------------#

def advanced_info_print(i):
    fout = open("out.csv", 'a')

#-------------------------------OUTPUT GPU-------------------------------#
    fout.write("gpu Device{},\n".format(str(i)))
    # fout.write(gpu_name[i].split(':')[-1] + "\n")
    #gpu_bus_id = "bus_id," + concatelist(bus_id)
    #fout.write(gpu_bus_id)
#    gpu_version = "driver/runtime version," + concatelist(driver_runtime_version)
    gpu_version = "CUDA version," + \
                  check(driver_runtime_version, check_driver_runtime_version)
    fout.write(gpu_version)
    # gpu_cap_version = "capability version," + \
    #                   check(capability_M_version, check_capability_M_version)
    # fout.write(gpu_cap_version)
    gpu_memory = "memory size(GB)," + \
                 check_bw_flops(memory_size, check_memory_size)
    fout.write(gpu_memory)
    gpu_core = "cuda core(s)," + \
               check(cuda_cores, check_cuda_cores)
    fout.write(gpu_core)
    gpu_clock = "main clock(GHz)," + \
                check_bw_flops(gpu_mainclock, check_gpu_mainclock)
    fout.write(gpu_clock)
    # gpu_mem_bus = "Bus width," + \
    #     check(memory_bus_w,check_memory_bus_w)
    # fout.write(gpu_mem_bus)
    gpu_single_flops = "Single float(TFLOPS)," + \
        check_bw_flops(single_f,check_single_f)
    fout.write(gpu_single_flops)
    gpu_d2d = "Memory bandwidth(GB/s)," + \
        check_bw_flops(d2d,check_d2d)
    fout.write(gpu_d2d)
    gpu_h2d = "CPU to GPU(GB/s)," + \
        check_bw_flops(h2d,check_h2d)
    fout.write(gpu_h2d)
    gpu_d2h = "GPU to CPU(GB/s)," + \
        check_bw_flops(d2h,check_d2h)
    fout.write(gpu_d2h)
    fout.write("\n")
#-------------------------------OUTPUT GPU END-------------------------------#

    fout.close()

def get_cpu_frequency():
    command = 'cat /proc/cpuinfo | grep MHz'
    raw_frequency = commands.getoutput(command).split("\n")
    frequency = []
    for i in raw_frequency:
        f = i.split(":")[-1].strip()
        frequency.append(int(f[:4]))
    return frequency

def stress_test():
    fout = open("out.csv", 'a')
    standard = get_cpu_frequency()
    fout.write("CPU stress test,Standard : {},".format(standard[0]))
    for i in range(10):
        tmp = get_cpu_frequency()
        for j in range(len(tmp)):
            if(tmp[j] != standard[j]):
                fout.write("Failed")
                return 0
        time.sleep(1)
    fout.write("Pass")
    return 1



if __name__ == "__main__":
    CUDASAMPLES = "/home/tusimple/HardwareTest/cudaSamples"
    device_number = int(commands.getoutput('nvidia-smi -L | wc -l'))
    cpu_number = int(commands.getoutput("cat /proc/cpuinfo | grep \"physical id\" | sort | uniq | wc -l"))
    operation_info = commands.getoutput("lsb_release -a")
    op_release_info = operation_info.split("\n")[2].split(":")[-1].split(" ")[1]
# cpu and mainboard
    error_range = 0 #误差范围
    cpuinfo_list = []
    check_cpuinfo_list = []
    std_cache_size = []
    local_cache_size = []
    cpu_model_name = Set()
    std_cpu_number = 0
    std_os_version = ""
    os.system("lscpu > log_cpu")
    profile_cpulog("log_cpu")
    check_cpulog('./standard_info')
# gpu
#------------------GPU:BASIC INFORMATION------------------#
    bus_id_str = commands.getoutput("nvidia-smi --query-gpu=pci.bus_id --format=csv")
    bus_id =  bus_id_str.split()[1:]
    driver_runtime_version = []
    check_driver_runtime_version = []
    # capability_M_version = []
    # check_capability_M_version = []
    memory_size = []
    check_memory_size = []
    cuda_cores = []
    check_cuda_cores = []
    gpu_mainclock = []
    check_gpu_mainclock = []
    memory_bus_w = []
    check_memory_bus_w = []
    gpu_name = []
    std_device_number = 0
    os.system(CUDASAMPLES + "/1_Utilities/deviceQuery/deviceQuery > log_gpu")
    profile_gpulog("./log_gpu")
    check_gpulog("./standard_info")


#------------------BASIC INFORMATION END------------------#

#-----------------------GPU:BANDWIDTH-------------------------#
    h2d = []
    d2h = []
    d2d = []
    check_h2d = []
    check_d2h = []
    check_d2d = []
    # for each device
    for n in range(device_number):
        os.system(CUDASAMPLES + "/1_Utilities/bandwidthTest/bandwidthTest -device=" + str(n) + " > log_bandwidth_"+str(n))
        profile_bandwidthlog("./log_bandwidth_"+str(n))
    # for all device
    os.system(CUDASAMPLES + "/1_Utilities/bandwidthTest/bandwidthTest -device=all > log_bandwidth_all")
    profile_bandwidthlog("./log_bandwidth_all")
    check_bandwidthlog("./standard_info")

#-----------------------BANDWIDTH END-------------------------#

#-----------------------GPU:GFLOPS------------------------#
    single_f = []
    double_f = []
    check_single_f = []
    check_double_f = []
    # for each device
    for n2 in range(device_number):
        os.system(CUDASAMPLES + "/7_CUDALibraries/batchCUBLAS/batchCUBLAS -device=" + str(n) + " > log_flops_"+str(n2))
        profile_flopslog("./log_flops_"+str(n2))
        check_flopslog("./standard_info")

#-----------------------GFLOPS END------------------------#
    base_info_print()
    for i in range(device_number):
        advanced_info_print(i)
