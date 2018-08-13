import psutil


# def initialize():
#    psutil.cpu_percent(interval=1)


def cpu_percentage_used():
    return {'type': 'cpu_percentage_used',
            'value': psutil.cpu_percent(interval=None),
            'unit': '%'}


def memory_used():
    return {'type': 'memory_used',
            'value': int(psutil.virtual_memory().used / (1024 ** 2)),
            'unit': 'MiB'
            }


def disk_used():
    return {'type': 'disk_used',
            'value': round(float(
                psutil.disk_usage('/').used) / (1024 ** 3), 1),
            'unit': 'GiB'
            }
