import os
import time
from importlib import import_module
from functools import partial
from threading import Thread

class Parser:

    def __init__(self):

        self.__parsers = []
        self.__parsers_by_name = {}
        self.__parsers_by_group = {}
        self.__default_parsers_argument = []

        directory = '%s/parsers/' % os.path.dirname(os.path.realpath(__file__))

        for file in os.listdir(directory):

            if os.path.isfile('%s%s' % (directory, file)):

                module = import_module('proxy_list.parsers.' + file[:-3])

                self.__parsers_by_group[module.group] = []

                for parser in module.parsers:

                    self.__parsers.append({

                        'name': parser.__name__,
                        'group': module.group,
                        'parser': parser
                    })

                    self.__parsers_by_name[parser.__name__] = self.__parsers[-1]

                    self.__parsers_by_group[module.group].append(self.__parsers[-1])

                    self.__default_parsers_argument.append(parser.__name__)

    @staticmethod
    def __get_parsers(handled_parsers):

        parsers = []

        for group in handled_parsers:

            for parser in group:

                parsers.append(parser)

        return parsers

    @staticmethod
    def __get_parsers_safe(handled_parsers):

        parsers = []

        for group in handled_parsers:

            def parse(parsers):

                proxies = []

                for parser in parsers:

                    proxies += parser()

                    time.sleep(1)

                return proxies

            parsers.append(partial(parse, group))

        return parsers

    def __handle_parsers(self, parsers_argument):

        if parsers_argument is None:

            parsers_argument = self.__default_parsers_argument

        if type(parsers_argument) is not list:

            parsers_argument = [parsers_argument]

        built_in_parsers, custom_parsers, disable_mode = [], [], False

        for parser_argument in parsers_argument:

            def change_built_in_parsers(parser_argument, action):

                if parser_argument in self.__parsers_by_group:

                    for parser in self.__parsers_by_group[parser_argument]:

                        getattr(built_in_parsers, action)(parser)

                else:

                    getattr(built_in_parsers, action)(self.__parsers_by_name[parser_argument])

            if type(parser_argument) is str:

                if parser_argument[0] == '-':

                    if not disable_mode:

                        disable_mode = True

                        built_in_parsers = self.__parsers.copy()

                    change_built_in_parsers(parser_argument[1:], 'remove')

                else:

                    change_built_in_parsers(parser_argument, 'append')

            elif type(parser_argument) == list:

                custom_parsers.append(parser_argument)

            else:

                custom_parsers.append([parser_argument])

        built_in_parsers_by_group = {}

        for parser in built_in_parsers:

            if parser['group'] not in built_in_parsers_by_group:

                built_in_parsers_by_group[parser['group']] = []

            built_in_parsers_by_group[parser['group']].append(parser)

        built_in_parsers = []

        for group in built_in_parsers_by_group:

            built_in_parsers.append([parser['parser'] for parser in built_in_parsers_by_group[group]])

        return built_in_parsers + custom_parsers

    def parse(self, parsers, safe_parse):

        parsers = self.__handle_parsers(parsers)

        if safe_parse:

            parsers = self.__get_parsers_safe(parsers)

        else:

            parsers = self.__get_parsers(parsers)

        threads, proxies = [], []

        for parser in parsers:

            def parse(parser):

                for proxy in parser():

                    proxies.append(proxy)

            threads.append(Thread(target = parse, args = [parser]))

        for thread in threads:

            thread.start()

        for thread in threads:

            thread.join()

        return proxies