import os
import random
import requests
from importlib import import_module
from threading import Thread, Timer

from .utilities import selector_is_valid

default_url = 'https://example.org/'
default_timeout = 10
default_chunk_size = 100

default_parsers = []

for file in os.listdir('%s/parsers/' % os.path.dirname(os.path.realpath(__file__))):

    if file[-3:] == '.py':

        default_parsers.append(getattr(import_module('proxy_list.parsers.%s' % file[:-3]), file[:-3]))

class ProxyList:

    def __init__(self):

        self.__proxies = []
        self.__update_timer = None

    @staticmethod
    def __parse(parsers):

        threads, proxies = [], []

        for parser in parsers:

            def parse(parser):

                for proxy in parser():

                    proxies.append(proxy)

            threads.append(Thread(target = parse, args = [parser], name = 'parse %s' % parser.__name__))

        for thread in threads:

            thread.start()

        for thread in threads:

            thread.join()

        return proxies

    def __cancel_update_timer(self):

        if self.__update_timer:

            self.__update_timer.cancel()

    def __start_update_timer(self, interval, target, kwargs):

        self.__cancel_update_timer()

        self.__update_timer = Timer(interval, target, [], kwargs)

        self.__update_timer.start()

    @staticmethod
    def check(proxy, url = default_url, timeout = default_timeout):

        if type(proxy) == str:

            proxy = {'url': proxy, 'type': proxy.split('//')[0]}

        try:

            response = requests.get(url, timeout = timeout, proxies = {'http': proxy['url'], 'https': proxy['url']})

            if response.status_code == 200:

                return True

        except:

            return False

    def check_many(self, proxies, url = default_url, timeout = default_timeout, chunk_size = default_chunk_size):

        def check(proxy_list, proxy, url, timeout, thread):

            if proxy_list.check(proxy, url, timeout):

                checked_proxies.append(proxy)

            if thread:

                thread.start()

                thread.join()

        checked_proxies, threads = [], []

        for index, proxy in enumerate(proxies):

            thread = None

            if index >= chunk_size:

                thread = threads[index - chunk_size]

            threads.append(Thread(

                target = check,
                args = [self, proxy, url, timeout, thread],
                name = 'check proxy %s' % proxy['url']
            ))

        for thread in threads[-chunk_size:]:

            thread.start()

        for thread in threads[-chunk_size:]:

            thread.join()

        return checked_proxies

    def update(self, interval = 0, parsers = default_parsers, disabled_parsers = None, selector = None, count = None,
               check = False, url = default_url, timeout = default_timeout, chunk_size = default_chunk_size):

        if interval:

            kwargs = locals()

            del kwargs['self']

            self.__start_update_timer(interval, self.update, kwargs)

        if disabled_parsers:

            for parser in disabled_parsers:

                if parser in parsers:

                    parsers.remove(parser)

        unique_proxies = {}

        for proxy in self.__parse(parsers):

            proxy['url'] = '%s://%s:%s' % (proxy['type'], proxy['ip'], proxy['port'])

            unique_proxies[proxy['url']] = proxy

        self.__proxies = [unique_proxies[url] for url in unique_proxies]

        if selector:

            self.__proxies = self.get(selector)

        if check or url != default_url or timeout != default_timeout or chunk_size != default_chunk_size:

            self.__proxies = self.check_many(self.__proxies, url, timeout, chunk_size)

        if not interval:

            return self.get(None, count)

    def stop_update(self):

        self.__cancel_update_timer()

    def get(self, selector = None, count = None):

        if count is None:

            count = len(self.__proxies)

        proxies = self.__proxies.copy()

        if selector:

            random.shuffle(proxies)

            counter = 0

            for proxy in proxies.copy():

                if selector_is_valid(proxy, selector):

                    counter += 1

                else:

                    proxies.remove(proxy)

                if counter >= count:

                    break

            count = counter

        return proxies[:count]