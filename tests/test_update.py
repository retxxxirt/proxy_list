import time

from proxy_list import ProxyList
from proxy_list import utilities

def check_proxies(proxies, min_number, selector = None):

    assert len(proxies) >= min_number

    for proxy in proxies:

        utilities.validate_proxy(proxy)

        if selector:

            utilities.validate_selector(proxy, selector)

def test_default():

    check_proxies(ProxyList().update(), 2000)

def test_with_check():

    check_proxies(ProxyList().update(check = True), 350)

def test_with_specified_parsers():

    from proxy_list.parsers.free_proxy_list_net import free_proxy_list_net

    check_proxies(ProxyList().update(parsers = [free_proxy_list_net]), 600)

def test_with_disabled_parsers():

    from proxy_list.parsers.hidester_com import hidester_com

    check_proxies(ProxyList().update(disabled_parsers = [hidester_com]), 600)

def test_with_specified_url():

    check_proxies(ProxyList().update(url = 'https://google.com/'), 250)

def test_with_selector():

    selector = {'country': 'US', 'port': ['80', '8080']}

    check_proxies(ProxyList().update(selector = selector), 150, selector)

def test_with_interval():

    proxy_list = ProxyList()

    proxy_list.update(interval = 120)

    proxies_first = proxy_list.get()

    check_proxies(proxies_first, 2000)

    time.sleep(180)

    proxies_second = proxy_list.get()

    check_proxies(proxies_second, 2000)

    assert proxies_first != proxies_second

