import psutil


def initialize():
    psutil.cpu_percent(interval=1)


def cpu_percentage_used():
    return str(psutil.cpu_percent(interval=None))


def memory_used():
    return int(psutil.virtual_memory().used / (1024 ** 2))
