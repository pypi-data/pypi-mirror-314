from subprocess import Popen, PIPE
import os, platform, psutil, time

def gethwid() -> str:
    p = Popen('wmic csproduct get uuid', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split('\n')[1].strip()

def getuser() -> str:
    return os.getlogin()

def getcpuinfo() -> dict:
    cpu_info = {}
    try:
        cpu_info['cpu_model'] = platform.processor()
        cpu_info['cpu_cores'] = psutil.cpu_count(logical=False)
        cpu_info['cpu_threads'] = psutil.cpu_count(logical=True)
    except Exception as e:
        pass
    return cpu_info

def getgpuinfo() -> dict:
    gpu_info = {}
    try:
        if platform.system() == "Windows":
            p = Popen('wmic path win32_videocontroller get caption', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            gpu_info['gpu_model'] = p.stdout.read().decode().splitlines()[1].strip()
        elif platform.system() == "Linux":
            # For Linux, use lspci
            p = Popen(['lspci', '|', 'grep', 'VGA'], stdout=PIPE)
            gpu_info['gpu_model'] = p.stdout.read().decode().strip().split(":")[2]
        else:
            gpu_info['gpu_model'] = 'Unknown'
    except Exception as e:
        pass
    return gpu_info

def getraminfo() -> dict:
    ram_info = {}
    try:
        ram_info['total_ram'] = round(psutil.virtual_memory().total / 1024 / 1024)
        ram_info['available_ram'] = round(psutil.virtual_memory().available / 1024 / 1024)
        ram_info['used_ram'] = round(psutil.virtual_memory().used / 1024 / 1024)
    except:
        pass
    return ram_info

def getosinfo() -> dict:
    os_info = {}
    try:
        os_info['os_name'] = platform.system()
        os_info['os_version'] = platform.version()
        os_info['os_arch'] = platform.architecture()
    except:
        pass
    return os_info


def getdiskinfo() -> dict:
    disk_info = {}
    try:
        partitions = psutil.disk_partitions()
        disk_info['partitions'] = []
        for partition in partitions:
            partition_info = {}
            partition_info['device'] = partition.device
            partition_info['mountpoint'] = partition.mountpoint
            partition_info['fstype'] = partition.fstype
            partition_info['total'] = psutil.disk_usage(partition.mountpoint).total
            partition_info['used'] = psutil.disk_usage(partition.mountpoint).used
            partition_info['free'] = psutil.disk_usage(partition.mountpoint).free
            partition_info['percent'] = psutil.disk_usage(partition.mountpoint).percent
            disk_info['partitions'].append(partition_info)
    except Exception as e:
        disk_info['error'] = str(e)
    return disk_info

def getbatteryinfo() -> dict:
    battery_info = {}
    try:
        battery = psutil.sensors_battery()
        if battery:
            battery_info['percent'] = battery.percent
            battery_info['plugged'] = battery.power_plugged
            battery_info['secsleft'] = battery.secsleft
        else:
            battery_info['error'] = "No battery information available."
    except Exception as e:
        battery_info['error'] = str(e)
    return battery_info

def getmotherboardinfo() -> dict:
    motherboard_info = {}
    try:
        if platform.system() == "Windows":
            p = Popen('wmic baseboard get product,Manufacturer', shell=True, stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            output = out.decode().splitlines()
            if len(output) > 1:
                motherboard_info['manufacturer'] = output[1].split()[0]
                motherboard_info['product'] = ' '.join(output[1].split()[1:])
            else:
                motherboard_info['error'] = "No motherboard information found."
    except Exception as e:
        motherboard_info['error'] = str(e)
    return motherboard_info

def get_uptime() -> dict:
    uptime_info = {}
    try:
        # Get the boot time in seconds since the epoch
        boot_time = psutil.boot_time()
        # Calculate the uptime in seconds by subtracting the boot time from the current time
        uptime_seconds = int(time.time()) - int(boot_time)

        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60

        uptime_info['uptime'] = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    except Exception as e:
        uptime_info['error'] = str(e)
    

def getallinfo() -> dict[str, any]:
    system_info = {
        "HWID": gethwid(),
        "Username":getuser(),
        "CPU": getcpuinfo(),
        "GPU": getgpuinfo(),
        "RAM": getraminfo(),
        "OS": getosinfo(),
        "Disk": getdiskinfo(),
        "Battery": getbatteryinfo(),
        "Motherboard": getmotherboardinfo(),
        "Uptime": get_uptime()
    }


    return system_info
