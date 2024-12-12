"""Decorator to analyze method performance.
TODO:
    profiler = cProfile.Profile()
    profiler.enable()
    my_function()
    profiler.disable()

    # Log profiling data
    logging.info(profiler.print_stats())
"""

__version__ = '1.0'
__author__ = 'Elifarley'
__all__ = ['profiled', 'perf_counter_ns']

import gc
import logging
import time


def perf_counter_ns():
    return time.perf_counter_ns()


def profiled(func):
    def wrapper(*args, **kwargs):
        execution_ok = False
        start_time_ns = perf_counter_ns()
        try:
            result = func(*args, **kwargs)
            execution_ok = True
            return result
        finally:
            task_execution_ms = (time.perf_counter_ns() - start_time_ns) / 1e6
            logging_func = logging.info if execution_ok else logging.warning
            logging_func(f"[perfmon: {func.__name__}] {task_execution_ms * 1e-3: .6f}s (GC: {gc.get_count()})")

    return wrapper

