import threading
import _thread


def quit_function():
    """
    Прерывание выполнения функции исключением KeyboardInterrupt.
    """

    _thread.interrupt_main()


def exit_after_timeout(timeout: float):
    """
    Декоратор функции для ограничения времени ее работы.
    """

    def outer(func):
        def inner(*args, **kwargs):
            timer = threading.Timer(interval=timeout, function=quit_function)
            try:
                timer.start()
                result = func(*args, **kwargs)
            except KeyboardInterrupt:
                raise TimeoutError("Выполнение функции длилось слишком долго.")
            finally:
                timer.cancel()
            return result

        return inner

    return outer
