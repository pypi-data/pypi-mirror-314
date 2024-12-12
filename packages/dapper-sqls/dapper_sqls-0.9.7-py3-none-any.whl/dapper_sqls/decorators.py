# -*- coding: latin -*-
from functools import wraps
import asyncio
from time import perf_counter
from typing import Callable

def func_validation(callable_msg_error: Callable = None, use_raise: bool = False, use_log: bool = True):
    """
    Synchronous function decorator for validation, error handling, and logging execution time.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if use_log:
                start = perf_counter()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = str(e)
                if error_message == "Database unavailable":
                    if callable_msg_error:
                        callable_msg_error("Service temporarily unavailable. Please try again later.")
                else:
                    if use_raise:
                        raise
                    else:
                        print(f"Unhandled exception in '{func.__name__}': {error_message}")
            finally:
                if use_log:
                    stop = perf_counter()
                    execution_time = round(stop - start, 3)
                    print(f"The function '{func.__name__}' executed in {execution_time} seconds.")
        return wrapper
    return decorator

def async_func_validation(callable_msg_error: Callable = None, use_raise: bool = False, use_log: bool = True):
    """
    Asynchronous function decorator for validation, error handling, and logging execution time.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if use_log:
                start = perf_counter()
            try:
                return await asyncio.create_task(func(*args, **kwargs))
            except Exception as e:
                error_message = str(e)
                if error_message == "Database unavailable":
                    if callable_msg_error:
                        callable_msg_error("Service temporarily unavailable. Please try again later.")
                else:
                    if use_raise:
                        raise
                    else:
                        print(f"Unhandled exception in async function '{func.__name__}': {error_message}")
            finally:
                if use_log:
                    stop = perf_counter()
                    execution_time = round(stop - start, 3)
                    print(f"The async function '{func.__name__}' executed in {execution_time} seconds.")
        return wrapper
    return decorator