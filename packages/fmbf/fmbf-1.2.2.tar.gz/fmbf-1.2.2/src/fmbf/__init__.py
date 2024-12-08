### ВЕРСИЯ 1.2.2

'''
Fork's Minecraft Botting Framework
----
Харош, что импортировал! Теперь чекни пример использования:

.. code-block:: python
    from fmbf import AbsoluteSolver

    solver = AbsoluteSolver()
    
    def program():
        return 'walk_forward'
    
    solver.add('Test23', program)

Читай эти подсказки по мере изучения модуля!
'''

import threading
import socket
import json
import inspect
from time import time, sleep
from typing import Protocol
import signal
import sys

def _exit_handler(signum, frame):
    '''
    Эта функция останавливает потоки ввода-вывода и закрывает сокет.
    Она вызывается при попытке выключить программу.'''

    print('Выключение программы')
    sys.exit(0)

sigint_handler = signal.signal(signal.SIGINT, _exit_handler)

def _decode_data(request: str) -> dict:
    '''Эта функция преобразует входящее сообщение от бота в словарь данных об окружающем мире Майнкрафта и о состоянии самого бота.'''
    try:
        return json.loads(request)
    except json.decoder.JSONDecodeError:
        print('Ошибка в отправленном из мода сообщении. Сообщи его создателю!')

class _ProgramCallable(Protocol):
    '''Это класс, описывающий **тип** функции, отвечающей за программу, которая даётся боту. Суть в том, что эта функция может принимать неограниченное количество названных аргументов и обязана возвращать только строку, и этот класс и описывает функцию такого рода.'''
    def __call__(self, **kwargs: str) -> str: ...

# Шаблон класса, чтобы строка 39 не ругалась на несуществующий класс, который я потом всё равно создаю
class _MinecraftConnection(threading.Thread): ...

class AbsoluteSolver(threading.Thread):
    '''ЗАПУСТИ PYTHON ДО MINECRAFT'А!
    ----'''

    def __init__(self, ip='127.0.0.1', port=2323, debug=False, info=False):
        '''Перед тобой программа, бесконечно слушающая входящие соединения клиентов Майнкрафта, но разрешающая войти только тем, кто был передан ей командой **add()**. Она работает параллельно основному потоку Python.

        Этот объект запускается только один раз, сразу после его инициализации. Его можно в любой момент закрыть методом **close()**, после чего он больше не запустится.
        
        :param ip: IP-адрес (по умолчанию твой локальный)
        :param port: порт для входящих соединений (по умолчанию 2323, как и в моде Minecraft)
        :param debug: режим отладки - куча сообщений заполнят консоль мигом
        :param info: режим ослабленной отладки - только сообщения о трансфере данных'''
        super().__init__()
        self.ip = ip
        self.port = port
        self.debug = debug
        self.info = info
        self.bots: list[_MinecraftConnection] = []
        self.allowed_bots: dict[callable] = dict()
        self.socket = socket.socket()
        self.is_running = True
        self.daemon = True
        signal.signal(signal.SIGINT, sigint_handler)
        self.start()
        if self.info:
            print('[INFO] FMBF 1.2.2, (c) Fork Genesis. Нажмите Ctrl+C, чтобы остановить программу.')
    
    def run(self):
        # Объект класса MinecraftServer работает в отдельном потоке от остальной программы.
        # Он открывает TCP-сервер и постоянно слушает входящие соединения (как ожидается, от клиентов Minecraft с модом FMBF).
        self.socket.bind((self.ip, self.port))
        self.socket.settimeout(0.5)
        self.socket.listen()
        while self.is_running:
            if self.debug:
                print(f'[DEBUG] Работающие потоки программы: {list(map(lambda x: x.name, threading.enumerate()))}')
                print(f'[DEBUG] Разрешения Солвера: {self.allowed_bots}')
            try:
                bot, _ = self.socket.accept()
                response_length = int.from_bytes(bot.recv(2))
                response = bot.recv(response_length*2).decode('utf-16-be')
                print(response)
                name = _decode_data(response)['name']

                if name in self.allowed_bots.keys():
                    bot.sendall((chr(1)+'1').encode('utf-16-be'))
                    self.bots.append(_MinecraftConnection(self, name, bot, self.allowed_bots[name]))

                    if self.debug:
                        print(f'[DEBUG] К Python попытался подключиться {name}, я разрешил!')
                else:
                    bot.sendall((chr(1)+'0').encode('utf-16-be'))
                    bot.close()

                    if self.debug:
                        print(f'[DEBUG] К Python попытался подключиться какой-то {name}, я запретил.')
            
            except socket.timeout:
                if not self.is_running:
                    break
            except ConnectionResetError:
                pass
            except KeyboardInterrupt:
                print('key')
            #sleep(5)
        
        for bot in self.bots:
            bot.close()
        self.socket.close()
        if self.debug:
            print(f'[DEBUG] Закрыл сервер!')

    def add(self, program: _ProgramCallable, name: str|None=None):
        '''Эта функция соединяет Python с ботом Minecraft и даёт ему программу, по которой он будет работать.
        Эта программа запускается в ответ на каждый раз, когда бот присылает Python'у данные из Minecraft'а.

        :param program: Функция, которая определяет поведение бота.

        Аргумент **program** это функция следующего вида:

        .. code-block:: python
            def Test23() -> str:
                return 'move_forward'
        
        Она должна иметь **ровно** такое же имя, как и аккаунт Майнкрафта; может принимать какие угодно **названные** аргументы и должна обязательно возвращать строку. Подробное описание этой функции и её возможностей будет приведено где-то *не тут*.
        '''
        if name == None:
            name = program.__name__
        
        self.allowed_bots[name] = program
        if self.debug:
            print(f'[DEBUG] Разрешил подключаться боту {name}!')
    
    def close(self):
        '''Закрыть!'''
        self.is_running = False

class _MinecraftConnection(threading.Thread):
    '''Скрытый от общих глаз, этот поток занимается одним конкретным ботом Майнкрафта, чтобы не мешать серверу принимать новых.'''
    def __init__(self, solver: AbsoluteSolver, name: str, bot: socket.socket, program: _ProgramCallable):
        super().__init__()
        self.solver = solver
        self.name = name
        self.bot = bot
        self.is_running = True
        self.program = program
        self.daemon = True
        self.start()

    def actual_program(self, data):
        '''Бот Minecraft передаёт JSON-словарь с огромным количеством данных - о сущностях, блоках, инвентаре и т.п. Модуль построен так, что функции-программе для бота не обязательно обрабатывать весь словарь, она может посмотреть только в информацию об инвентаре, а на остальное забить. Эта меж-функция фильтрует подаваемый в self.program словарь с данным майнкрафта, оставляя только те ключи, которые заданы в self.program'''
        
        kwargs = set(inspect.getfullargspec(self.program)[0])
        new_data = dict()
        
        # Проходим по тем значениям, что получили из Майнкрафта
        for key in data.keys():

            # Если такие ключи есть и в функции Питона, то
            if key in kwargs:
                new_data[key] = data[key]  # добавляем
            # А иначе просто игнорируем.

        # Проходим по тем значениям, что запрашивает функция Питона
        for arg in kwargs:
            # Если такого значения не было отправлено, то
            if arg not in new_data.keys():
                new_data[arg] = None  # засовываем пустышку
            
        return str(self.program(**new_data))

    def run(self):
        try:
            
            while self.is_running:
                response_length = int.from_bytes(self.bot.recv(2))
                response = self.bot.recv(response_length*2).decode('utf-16-be')
                if self.solver.info:
                    print(f'[INFO] Бот {self.name} прислал ответ: {response}')

                data = _decode_data(response)
                request = self.actual_program(data)

                self.bot.sendall((chr(len(request))+request).encode('utf-16-be')) # отправляем в маин
                if self.solver.info:
                    print(f'[INFO] Отослал боту {self.name} команду: {request}')
                #sleep(5)
            self.bot.close()
        except OSError:
            pass
        self.solver.bots.remove(self)
        if self.solver.debug:
            print(f'[DEBUG] Бот {self.name} завершил работу')

    def close(self):
        self.is_running = False


if __name__=='__main__':
    print('Вы запустили файл модуля fmbf. Вы точно хотели это сделать? Да? Ну тогда вот вам пример работы программы с этим модулем.')
    name = input('Введите свой никнейм: ')
    solver = AbsoluteSolver(info=True)

    def program(ctx):
        return ctx

    # Замените Test23 на никнейм вашего игрока Майнкрафт
    solver.add(program, name)
    while True:
        pass