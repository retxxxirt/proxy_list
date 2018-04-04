import time

from proxy_list import ProxyList

def proxies_valid(proxies):

    assert len(proxies) != 0

    for proxy in proxies:

        assert 'address' and 'ip' and 'port' and 'type' and 'country' in proxy

def check_with_specified_arguments(*args, **kwargs):

    proxy_list = ProxyList()

    proxy_list.start_update(*args, **kwargs)

    proxies_first = proxy_list.get_all()

    proxies_valid(proxies_first)

    time.sleep(kwargs['interval'] * 1.3)

    proxy_list.stop_update()

    proxies_second = proxy_list.get_all()

    proxies_valid(proxies_second)

    assert proxies_first != proxies_second

def test_default():

    check_with_specified_arguments(interval = 120)

def test_check():

    check_with_specified_arguments(interval = 600, check = True)

def test_specified_parsers():

    check_with_specified_arguments(interval = 120, parsers = ['free-proxy-list.net', 'hidester.com'])

def test_disabled_parsers():

    check_with_specified_arguments(interval = 120, parsers ='-spys.one')

def test_unsafe_parse():

    check_with_specified_arguments(interval = 120, parsers ='free-proxy-list.net', safe_parse = False)

