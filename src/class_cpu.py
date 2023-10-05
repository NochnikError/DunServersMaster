import psutil
import os
import sys
from psutil._common import bytes2human


# Вот тут я сделал класс с инфой по процу, своими руками нахуй блять. Сделать то сделал, а как использовать в
# в main`e, я хуй знает. Пробовал и через import и через open, но когда вызываешь бота, он выдает хуйню


class cpu():
    def __init__(self, core, load, freq, freq_max):
        self.core = core
        self.load = load
        self.freq = freq
        self.fraq_max = freq_max

    def conclusion(self):
        print("\nCPU\n" "\n Количество ядер: " + str(self.core) + "\n Количество потоков: " + str(
            self.load) + " \n Нагрузка на ЦП: " + str(
            self.freq) + "%" + "\n Частота процессора: " + str(self.fraq_max) + "MHz")

command_cpu = cpu((psutil.cpu_count(logical=False)), (psutil.cpu_count(logical=True)), (psutil.cpu_percent(interval=2)),
                  (psutil.cpu_freq().current))

command_cpu.conclusion()

# class RAM:
#     def __init__(self, total, free, used, percent):
#         self.total = total
#         self.free = free
#         self.used = used
#         self.percent = 0
#
#     def ram(self):
#         ([total] + [free] + [used])
#     def ram_print(self):
#         print("\nRAM\n----------", + "\nTotal = ", + self.total, "\nUsed = ", + self.usage, + "\nFree = ", + self.free, + "\nPercent Usage: " + self.percent )
#
#     def disk_print(self):
#         print("\nSWAP\n----------", + "\nTotal = ", + self.total, "\nUsed = ", + self.usage, + "\nFree = ", + self.free, + "\nPercent Usage: " + self.percent )
#
# ram = psutil.virtual_memory()
# total_ = (ram[0])
# used_ = (ram[2])
# free_ = (ram[4])
#
# total = bytes2human(total_)
# used = bytes2human(used_)
# free = bytes2human(free_)
# percent = (ram[3])
# print(total)
# print(type(total))

