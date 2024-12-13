# -*- coding: latin -*-

import threading
from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from threading import Event
from queue import Queue
import asyncio, inspect
from functools import partial

class Thread(object):

    def is_thread_alive():
        """
        Verifica se existe alguma thread secund�ria ativa.
        Retorna True se pelo menos uma thread secund�ria estiver ativa, False caso contr�rio.
        """
        for thread in threading.enumerate():
            if thread.is_alive() and thread != threading.current_thread():

                if not thread.isDaemon() and thread.name != ['ThreadPoolExecutor-0_0']:
                    if 'asyncio_' not in thread.name and 'ThreadPoolExecutor-' not in thread.name:
                        print(thread.name)
                        return True

        return False


    class Processing(QObject):
        signal_function_executed = pyqtSignal()

        def __init__(self, target_function : object, update_function : object = None, callback_function : object = None, daemon = True, interval=1000, result_to_callback = False, initialize=True):
            super().__init__()

            self.signal_function_executed.connect(lambda : self.thread_finished())
            self.target_function = target_function
            self.result_target = None
            self.update_function = update_function
            self.callback_function = callback_function
            self.interval = interval
            self.result_to_callback = result_to_callback
            if isinstance(target_function, partial):
                self.is_async = inspect.iscoroutinefunction(target_function.func)
            else:
                self.is_async = inspect.iscoroutinefunction(target_function)
         
            if self.update_function:
                self.timer = QTimer()
                self.timer.timeout.connect(self.execute_update_function)

            self.thread : threading.Thread = None
            self.daemon = daemon

            if initialize:
                self.start()

        def execute_update_function(self):
            self.update_function()

        def start(self):
            if self.is_async:
                self.thread = threading.Thread(target=asyncio.run, args=(self.async_execute_target_function(),))
            else:
                self.thread = threading.Thread(target=self.execute_target_function)
            self.thread.daemon = self.daemon
            self.thread.start()
            
            if self.update_function:
                self.timer.start(self.interval)

        def execute_target_function(self):
            self.result_target = self.target_function()

            try:
                self.signal_function_executed.emit()
            except: 
                ...

        async def async_execute_target_function(self):
            self.result_target = await self.target_function()

            try:
                self.signal_function_executed.emit()
            except: 
                ...

        def thread_finished(self):
            if self.update_function:
                self.timer.disconnect()
                self.timer.stop()  # Para o timer quando a thread terminar
            if self.callback_function:
                if self.result_to_callback:
                    self.callback_function(self.result_target)
                else:
                    self.callback_function()

            self.thread : threading.Thread = None

        def is_alive(self):
            if self.thread:
                return self.thread.is_alive()
            return False

        def join(self):
            if self.thread:
                self.thread.join()


    class Multiprocessing(object):

        def __init__(self, lista_args : list , target_function : object, update_function : object = None, callback_function : object = None, callback_task : object = None, daemon = True, interval=1000, n_threads=5, wait=False, initialize=True):
            self.type_args = str
            if lista_args:
               self.type_args = type(lista_args[0])

            self.event = Event()
            self.target_function = target_function
            self.update_function = update_function
            self.callback_function = callback_function
            self.callback_task = callback_task
            self._already_call_callback_task = False
            self.interval = interval
            self.daemon = daemon
            if isinstance(target_function, partial):
                self.is_async = inspect.iscoroutinefunction(target_function.func)
            else:
                self.is_async = inspect.iscoroutinefunction(target_function)
         
            self.__fila = Queue(maxsize=len(lista_args) + 1)
            for args in lista_args:
                self.__fila.put(args)

            self.event.set()
            self.__fila.put('Kill')

            if len(lista_args) < n_threads:
                n_threads = len(lista_args)

            self.thrs = self.get_pool(n_threads)
            if initialize:
                self.start()

            if wait:
                self.join()

        def start(self):
            [th.start() for th in self.thrs]

        def join(self):
            [th.join() for th in self.thrs]

        def run_callback_task(self):
            for th in self.thrs:
                if th.is_alive():
                    return

            if self.callback_task and not self._already_call_callback_task:
                self.callback_task()
                self._already_call_callback_task = True

        def get_pool(self, n_th: int):
            """Retorna um n�mero n de Threads."""
            return [self.ThreadedFunctionRunner(event=self.event,
                                                queue=self.__fila,
                                                target_function=self.target_function,
                                                update_function = self.update_function,
                                                callback_function = self.callback_function,
                                                daemon = self.daemon,
                                                interval = self.interval,
                                                is_async=self.is_async,
                                                callback_task=self.run_callback_task)
                                    for n in range(n_th)]


        class ThreadedFunctionRunner(QObject):
            signal_function_executed = pyqtSignal(object)

            def __init__(self, event : Event, queue : Queue, target_function : object,  update_function : object | None, callback_function : object | None , daemon : bool , interval : int, is_async : bool, callback_task : object):
                super().__init__()
                
                self.signal_function_executed.connect(self.thread_finished)
                self.event = event
                self.queue = queue
                self.target_function = target_function
                self.update_function = update_function
                self.callback_function = callback_function
                self.interval = interval
                self.stoped = False
                self.daemon = daemon
                self.is_async = is_async
                self.callback_task = callback_task

                if self.update_function:
                    self.timer = QTimer()
                    self.timer.timeout.connect(self.execute_update_function)

                self.runner_thread : threading.Thread = None
             
            def execute_update_function(self):
                self.update_function(*self.runner_thread.args)

            def start(self):
                if self.is_async:
                    self.runner_thread = self.AsyncWorker(self.async_execute_target_function, self.queue, self.event)
                else:
                    self.runner_thread = self.Worker(self.execute_target_function, self.queue, self.event)
                self.runner_thread.daemon = self.daemon
                self.runner_thread.start()
               
                if self.update_function:
                    self.timer.start(self.interval)

            def join(self):
                if self.runner_thread:
                    self.runner_thread.join()

            def is_alive(self):
                if self.runner_thread:
                    return self.runner_thread.is_alive()
                return False

            async def async_execute_target_function(self, *args):
                args_target_function = await self.target_function(*args)
                if args_target_function:
                    if type(args_target_function) != list or type(args_target_function) != tuple:
                        args_target_function = [args_target_function]
                    self.signal_function_executed.emit(*args_target_function)
                else:
                    if type(args) != list and type(args) != tuple:
                        args = [args]

                    self.signal_function_executed.emit(*args)

            def execute_target_function(self, *args):
                args_target_function = self.target_function(*args)
                if args_target_function:
                    if type(args_target_function) != list or type(args_target_function) != tuple:
                        args_target_function = [args_target_function]
                    self.signal_function_executed.emit(*args_target_function)
                else:
                    if type(args) != list and type(args) != tuple:
                        args = [args]

                    self.signal_function_executed.emit(*args)

            def thread_finished(self, *args):
                if self.update_function:
                    self.timer.disconnect()
                    self.timer.stop()  # Para o timer quando a thread terminar
                if self.callback_function:
                    self.callback_function(*args)
                self.runner_thread = None

                self.callback_task()

            class AsyncWorker(threading.Thread):
                def __init__(self, async_target_function: object, queue: Queue, event: Event):
                    super().__init__()
                    self.async_target_function = async_target_function
                    self.queue = queue
                    self.event = event
                    self._stopped = False
                    self.args = []

                async def async_run(self):
                    self.event.wait()
                    while not self.queue.empty():
                        trabalho = self.queue.get()

                        if trabalho == 'Kill':
                            self.queue.put(trabalho)
                            self._stopped = True
                            break

                        if isinstance(trabalho, (list, tuple)):
                            self.args = trabalho
                        else:
                            self.args = [trabalho]

                        await self.async_target_function(*self.args)

                def run(self):
                    asyncio.run(self.async_run())

            class Worker(threading.Thread):
            
                def __init__(self, target_function : object, queue : Queue, event : Event):
                    super().__init__()
                    self.target_function = target_function
                    self.queue = queue
                    self.event = event
                    self._stoped = False
                    self.args = []

                def run(self):
                    self.event.wait()
                    while not self.queue.empty():
                        trabalho = self.queue.get()

                        if trabalho == 'Kill':
                            self.queue.put(trabalho)
                            self._stoped = True
                            break
                   
                        if type(trabalho) == list or type(trabalho) == tuple:
                            self.args = trabalho
                        else:
                            self.args = [trabalho]


                        self.target_function(*self.args)

        




