import psutil
"""Апофеоз моего кодинга. Единственное, что отлично завелось под классом и принтуется без единой ошибки. 
 Хотя синтаксис класса надо подправить.
 Вот тут я сделал класс с инфой по процу, своими руками нахуй блять. Сделать то сделал, а как использовать в
 в main`e, я хуй знает. Пробовал и через import и через open, но когда вызываешь бота, он выдает хуйню"""
class cpu():
    def __init__(self, core, load, freq, freq_max):
        self.core = core
        self.load = load
        self.freq = freq
        self.fraq_max = freq_max

    def conclusion(self):
        print("\nCPU\n" "\n Количество ядер: " + str(self.core) + "\nКоличество потоков: " + str(
            self.load) + " \n Нагрузка на ЦП: " + str(
            self.freq) + "%" + "\nТекущая частота процессора: " + str(self.fraq_max) + "MHz")

command_cpu = cpu((psutil.cpu_count(logical=False)), (psutil.cpu_count(logical=True)), (psutil.cpu_percent(interval=3)),
                  (psutil.cpu_freq().current))

command_cpu.conclusion()