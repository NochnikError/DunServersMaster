
import psutil
"""вот ту я подзавис, надо сделать функцию конверта секунд в dd:hh:mm:ss вывода (started),но пока снова столкнулся с тем,
  что не могу запихнуть вывод команды в класс. Конвертер описан в PID.py, но возможно, для него не подключена библеотека
  Смысл в том, что бы завести выходные данные с команды в функцию класса, разбив на части. Но класс не принимает список."""
print('\n------------\nИнформация по использованию сервера пользователями.\n------------\n')
print(psutil.users())
# class user():
#     def command(self, name, terminal, host, started, pid):
#         self.name = name
#         self.terminal = terminal
#         self.host = host
#         self.started = started
#         self.pid = pid
#
#     def sectotime(self, a):
#         self.a=int(self.started)
#         h = a // 3600
#         m = (a // 60) % 60
#         s = a % 60
#         if m < 10:
#             m = str('0' + m)
#         else:
#             m = str(m)
#         if s < 10:
#             s = str('0' + s)
#         else:
#             s = str(s)
#         self.started = (str(h) + ':' + str(m) + ':' + str(s))
#
#     def conclusion(self):
#         print("\nCPU\n" "\n Количество ядер: " + str(self.name) + "\n Количество потоков: " + str(
#             self.terminal) + " \n Нагрузка на ЦП: " + str(
#             self.host) + "%" + "\n Частота процессора: " + str(self.started) + "MHz" + str(self.pid))
#
# command_user = user()
# command_user.command(psutil.users()[0], psutil.users()[1], psutil.users()[2], psutil.users()[3], psutil.users()[4])
#
# print(command_user)
