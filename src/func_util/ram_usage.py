import psutil
from psutil._common import bytes2human


class RamUsageInfo:
    def print_info(self):
        print('\n------------\nCтатистикa использования памяти. (RAM, SWAP)\n------------\n')
        print('MEMORY\n------')
        self.print_virtual_memory_info()
        print('\nSWAP\n----')
        # self.pprint_ntuple(psutil.swap_memory())

    def get_info(self):
        virtual_memory = psutil.virtual_memory()
        total = bytes2human(virtual_memory.total)
        available = bytes2human(virtual_memory.available)
        percent = virtual_memory.percent
        used = bytes2human(virtual_memory.used)
        info_text = f'Всего:             {total}\n' \
                    f'Доступно:          {available}\n' \
                    f'Использовано:      {used}\n' \
                    f'Использовано(%):   {percent}%'
        return info_text

    def print_virtual_memory_info(self):
        print(self.get_info())


if __name__ == '__main__':
    info = RamUsageInfo()
    info.print_info()
