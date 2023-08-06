from timeit import default_timer
from multiprocessing import cpu_count, Pool
import math
import logging
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')


def exute_time(func):
    def delta_time(*args, **kwargs):
        t1 = default_timer()
        data = func(*args, *kwargs)
        delta = default_timer() - t1
        logging.info(
            f'Returned data: {data}. Run asynchronous time: {delta}')
    return delta_time


@exute_time
def factorize(number):
    factors = []
    for num in number:
        num_factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                num_factors.append(i)
        factors.append(num_factors)
    return factors


test_numbers = [128, 255, 99999, 10651060]


def process(numbers):
    return factorize(numbers)


max_wokers = cpu_count() * 2 + 1


def main():
    pool = Pool(processes=max_wokers)
    result = pool.map(process, [test_numbers])
    return result


if __name__ == '__main__':
    main()
