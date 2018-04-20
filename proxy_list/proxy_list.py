import os
import random
import requests
from importlib import import_module
from threading import Thread, Timer

from .utilities import selector_is_valid

default_url = 'https://example.org/'
default_timeout = 10
default_check_interval = 0.03

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

            pass

        return False

    @staticmethod
    def check_many(proxies, url = default_url, timeout = default_timeout, interval = default_check_interval):

        checked_proxies, timers = [], []

        def check_many():

            proxy = proxies.pop()

            if len(proxies):

                timer = Timer(interval, check_many)

                timer.start()

                timers.append(timer)

            if ProxyList.check(proxy, url, timeout):

                checked_proxies.append(proxy)

        check_many()

        for timer in timers:

            timer.join()

        return checked_proxies

    def update(self, interval = 0, parsers = default_parsers, disabled_parsers = None, selector = None, count = None,
               check = False, url = default_url, timeout = default_timeout, check_interval = default_check_interval):

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

        if check or url != default_url or timeout != default_timeout or check_interval != default_check_interval:

            self.__proxies = self.check_many(self.__proxies, url, timeout, check_interval)

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