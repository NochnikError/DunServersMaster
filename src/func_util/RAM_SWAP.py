import psutil
from psutil._common import bytes2human
"""Опять же, есть чуйка, что это можно все завернуть в класс и гонять через класс, но функция bytes2human все ломает.
Я честно, заебался. Неделю голову ломаю и не могу это оптимизировать под класс. Все ломается на поллучение атрибутов."""
print('\n------------\nCтатистикa использования памяти. (RAM, SWAP)\n------------\n')

def pprint_ntuple(nt):
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value)
        print('%-10s : %7s' % (name.capitalize(), value))

def main():
    print('MEMORY\n------')
    pprint_ntuple(psutil.virtual_memory())
    print('\nSWAP\n----')
    pprint_ntuple(psutil.swap_memory())

if __name__ == '__main__':
    main()