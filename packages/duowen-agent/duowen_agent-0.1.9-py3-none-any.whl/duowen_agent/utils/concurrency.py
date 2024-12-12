import logging
from multiprocessing.pool import ThreadPool
from threading import Thread
from typing import Union, List


def concurrent_execute(fn, data: Union[List[dict], List[str], List[tuple], List[list]], work_num=4):
    def process_item(item):
        if isinstance(item, dict):
            return fn(**item)
        elif isinstance(item, tuple):
            return fn(*item)
        elif isinstance(item, list):
            return fn(*item)
        elif isinstance(item, (str,int,float,bool)):
            return fn(item)
        else:
            raise ValueError(f"Unsupported data type: {type(item)}")

    logging.debug(f"thread concurrent_execute,work_num:{work_num} fn:{fn.__name__} data: {repr(data)}")

    with ThreadPool(work_num) as pool:
        results = pool.map(process_item, data)

    return results


def run_in_thread(fn):
    '''
    @run_in_thread
    def test(abc):
        return abc

    test(123)
    '''

    def wrapper(*k, **kw):
        t = Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t

    return wrapper
