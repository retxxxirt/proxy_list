import random
import requests
from threading import Thread, Timer

from .parser import Parser

class ProxyList:

    def __init__(self):

        self.__proxies = []
        self.parser = Parser()

        self.__update_timer = None

    @staticmethod
    def __check_selector(proxy, selector):

        for key in selector:

            if type(selector[key]) is not list:

                selector[key] = [selector[key]]

        for key in selector:

            is_appropriate = False

            for value in selector[key]:

                if proxy[key] == value:

                    is_appropriate = True

                    break

            if not is_appropriate:

                return False

        return True

    @staticmethod
    def __check_proxies(proxies, timeout = 10, chunk_size = 100):

        def check_proxy(proxy, thread):

            protocol = 'http' if proxy['type'] == 'http' else 'https'

            url = '%s://example.org/' % protocol

            try:

                response = requests.get(url, timeout = timeout, proxies = {protocol: proxy['address']})

                if response.status_code == 200 and response.url == url:

                    proxies_checked.append(proxy)

            except:

                pass

            if thread:

                thread.start()

                thread.join()

        proxies_checked, threads = [], []

        for index, proxy in enumerate(proxies):

            next_thread = None

            if index >= chunk_size:

                next_thread = threads[index - chunk_size]

            threads.append(Thread(target = check_proxy, args = [proxy, next_thread]))

        for thread in threads[-chunk_size:]:

            thread.start()

        for thread in threads[-chunk_size:]:

            thread.join()

        return proxies_checked

    def __cancel_update_timer(self):

        if self.__update_timer:

            self.__update_timer.cancel()

    def __start_update_timer(self, interval, target, arguments):

        self.__cancel_update_timer()

        self.__update_timer = Timer(interval, target, arguments)

        self.__update_timer.start()

    def __update(self, parsers, safe_parse, interval, check):

        if interval:

            self.__start_update_timer(interval, self.__update, [parsers, safe_parse, interval, check])

        unique_proxies = {}

        for proxy in self.parser.parse(parsers, safe_parse):

            proxy['address'] = '%s://%s:%s' % (proxy['type'], proxy['ip'], proxy['port'])

            unique_proxies[proxy['address']] = proxy

        proxies = [unique_proxies[address] for address in unique_proxies]

        if check:

            if type(check) is dict:

                self.__proxies = self.__check_proxies(proxies, **check)

            else:

                self.__proxies = self.__check_proxies(proxies)

        else:

            self.__proxies = proxies

    def update(self, parsers = None, check = False, safe_parse = True):

        self.__update(parsers, safe_parse, 0, check)

    def start_update(self, parsers = None, interval = 300, check = False, safe_parse = True):

        self.__update(parsers, safe_parse, interval, check)

    def stop_update(self):

        self.__cancel_update_timer()

    def get(self, selector = None):

        if selector:

            proxies = self.__proxies

            random.shuffle(proxies)

            for proxy in proxies:

                if self.__check_selector(proxy, selector):

                    return proxy

            return None

        else:

            return random.choice(self.__proxies)

    def get_all(self, selector = None):

        if selector:

            proxies = []

            for proxy in self.__proxies:

                if self.__check_selector(proxy, selector):

                    proxies.append(proxy)

            return proxies

        else:

            return self.__proxies