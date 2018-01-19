#!/usr/bin/env python
# coding=utf-8

import os
import csv
import codecs
import os.path
import logging
import argparse
import multiprocessing
from myspider.lib.ip_validator import Validator
import myspider.lib.mongo_helper

root = os.path.dirname(os.path.abspath(__file__))

def main():
    args = parse_args()
    db = myspider.lib.mongo_helper.Mongo()
    set_loglevel(args.loglevel)
    validator = Validator(args.target, args.timeout, args.worker, args.thread)
    ip_all = [ip for ip in db.proxy.find()]
    logging.info('Load proxy ip, total: %s', len(ip_all))
    result = validator.run(ip_all)
    result = sorted(result, key=lambda x: x['speed'])

def parse_args():
    procs_num = multiprocessing.cpu_count()
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', default='https://httpbin.org', help='target uri to validate proxy ip, default: https://httpbin.org')
    parser.add_argument('--timeout', type=int, default=15, help='timeout of validating each ip, default: 15s')
    parser.add_argument('--worker', type=int, default=procs_num, help='run with multi workers, default: CPU cores')
    parser.add_argument('--thread', type=int, default=100, help='run with multi thread in each worker, default: 100')
    parser.add_argument('--loglevel', default='info', help='set log level, e.g. debug, info, warn, error; default: info')
    args = parser.parse_args()
    return args

def set_loglevel(loglvl):
    level = logging.INFO
    if loglvl == 'debug':
        level = logging.DEBUG
    elif loglvl == 'info':
        level = logging.INFO
    elif loglvl == 'warn':
        level = logging.WARN
    elif loglvl == 'error':
        level = logging.ERROR
    else:
        logging.error('Unknown logging level: %s', loglvl)
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=level)
    logging.info('Set log level: %s', loglvl)

if __name__ == '__main__':
    main()
