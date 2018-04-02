import random
import requests
from threading import Timer, Thread

from .sources import BUILT_IN_SOURCES, DEFAULT_SOURCES

class ProxyList:

    def __init__(self):

        self.__proxies = []

        self.__stop_update = False

    @staticmethod
    def __check_selector(proxy, selector):

        for key in selector:

            if type(selector[key]) != list:

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

    def __update(self, sources, interval, check):

        if interval and not self.__stop_update:

            Timer(interval, self.__update, [sources, interval, check]).start()

        unique_proxies = {}

        for source in sources:

            if type(source) == str:

                proxies = BUILT_IN_SOURCES[source]()

            else:

                proxies = source()

            for proxy in proxies:

                proxy['address'] = '%s://%s:%s' % (proxy['type'], proxy['ip'], proxy['port'])

                unique_proxies[proxy['address']] = proxy

        proxies = [unique_proxies[key] for key in unique_proxies]

        if check:

            if type(check) == dict:

                self.__proxies = self.__check_proxies(proxies, **check)

            else:

                self.__proxies = self.__check_proxies(proxies)

        else:

            self.__proxies = proxies

    def update(self, sources = DEFAULT_SOURCES, check = False):

        self.__update(sources, 0, check)

    def start_update(self, interval = 300, sources = DEFAULT_SOURCES, check = False):

        self.__stop_update = False

        self.__update(sources, interval, check)

    def stop_update(self):

        self.__stop_update = True

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