import os
import sys
import time
import psutil
from psutil._common import bytes2human
"""Здесь 2 функции, которые скорей всего конфликтуют из-за названия. 1 функция отрабатывает отлично, когда доходит до второй,
Должна вылезать системная ошибка "платформа не поддерживается", но ее нету. Хотя иногда выскакивает.  """
print('\n------------\nCтатистикa  использования смонтированных разделов диска.\n------------\n')

def main():
    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type",
                   "Mount"))
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                # пропускаем приводы cd-rom, в которых нет диска;
                # они могут вызвать ошибку графического интерфейса
                # Windows для неготового раздела или просто зависнуть
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

if __name__ == '__main__':
    sys.exit(main())

print('\n------------\nCтатистикa дискового ввода-вывода. (ONLY UNIX)\n------------\n')

try:
    import curses
except ImportError:
    sys.exit('Платформа не поддерживается')

import psutil
from psutil._common import bytes2human

win = curses.initscr()
lineno = 0

def printl(line, highlight=False):
    """Тонкая обертка вокруг `curses`."""
    global lineno
    try:
        if highlight:
            line += " " * (win.getmaxyx()[1] - len(line))
            win.addstr(lineno, 0, line, curses.A_REVERSE)
        else:
            win.addstr(lineno, 0, line, 0)
    except curses.error:
        lineno = 0
        win.refresh()
        raise
    else:
        lineno += 1

def poll(interval):
    """Расчет использования операций ввода-вывода, сравнив
    данные до и после интервала `interval` (аргумент функции).
    Возвращает кортеж, включающий все запущенные в данный
    момент процессы, отсортированные по активности ввода-вывода
    и общей активности дискового ввода-вывода.
    """
    # получаем список всех процессов и счетчиков ввода-вывода с диска
    procs = [p for p in psutil.process_iter()]
    for p in procs[:]:
        try:
            p._before = p.io_counters()
        except psutil.Error:
            procs.remove(p)
            continue
    disks_before = psutil.disk_io_counters()

    # немного спим
    time.sleep(interval)

    # затем снова вытаскиваем ту же информацию
    for p in procs[:]:
        with p.oneshot():
            try:
                p._after = p.io_counters()
                p._cmdline = ' '.join(p.cmdline())
                if not p._cmdline:
                    p._cmdline = p.name()
                p._username = p.username()
            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                procs.remove(p)
    disks_after = psutil.disk_io_counters()

    # рассчитываем результаты, сравнив данные до и после `interval`
    for p in procs:
        p._read_per_sec = p._after.read_bytes - p._before.read_bytes
        p._write_per_sec = p._after.write_bytes - p._before.write_bytes
        p._total = p._read_per_sec + p._write_per_sec

    disks_read_per_sec = disks_after.read_bytes - disks_before.read_bytes
    disks_write_per_sec = disks_after.write_bytes - disks_before.write_bytes
    # сортируем процессы по общему объему ввода-вывода с диска,
    # более интенсивные будут первыми
    processes = sorted(procs, key=lambda p: p._total, reverse=True)
    return (processes, disks_read_per_sec, disks_write_per_sec)

def refresh_window(procs, disks_read, disks_write):
    """Вывод результатов на экран с помощью curses."""
    curses.endwin()
    templ = "%-5s %-7s %11s %11s  %s"
    win.erase()

    disks_tot = "Total DISK READ: %s | Total DISK WRITE: %s" \
                % (bytes2human(disks_read), bytes2human(disks_write))
    printl(disks_tot)

    header = templ % ("PID", "USER", "DISK READ", "DISK WRITE", "COMMAND")
    printl(header, highlight=True)

    for p in procs:
        line = templ % (
            p.pid,
            p._username[:7],
            bytes2human(p._read_per_sec),
            bytes2human(p._write_per_sec),
            p._cmdline)
        try:
            printl(line)
        except curses.error:
            break
    win.refresh()

def setup():
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    curses.endwin()
    win.nodelay(1)

def tear_down():
    win.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    setup()
    try:
        interval = 0
        while True:
            if win.getch() == ord('q'):
                break
            args = poll(interval)
            refresh_window(*args)
            lineno = 0
            interval = 0.5
            time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        tear_down()


print('\n------------\nCтатистикa дискового ввода-вывода. (only unix)\n------------\n')

import sys
import time

try:
    import curses
except ImportError:
    sys.exit('Платформа не поддерживается')

win = curses.initscr()
lineno = 0

def printl(line, highlight=False):
    """Тонкая обертка вокруг `curses`."""
    global lineno
    try:
        if highlight:
            line += " " * (win.getmaxyx()[1] - len(line))
            win.addstr(lineno, 0, line, curses.A_REVERSE)
        else:
            win.addstr(lineno, 0, line, 0)
    except curses.error:
        lineno = 0
        win.refresh()
        raise
    else:
        lineno += 1

def poll(interval):
    """Расчет использования операций ввода-вывода, сравнив
    данные до и после интервала `interval` (аргумент функции).
    Возвращает кортеж, включающий все запущенные в данный
    момент процессы, отсортированные по активности ввода-вывода
    и общей активности дискового ввода-вывода.
    """
    # получаем список всех процессов и счетчиков ввода-вывода с диска
    procs = [p for p in psutil.process_iter()]
    for p in procs[:]:
        try:
            p._before = p.io_counters()
        except psutil.Error:
            procs.remove(p)
            continue
    disks_before = psutil.disk_io_counters()

    # немного спим
    time.sleep(interval)

    # затем снова вытаскиваем ту же информацию
    for p in procs[:]:
        with p.oneshot():
            try:
                p._after = p.io_counters()
                p._cmdline = ' '.join(p.cmdline())
                if not p._cmdline:
                    p._cmdline = p.name()
                p._username = p.username()
            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                procs.remove(p)
    disks_after = psutil.disk_io_counters()

    # рассчитываем результаты, сравнив данные до и после `interval`
    for p in procs:
        p._read_per_sec = p._after.read_bytes - p._before.read_bytes
        p._write_per_sec = p._after.write_bytes - p._before.write_bytes
        p._total = p._read_per_sec + p._write_per_sec

    disks_read_per_sec = disks_after.read_bytes - disks_before.read_bytes
    disks_write_per_sec = disks_after.write_bytes - disks_before.write_bytes
    # сортируем процессы по общему объему ввода-вывода с диска,
    # более интенсивные будут первыми
    processes = sorted(procs, key=lambda p: p._total, reverse=True)
    return (processes, disks_read_per_sec, disks_write_per_sec)

def refresh_window(procs, disks_read, disks_write):
    """Вывод результатов на экран с помощью curses."""
    curses.endwin()
    templ = "%-5s %-7s %11s %11s  %s"
    win.erase()

    disks_tot = "Total DISK READ: %s | Total DISK WRITE: %s" \
                % (bytes2human(disks_read), bytes2human(disks_write))
    printl(disks_tot)

    header = templ % ("PID", "USER", "DISK READ", "DISK WRITE", "COMMAND")
    printl(header, highlight=True)

    for p in procs:
        line = templ % (
            p.pid,
            p._username[:7],
            bytes2human(p._read_per_sec),
            bytes2human(p._write_per_sec),
            p._cmdline)
        try:
            printl(line)
        except curses.error:
            break
    win.refresh()

def setup():
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    curses.endwin()
    win.nodelay(1)

def tear_down():
    win.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    setup()
    try:
        interval = 0
        while True:
            if win.getch() == ord('q'):
                break
            args = poll(interval)
            refresh_window(*args)
            lineno = 0
            interval = 0.5
            time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        tear_down()


