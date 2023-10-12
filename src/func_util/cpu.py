import datetime
import re
from pprint import pprint as pp

import psutil
from psutil._common import bytes2human
from rich.console import Console
from rich.table import Table, Column


# saw=436563643
# delta = timedelta(seconds=saw)
# print(delta)
class CpuUsageInfo:
    def get_info_time(self):
        print('\n------------\nСтатистика времени использования CPU\n------------\n')
        cpu_time_work = psutil.cpu_times(percpu=False)
        users_time = datetime.timedelta(seconds=int(cpu_time_work.user))
        system_time = datetime.timedelta(seconds=int(cpu_time_work.system))
        idle_time = datetime.timedelta(seconds=int(cpu_time_work.idle))
        percent = psutil.cpu_percent(interval=1)
        load = psutil.cpu_freq().current
        phih_count_cpu = psutil.cpu_count(logical=False)
        count_cpu = psutil.cpu_count(logical=True)
        intterupts = psutil.cpu_stats().interrupts

        time_cpu = f'Время использования CPU пользователем:    {users_time}\n' \
                   f'Время использование CPU системой:      {system_time}\n' \
                   f'Время простоя CPU:     {idle_time}\n' \
                   f'Нагрузка CPU(%):     {percent}%\n' \
                   f'Тактовая частота:     {load}MHz\n' \
                   f'Количество физ. ядер:     {phih_count_cpu}\n' \
                   f'Количество потоков:     {count_cpu}\n' \
                   f'Системных прерывания:     {intterupts}\n'
        return time_cpu

    def print_info_time(self):
        print(self.get_info_time())


class RamUsageInfo:
    def print_info(self):
        print('\n------------\nCтатистикa использования памяти. (RAM, SWAP)\n------------\n')
        print('MEMORY\n------')
        self.print_virtual_memory_info()
        print('\nSWAP\n------')
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
     # _template = "Device: %-\nTotal: Used: %8s\nFree: %8s\nUse: %5s%%\nType: %3s\nMount: %s\n"
    _error_expression = re.compile(r'(.+)(\n+|\.+.+)')
    _console = Console(width=24)

    def print_stats(self):
        print('\n------------\nCтатистикa смонтированных разделов диска\n------------\n')
        print(self.get_stats_message())

    def get_stats_message(self):
        # header = self._template
        disks_stats = []

        for part in psutil.disk_partitions(all=True):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                # stats = (self._template % (
                #     part.device,
                #     bytes2human(usage.total),
                #     bytes2human(usage.used),
                #     bytes2human(usage.free),
                #     int(usage.percent),
                #     part.fstype,
                #     part.mountpoint))
                stats = {
                    'device': part.device,
                    'total': bytes2human(usage.total),
                    'used': bytes2human(usage.used),
                    'free': bytes2human(usage.free),
                    'use': int(usage.percent),
                    'type': part.fstype,
                    'mount': part.mountpoint
                }

                grid = Table(show_header=False, expand=True, width=26, min_width=26)
                # grid.add_column() # max_width=10, min_width=10,
                # grid.add_column(Column(justify='right')) #width=10, max_width=10, min_width=10,

                # grid.add_column(max_width=14, min_width=14, overflow='fold', no_wrap=True)
                # grid.add_column(width=10, max_width=10, min_width=10, justify='right', overflow='fold', no_wrap=True)

                grid.add_row('Device: ', stats['device'])
                grid.add_row('Total: ', stats['total'])
                grid.add_row('Used: ', stats['used'])
                grid.add_row('Free: ', stats['free'])
                grid.add_row('Use: ', f'{stats["use"]}%')
                grid.add_row('Type: ', stats['type'])
                grid.add_row('Mount: ', stats['mount'])

                with self._console.capture() as capture:
                    self._console.print(grid)

                disks_stats.append(capture.get())
            except OSError as err:
                message = self._error_expression.match(str(err)).group().strip()
                failed_disk_stats = f'{part.device} ERROR: {message}'

                disks_stats.append(failed_disk_stats)

        # return '---------\n'.join(disks_stats)
        text = '---------\n'.join(disks_stats)

        # columns = Columns(text, expand=True)
        # columns = Columns(disks_stats, expand=True)
        return '`' + '\n' + text + '\n' + '`'


# def iotop(self):
#     try:
#         import curses
#     except ImportError:
#         sys.exit("Статистика дискового ввода-вывода доступна толькo под Unix")

class NetUsageInfo:

    def net_get_info_all_io(self):
        print('\n------------\nСтатистика сетевого ввода-вывода\n------------\n')
        connection = psutil.net_io_counters(pernic=False, nowrap=True)
        bytes_sent = bytes2human(connection.bytes_sent)
        bytes_recv = bytes2human(connection.bytes_recv)
        packets_sent = bytes2human(connection.packets_sent)
        packets_recv = bytes2human(connection.packets_recv)
        errin = bytes2human(connection.errin)
        errout = bytes2human(connection.errout)
        dropin = bytes2human(connection.dropin)
        dropout = bytes2human(connection.dropout)

        net_info_text = f'Получено:       {bytes_recv}\n' \
                        f'Отправлено:         {bytes_sent}\n' \
                        f'Пакетов получено:         {packets_recv}\n' \
                        f'Пакетов отправлено:       {packets_sent}\n' \
                        f'Ошибок при получение:         {errin}\n' \
                        f'Ошибок при отправке:          {errout}\n' \
                        f'Вход. отброшенные пакеты:       {dropin}\n' \
                        f'Выход. отброшенные пакеты:         {dropout}\n'
        return net_info_text

    def print_net_info(self):
        print(self.net_get_info_all_io())


class PIDUsageInfo:
    def get_info_top_pid(self):
        print('Введите кол-во выводих процессов:')
        q = 1
        pp([
               (p.pid, p.info['name'], sum(p.info['cpu_times']))
               for p in sorted(psutil.process_iter(['name', 'cpu_times']),
                               key=lambda p: sum(p.info['cpu_times'][:0]))
           ][-q:])

    def print_top_pid(self):
        print('\n------------\nПолучение топа процессов по потреблению ресурса процессора\n------------\n')
        print(self.get_info_top_pid())


class UsersUsageInfo:
    pass
    # def users_get_info


if __name__ == '__main__':
    time = CpuUsageInfo()
    time.print_info_time()
    info = RamUsageInfo()
    info.print_info()
    mount = DiskUsageInfo()
    mount.print_stats()
    net = NetUsageInfo()
    net.print_net_info()
    pid = PIDUsageInfo()
    pid.print_top_pid()
