import psutil


def cpu_percentage_used():
    return str(psutil.cpu_percent(interval=1))
