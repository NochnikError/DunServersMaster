import psutil
from psutil._common import bytes2human

# def pprint_ntuple(self, nt):
#     for name in nt._fields:
#         value = getattr(nt, name)
#         if name != 'percent':
#             value = bytes2human(value)
#         print('%-10s : %7s' % (name.capitalize(), value))
# def main(self):
#     print('MEMORY\n------')
#     pprint_ntuple(psutil.virtual_memory())
#     print('\nSWAP\n----')
#     pprint_ntuple(psutil.swap_memory())
# #
# if __name__ == '__main__':
#     main()



mem = str(psutil.virtual_memory())

mem1 = mem.replace('svmem', '')
mem11 = mem1.replace('(', '')
mem12 = mem11.replace(')', '')
mem13 = mem12.split(',')
total = mem13[0]
usage = mem13[3]
free = mem13[4]
percent = mem13[2]
testss = 'none'
print(testss.ram_print())
# mem14 = int(mem13)
# mem15 = mem14[0:1:4]
# mem16 = tuple(mem15)
# mem17 = RAM(mem16)
# print(mem15.ram_print())
# mem = mem.split(',')
print(mem13)
# print(mem17)
print(type(mem13))
# mem2 = mem1.remove(1)
# tram.ram_print()