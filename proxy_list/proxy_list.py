import random
from threading import Timer

from .sources import BUILT_IN_SOURCES, DEFAULT_SOURCES

class ProxyList:

    def __init__(self):

        self.__list = []

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

    def update(self, interval = 60, sources = DEFAULT_SOURCES, single_executing = False):

        def update():

            if not single_executing and not self.__stop_update:

                Timer(interval, update).start()

            self.__list, unique_proxies = [], {}

            for source in sources:

                if type(source) == str:

                    list = BUILT_IN_SOURCES[source]()

                else:

                    list = source()

                for proxy in list:

                    proxy['address'] = '%s://%s:%s' % (proxy['type'], proxy['ip'], proxy['port'])

                    unique_proxies[proxy['address']] = proxy

            self.__list = [unique_proxies[key] for key in unique_proxies]

        update()

    def stop_update(self):

        self.__stop_update = True

    def get(self, selector = None):

        if selector:

            list = self.__list

            random.shuffle(list)

            for proxy in list:

                if self.__check_selector(proxy, selector):

                    return proxy

            return None

        else:

            return random.choice(self.__list)

    def get_all(self, selector = None):

        if selector:

            list = []

            for proxy in self.__list:

                if self.__check_selector(proxy, selector):

                    list.append(proxy)

            return list

        else:

            return self.__list