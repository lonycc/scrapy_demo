# coding=utf-8

import time
import logging
import multiprocessing
import requests
import gevent
from gevent import monkey
monkey.patch_all()


class Validator:

    def __init__(self, target, timeout, procs_num, thread_num):
        self._target = target
        self._timeout = timeout
        self._procs_num = procs_num
        self._thread_num = thread_num
        logging.info('Init validator...\ntarget: %s\ntimeout: %s\nprocess num: %s\nthread num: %s',
                     target, timeout, procs_num, thread_num)

    def run(self, ip_all):
        result_queue = multiprocessing.Queue()
        process = []
        piece = len(ip_all) / self._procs_num + 1
        for i in range(0, self._procs_num):
            ip_list = ip_all[int(piece)*i:int(piece)*(i+1)]
            p = multiprocessing.Process(target=self.process_with_gevent, args=(ip_list, result_queue))
            p.start()
            process.append(p)
        for p in process:
            p.join()
        result = []
        for p in process:
            result.extend(result_queue.get())
        return result

    def process_with_gevent(self, ip_list, result_queue):
        jobs = [gevent.spawn(self.worker, ip_list) for _ in range(self._thread_num)]
        gevent.joinall(jobs)
        result = []
        for j in jobs:
            result.extend(j.value)
        result_queue.put(result)

    def worker(self, ip_list=[]):
        result = []
        while len(ip_list) > 0:
            ip = ip_list.pop()
            is_valid, speed = self.validate(ip['url'])
            print(ip['url'])
            if is_valid:
                ip['speed'] = speed
                result.append(ip)
                logging.info('Get valid ip %(ip)s in %(speed)ss' % ip )
        return result

    def validate(self, _url):
        proxies = {
            'http': 'http://%s' % _url
        }
        try:
            start = time.time()
            r = requests.get(self._target, proxies=proxies, timeout=self._timeout)
            if r.status_code == requests.codes.ok:
                speed = time.time() - start
                logging.debug('Validating %s, success in %ss', _url, speed)
                return True, speed
        except Exception as e:
            logging.debug('validating %s, err: %s', _url, e)
        return False, 0
