import time

from proxy_list import ProxyList

def proxies_are_valid(proxies):

    assert len(proxies) != 0

    for proxy in proxies:

        assert 'address' and 'ip' and 'port' and 'type' and 'country' in proxy

def test_default_update():

    proxy_list = ProxyList()

    proxy_list.update()

    proxies_are_valid(proxy_list.get_all())

def test_update_with_check():

    proxy_list = ProxyList()

    proxy_list.update(check = True)

    proxies_are_valid(proxy_list.get_all())

def test_update_daemon():

    proxy_list = ProxyList()

    proxy_list.start_update(120)

    proxies_first = proxy_list.get_all()

    proxies_are_valid(proxies_first)

    time.sleep(180)

    proxy_list.stop_update()

    proxies_second = proxy_list.get_all()

    proxies_are_valid(proxies_second)

    assert proxies_first != proxies_second