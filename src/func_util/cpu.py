import os
import sys
import psutil
from psutil._common import bytes2human
from datetime import timedelta


# saw=436563643
# delta = timedelta(seconds=saw)
# print(delta)
class CpuUsageInfo:
    def get_info_time(self):
        print('\n------------\nСтатистика времени использования CPU\n------------\n')
        cpu_time_work = psutil.cpu_times(percpu=False)
        users_time = timedelta(seconds=int(cpu_time_work.user))
        system_time = timedelta(seconds=int(cpu_time_work.system))
        idle_time = timedelta(seconds=int(cpu_time_work.idle))
        percent = psutil.cpu_percent(interval=3)
        load = psutil.cpu_freq().current
        quantity_cpu = len(psutil.Process().cpu_affinity())
        phih_count_cpu = psutil.cpu_count(logical=False)
        count_cpu = psutil.cpu_count(logical=True)
        intterupts = psutil.cpu_stats().interrupts

        time_cpu = f'Время использования CPU пользователем:    {users_time}\n' \
                   f'Время использование CPU системой:         {system_time}\n' \
                   f'Время простоя CPU:                        {idle_time}\n' \
                   f'Нагрузка CPU(%):                          {percent}%\n' \
                   f'Тактовая частота:                         {load}MHz\n'
        return time_cpu

    def print_info_time(self):
        print(self.get_info_time())


class RamUsageInfo:
    def print_info(self):
        print('\n------------\nCтатистикa использования памяти. (RAM, SWAP)\n------------\n')
        print('MEMORY\n------')
        self.print_virtual_memory_info()
        print('\nSWAP\n----')
        self.print_swap_memory_info()

    def ram_get_info(self):
        virtual_memory = psutil.virtual_memory()
        total = bytes2human(virtual_memory.total)
        available = bytes2human(virtual_memory.available)
        percent = virtual_memory.percent
        used = bytes2human(virtual_memory.used)
        ram_info_text = f'Всего:             {total}\n' \
                        f'Доступно:          {available}\n' \
                        f'Использовано:      {used}\n' \
                        f'Использовано(%):   {percent}%'
        return ram_info_text

    def swap_get_info(self):
        swap_memory = psutil.swap_memory()
        total_swap = bytes2human(swap_memory.total)
        free_swap = bytes2human(swap_memory.free)
        percenct_swap = swap_memory.percent
        used_swap = bytes2human(swap_memory.used)
        sin = bytes2human(swap_memory.sin)
        sout = bytes2human(swap_memory.sout)
        swap_info_text = f'Всего:             {total_swap}\n' \
                         f'Доступно:          {free_swap}\n' \
                         f'Использовано:      {used_swap}\n' \
                         f'Использовано(%):   {percenct_swap}%\n' \
                         f'Загружено из файла подкачки: {sin}\n' \
                         f'Выгружено из файла подкачки: {sout}'
        return swap_info_text

    def print_virtual_memory_info(self):
        print(self.ram_get_info())

    def print_swap_memory_info(self):
        print(self.swap_get_info())


class DiskUsageInfo:
    def mount_get_info(self):
        print('\n------------\nCтатистикa смонтированных разделов диска\n------------\n')
        templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
        print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type", "Mount"))
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
        usage = psutil.disk_usage(part.mountpoint)
        print(templ % (
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint))
    # def iotop(self):
    #     try:
    #         import curses
    #     except ImportError:
    #         sys.exit("Статистика дискового ввода-вывода доступна толькo под Unix")


if __name__ == '__main__':
    info = RamUsageInfo()
    info.print_info()
    time = CpuUsageInfo()
    time.print_info_time()
    mount = DiskUsageInfo()
    sys.exit(mount.mount_get_info())
