import multiprocessing

bind = '0.0.0.0:9876'
workers = multiprocessing.cpu_count() * 2 + 1