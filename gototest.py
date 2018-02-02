################################################################################
# This script is created by Guancheng Wang, HPC department of Tusimple.
# If any problem occurs, please be free to contact guancheng.wang@tusimple.com
################################################################################
import commands
import os
import sys,commands

password = 'tusimple2017'

def profile_gpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "CUDA Driver Version / Runtime Version" in lines[cnt]:
            driver_runtime_version.append(lines[cnt].split("Version")[-1].strip())
        if "CUDA Capability Major" in lines[cnt]:
            capability_M_version.append(lines[cnt].split(":")[-1].strip())
        if "Total amount of global memory" in lines[cnt]:
            memory_size.append(lines[cnt].split(":")[-1].strip()[0:4])
        if "Multiprocessors," in lines[cnt] and "CUDA Cores/MP" in lines[cnt]:
            cuda_cores.append(lines[cnt].split(":")[-1].strip()[0:4])
        if "GPU Max Clock rate" in lines[cnt]:
            gpu_mainclock.append(lines[cnt].split(":")[-1].strip()[0:4])
        if "Memory Bus Width" in lines[cnt]:
            memory_bus_w.append(lines[cnt].split(":")[-1].strip())

    fopen.close()

def check_gpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "CUDA Driver Version / Runtime Version" in lines[cnt]:
            check_driver_runtime_version.append(lines[cnt].split("Version")[-1].strip()[6:])
        if "CUDA Capability Major" in lines[cnt]:
            check_capability_M_version.append(lines[cnt].split(":")[-1].strip())
        if "Total amount of global memory" in lines[cnt]:
            check_memory_size.append(lines[cnt].split(":")[-1].strip()[0:4])
        if "Multiprocessors," in lines[cnt] and "CUDA Cores/MP" in lines[cnt]:
            check_cuda_cores.append(lines[cnt].split(":")[-1].strip()[0:4])
        if "GPU Max Clock rate" in lines[cnt]:
            check_gpu_mainclock.append(lines[cnt].split(":")[-1].strip()[0:4])
        if "GeForce" in lines[cnt] and "Device" in lines[cnt] and len(lines[cnt]) < 35:
            gpu_name.append(lines[cnt].split("Version")[-1].strip())
        # if "Memory Bus Width" in lines[cnt]:
        #     check_memory_bus_w.append(lines[cnt].split(":")[-1].strip())
    fopen.close()


def profile_bandwidthlog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Host to Device" in lines[cnt]:
            h2d.append(lines[cnt+3].split()[-1].strip())
        if "Device to Host" in lines[cnt]:
            d2h.append(lines[cnt+3].split()[-1].strip())
        if "Device to Device" in lines[cnt]:
            d2d.append(lines[cnt+3].split()[-1].strip())
    fopen.close()

def check_bandwidthlog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Host to Device" in lines[cnt]:
            check_h2d.append(lines[cnt+3].split()[-1].strip())
        if "Device to Host" in lines[cnt]:
            check_d2h.append(lines[cnt+3].split()[-1].strip())
        if "Device to Device" in lines[cnt]:
            check_d2d.append(lines[cnt+3].split()[-1].strip())
    fopen.close()

def profile_flopslog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Running N=10 batched" in lines[cnt]:
            single_f.append(lines[cnt+1].split("=")[-1].strip())
            double_f.append(lines[cnt+2].split("=")[-1].strip())
    fopen.close()

def check_flopslog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Running N=10 batched" in lines[cnt]:
            check_single_f.append(lines[cnt+5].split("=")[-1].strip())
            check_double_f.append(lines[cnt+10].split("=")[-1].strip())
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
    fopen.close()

def check_cpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Model name" in lines[cnt]:
            check_cpuinfo_list.append(lines[cnt].split(":")[-1].strip())
        if "CPU(s):" in lines[cnt]:
            check_cpuinfo_list.append(lines[cnt].split(":")[-1].strip())
        if "Thread(s) per core" in lines[cnt]:
            check_cpuinfo_list.append(lines[cnt].split(":")[-1].strip())
    fopen.close()


def concatelist(sample):
    res = ""
    for cnt in range(len(sample)-1):
        res = res + sample[cnt] + ","
    res = res + sample[-1] + "\n"
    return res
# def check(sample,standard):
#     res = ""
#     flag = True
#     for cnt in range(len(sample)):
#         if(sample[cnt] == standard[0]):
#             res = res + sample[cnt]+" , Pass"+","
#         else:
#             res = res + sample[cnt]+" , Failed "+standard[0]+""+","
#             flag = False
#     res = res + "\n"
#     return res
def check(sample,standard):
    res = ""
    flag = True
    if(len(sample) > 0):
        if(sample[0] == standard[0]):
            res = res + sample[0]+" , Pass,"+standard[0]+""+","
        else:
            res = res + sample[0]+" , Failed,"+standard[0]+""+","
            flag = False

        del sample[0]
    res = res + "\n"
    return res

def check_bw_flops(sample,standard):
    res = ""
    if(len(sample) > 0 ):
        if((float(standard[0]) - float(sample[0]))/float(standard[0]) < 0.1):
            res = res + sample[0]+"  ,Pass,"+standard[0]+""+","
        else:
            res = res + sample[0]+"  ,Failed, "+standard[0]+""+","

        del sample[0]
    res = res + "\n"
    return res



def base_info_print():
    fout = open("out.csv", 'w')
    fout.write("Class,Value,Pass/Fail,Standard\n")
#-------------------------------OUTPUT BASIC-------------------------------#
    command = 'echo ' + password + ' | sudo -S dmidecode -s baseboard-serial-number'
    serial_number = commands.getoutput(command)[-15:]
    fout.write("machine serial number,"+serial_number+"\n")
    fout.write("OS version," + op_release_info + "\n")
    fout.write("cpu physical number," + str(cpu_number) + "\n")
    fout.write("gpu device number," + str(device_number) + "\n")
    fout.write("\n")
#-------------------------------OUTPUT BASIC END-------------------------------#
#-------------------------------OUTPUT CPU-------------------------------#
    fout.write("CPU\n")
    cpu_model = "CPU name,"+cpuinfo_list[2]+'\n'

    cpu_core = "CPU core(s),"+cpuinfo_list[0]

    if(cpuinfo_list[0] == check_cpuinfo_list[0]):
        cpu_core += ",Pass," + check_cpuinfo_list[0] + '\n'
    else:
        cpu_core += ",Failed," + check_cpuinfo_list[0] + '\n'
    cpu_threadpercore = "CPU thread per core,"+cpuinfo_list[1]

    if(cpuinfo_list[1] == check_cpuinfo_list[1]):
        cpu_threadpercore += ",Pass,"+check_cpuinfo_list[1] + '\n'
    else:
        cpu_threadpercore += ",Failed," + check_cpuinfo_list[1] + '\n'

    fout.write(cpu_model)
    fout.write(cpu_core)
    fout.write(cpu_threadpercore)
    fout.write("\n")
#-------------------------------OUTPUT CPU END-------------------------------#

def advanced_info_print(i):
    fout = open("out.csv", 'a')

#-------------------------------OUTPUT GPU-------------------------------#
    fout.write("gpu,")
    fout.write(gpu_name[i] + "\n")
    #gpu_bus_id = "bus_id," + concatelist(bus_id)
    #fout.write(gpu_bus_id)
#    gpu_version = "driver/runtime version," + concatelist(driver_runtime_version)
    gpu_version = "CUDA version," + \
                  check(driver_runtime_version, check_driver_runtime_version)
    fout.write(gpu_version)
    gpu_cap_version = "capability version," + \
                      check(capability_M_version, check_capability_M_version)
    fout.write(gpu_cap_version)
    gpu_memory = "memory size(MB)," + \
                 check_bw_flops(memory_size, check_memory_size)
    fout.write(gpu_memory)
    gpu_core = "cuda core(s)," + \
               check(cuda_cores, check_cuda_cores)
    fout.write(gpu_core)
    gpu_clock = "main clock(MHz)," + \
                check_bw_flops(gpu_mainclock, check_gpu_mainclock)
    fout.write(gpu_clock)
    # gpu_mem_bus = "Bus width," + \
    #     check(memory_bus_w,check_memory_bus_w)
    # fout.write(gpu_mem_bus)
    gpu_single_flops = "Single float(GFLOPS)," + \
        check_bw_flops(single_f,check_single_f)
    fout.write(gpu_single_flops)
    gpu_d2d = "Memory bandwidth(MB/s)," + \
        check_bw_flops(d2d,check_d2d)
    fout.write(gpu_d2d)
    gpu_h2d = "CPU to GPU(MB/s)," + \
        check_bw_flops(h2d,check_h2d)
    fout.write(gpu_h2d)
    gpu_d2h = "GPU to CPU(MB/s)," + \
        check_bw_flops(d2h,check_d2h)
    fout.write(gpu_d2h)
#-------------------------------OUTPUT GPU END-------------------------------#

    fout.close()


if __name__ == "__main__":
    CUDASAMPLES = "/home/tusimple/HardwareTest/cudaSamples"
    device_number = int(commands.getoutput('nvidia-smi -L | wc -l'))
    cpu_number = int(commands.getoutput("cat /proc/cpuinfo | grep \"physical id\" | sort | uniq | wc -l"))
    operation_info = commands.getoutput("lsb_release -a")
    op_release_info = operation_info.split("\n")[2].split(":")[-1].strip()
# cpu and mainboard
    cpuinfo_list = []
    check_cpuinfo_list = []
    os.system("lscpu > log_cpu")
    profile_cpulog("log_cpu")
    check_cpulog('./standard_info')
# gpu
#------------------GPU:BASIC INFORMATION------------------#
    bus_id_str = commands.getoutput("nvidia-smi --query-gpu=pci.bus_id --format=csv")
    bus_id =  bus_id_str.split()[1:]
    driver_runtime_version = []
    check_driver_runtime_version = []
    capability_M_version = []
    check_capability_M_version = []
    memory_size = []
    check_memory_size = []
    cuda_cores = []
    check_cuda_cores = []
    gpu_mainclock = []
    check_gpu_mainclock = []
    memory_bus_w = []
    check_memory_bus_w = []
    gpu_name = []
    os.system(CUDASAMPLES + "/1_Utilities/deviceQuery/deviceQuery > log_gpu")
    profile_gpulog("./log_gpu")
    check_gpulog("./standard_info")

    print driver_runtime_version
    print capability_M_version
    print memory_size
    print cuda_cores
    print gpu_mainclock
    print memory_bus_w
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
    print h2d
    print d2h
    print d2d
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
    print single_f
    print double_f
#-----------------------GFLOPS END------------------------#
    base_info_print()
    for i in range(device_number):
        advanced_info_print(i)
