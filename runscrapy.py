#coding=utf-8

import os
import sys
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

def run(name):
    configure_logging(install_root_handler = False)
    logging.basicConfig(
        filename = 'log/%s.log' % name,
        format = '%(levelname)s %(asctime)s: %(message) s',
        level = logging.DEBUG
    )
    process = CrawlerProcess(get_project_settings())
    try:
        logging.info('run start spider: %s' % name)
        process.crawl(name)
        process.start()
    except Exception as e:
        logging.error('run spider: %s exception: %s' % (name, e))

def main():
    from scrapy import cmdline
    cmdline.execute("scrapy crawl douban_music".split())
    cmdline.execute("scrapy crawl douban_video".split())

if __name__ == '__main__':
    name = sys.argv[1] or 'demo'
    print('name: %s' % name)
    print('project dir: %s' % os.getcwd())
    run(name)
