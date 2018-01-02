################################################################################
# This script is created by Guancheng Wang, HPC department of Tusimple.
# If any problem occurs, please be free to contact guancheng.wang@tusimple.com
################################################################################
import commands
import os
import sys

def profile_gpulog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "CUDA Driver Version / Runtime Version" in lines[cnt]:
            driver_runtime_version.append(lines[cnt].split("Version")[-1].strip())
        if "CUDA Capability Major" in lines[cnt]:
            capability_M_version.append(lines[cnt].split(":")[-1].strip())
        if "Total amount of global memory" in lines[cnt]:
            memory_size.append(lines[cnt].split(":")[-1].strip())
        if "Multiprocessors," in lines[cnt] and "CUDA Cores/MP" in lines[cnt]:
            cuda_cores.append(lines[cnt].split(":")[-1].strip())
        if "GPU Max Clock rate" in lines[cnt]:
            gpu_mainclock.append(lines[cnt].split(":")[-1].strip())
        if "Memory Bus Width" in lines[cnt]:
            memory_bus_w.append(lines[cnt].split(":")[-1].strip())
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

def profile_flopslog(filename):
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    for cnt in range(len(lines)):
        if "Running N=10 batched" in lines[cnt]:
            single_f.append(lines[cnt+5].split("=")[-1].strip())
            double_f.append(lines[cnt+10].split("=")[-1].strip())
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

def concatelist(sample):
    res = ""
    for cnt in range(len(sample)-1):
        res = res + sample[cnt] + ","
    res = res + sample[-1] + "\n"
    return res

def prettyprint():
    fout = open("out.csv", 'w')

#-------------------------------OUTPUT BASIC-------------------------------#
    fout.write("operation release information," + op_release_info + "\n")
    fout.write("cpu physical number," + str(cpu_number) + "\n")
    fout.write("gpu device number," + str(device_number) + "\n")
    fout.write("\n")
#-------------------------------OUTPUT BASIC END-------------------------------#

#-------------------------------OUTPUT CPU-------------------------------#
    fout.write("CPU\n")
    cpu_model = "CPU name,"+cpuinfo_list[2]+'\n'
    cpu_core = "CPU core(s),"+cpuinfo_list[1]+'\n'
    cpu_threadpercore = "CPU thread per core,"+cpuinfo_list[0]+'\n'
    fout.write(cpu_model)
    fout.write(cpu_core)
    fout.write(cpu_threadpercore)
    fout.write("\n")
#-------------------------------OUTPUT CPU END-------------------------------#

#-------------------------------OUTPUT GPU-------------------------------#
    fout.write("GPU\n")
    fout.write("gpu,")
    for cnt in range(device_number-1):
        fout.write("device" + str(cnt) + ",")
    fout.write("device"+str(device_number-1)+"\n")
    gpu_bus_id = "bus_id," + concatelist(bus_id)
    fout.write(gpu_bus_id)
    gpu_version = "driver/runtime version," + concatelist(driver_runtime_version)
    fout.write(gpu_version)
    gpu_cap_version = "capability version," + concatelist(capability_M_version)
    fout.write(gpu_cap_version)
    gpu_memory = "memory size," + concatelist(memory_size)
    fout.write(gpu_memory)
    gpu_core = "cuda core(s)," + concatelist(cuda_cores)
    fout.write(gpu_core)
    gpu_clock = "main clock," + concatelist(gpu_mainclock)
    fout.write(gpu_clock)
    gpu_mem_bus = "显存总线宽度," + concatelist(memory_bus_w)
    fout.write(gpu_mem_bus)
    gpu_single_flops = "单精度浮点数(GFLOPS)," + concatelist(single_f)
    fout.write(gpu_single_flops)
    gpu_d2d = "显存带宽(MB/s)," + concatelist(d2d)
    fout.write(gpu_d2d)
    gpu_h2d = "CPU to GPU(MB/s)," + concatelist(h2d)
    fout.write(gpu_h2d)
    gpu_d2h = "GPU to CPU(MB/s)," + concatelist(d2h)
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
    os.system("lscpu > log_cpu")
    profile_cpulog("log_cpu")
# gpu
#------------------GPU:BASIC INFORMATION------------------#
    bus_id_str = commands.getoutput("nvidia-smi --query-gpu=pci.bus_id --format=csv")
    bus_id =  bus_id_str.split()[1:]
    driver_runtime_version = []
    capability_M_version = []
    memory_size = []
    cuda_cores = []
    gpu_mainclock = []
    memory_bus_w = []
    os.system(CUDASAMPLES + "/1_Utilities/deviceQuery/deviceQuery > log_gpu")
    profile_gpulog("./log_gpu")

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
    # for each device
    for n in range(device_number):
        os.system(CUDASAMPLES + "/1_Utilities/bandwidthTest/bandwidthTest -device=" + str(n) + " > log_bandwidth_"+str(n))
        profile_bandwidthlog("./log_bandwidth_"+str(n))
    # for all device 
    os.system(CUDASAMPLES + "/1_Utilities/bandwidthTest/bandwidthTest -device=all > log_bandwidth_all")
    profile_bandwidthlog("./log_bandwidth_all")
    print h2d
    print d2h
    print d2d
#-----------------------BANDWIDTH END-------------------------#

#-----------------------GPU:GFLOPS------------------------#
    single_f = []
    double_f = []
    # for each device
    for n2 in range(device_number):
        os.system(CUDASAMPLES + "/7_CUDALibraries/batchCUBLAS/batchCUBLAS -device=" + str(n) + " > log_flops_"+str(n2))
        profile_flopslog("./log_flops_"+str(n2))
    print single_f
    print double_f
#-----------------------GFLOPS END------------------------#
    prettyprint()
