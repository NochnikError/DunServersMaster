import psutil
from psutil._common import bytes2human
from pprint import pprint as pp
from rich.console import Console
from rich.table import Table, Column
import datetime

# pp([
#     (p.pid, p.info)
#     for p in psutil.process_iter(['name', 'status', 'cpu_times'])
#     if p.info['status'] == psutil.STATUS_RUNNING
#     and p.info(float['cpu_times']) >= 25.0
#    ])


class DiskUsageInfo:
    _console = Console(width=24)

    def print_stats(self):
        print('\n------------\nCтатистикa смонтированных разделов диска\n------------\n')
        print(self.get_stats_message())

    def display_time(self, seconds, granularity=2):
        result = []
        intervals = (
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),  # 60 * 60 * 24
            ('hours', 3600),  # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
        )
        for name, count in intervals:
            value = seconds // count
            if value:
                self.seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])

    def get_stats_message(self):
        disks_stats = []
        for part in psutil.users():
            stats = {
                'name': part.name,
                'terminal': part.terminal,
                'host': part.host,
                'started': self.display_time(int(part.started)),
                'pid': part.pid
            }
            grid = Table(show_header=False, expand=True, width=23, min_width=23)
            grid.add_row('Name: ', stats['name'])
            grid.add_row('Terminal: ', stats['terminal'])
            grid.add_row('Host: ', stats['host'])
            grid.add_row('Started: ', stats['started'])
            grid.add_row('Pid: ', stats["pid"])

            with self._console.capture() as capture:
                self._console.print(grid)

            disks_stats.append(capture.get())
        text = '---------\n'.join(disks_stats)
        return '```' + '\n' + text + '\n' + '```'
#
#
# if __name__ == '__main__':
#     mount = DiskUsageInfo()
#     mount.print_stats()
