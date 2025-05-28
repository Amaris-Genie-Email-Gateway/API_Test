import os
from ctypes import CDLL
import pynvml

# 初始化

# 获取驱动版本
nvml_path = "C:/Windows/System32/nvml.dll"
pynvml.nvmlLib = CDLL(nvml_path)
pynvml.nvmlInit()


driver_version = pynvml.nvmlSystemGetDriverVersion()
print("Driver Version:", driver_version)


# 获取 GPU 数量
device_count = pynvml.nvmlDeviceGetCount()
print("Number of GPUs:", device_count)

# 遍历每个 GPU
for i in range(device_count):
    handle = pynvml.nvmlDeviceGetHandleByIndex(i)

    name = pynvml.nvmlDeviceGetName(handle)
    mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

    print(f"GPU {i}: {name}")
    print(f"  Memory Total: {mem_info.total / 1024 ** 2:.1f} MB")
    print(f"  Memory Used : {mem_info.used / 1024 ** 2:.1f} MB")
    print(f"  Utilization : {util.gpu}%")
    print(f"  Temperature : {temp} C")

# 关闭 NVML
pynvml.nvmlShutdown()
