import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print('----------------------')
        print(f'程序执行时间: \n\t{total_time:.4f} 秒')
        print('----------------------')
        # print(f'程序 {func.__name__}{args} {kwargs} 执行时间: {total_time:.4f} seconds')
        return result

    return timeit_wrapper
