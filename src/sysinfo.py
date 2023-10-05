import psutil
import os
import sys
from psutil._common import bytes2human

#
commands = {"CPU": dict(core=psutil.cpu_count(logical=False), log_core=psutil.cpu_count(logical=True),
                        load=psutil.cpu_percent(interval=1), freq=psutil.cpu_freq().current)
            "RAM": dict(ram=psutil.virtual_memory, swap=psutil.swap_memory)
            "DISK": dict(mount=psutil.disk_partitions(), usage_disk=psutil.disk_usage(), IO_disk=psutil.disk_io_counters())
            "NET": dict(stat=psutil.net_io_counters(), connect=psutil.net_connections(), address=psutil.net_if_addrs(), card=psutil.net_if_stats())
            "PID": dict(pids=psutil.pids(), proc=psutil.process_iter(), check=psutil.pid_exists(),)
            }
# class test():
#     def __init__(self, command):
#         self.command = command
#
#     def sort(nt):
#
#         for name in nt._fields:
#             value = getattr(nt, name)
#             if name != 'percent':
#                 value = bytes2human(value)
#             print('%-10s : %7s' % (name.capitalize(), value))


# if __name__ == '__main__':
mem = (psutil.virtual_memory())
mem = (str(mem).split())
print(mem)


class test:
    def __init__(self, total, free, used, percent):
        self.total = total
        self.free = free
        self.used = used
        self.percent = percent

    def sort(self):
        for name in nt._fields:
            value = getattr(nt, name)
            if name != 'percent':
                value = bytes2human(value)
            print('%-10s : %7s' % (name.capitalize(), value))

#
total = bytes2human(psutil.virtual_memory())
print(total)







# mems = convert_tuple(mem)
print(mem)
