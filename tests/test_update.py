from proxy_list import ProxyList

def check_proxies(proxies, min_number, selector = None):

    selector = selector if selector else {}

    assert len(proxies) >= min_number

    for key in selector:

        if type(selector[key]) != list:

            selector[key] = [selector[key]]

    for proxy in proxies:

        assert 'url' and 'ip' and 'port' and 'type' and 'country' in proxy

        for key in selector:

            assert proxy[key] in selector[key]

def test_default():

    check_proxies(ProxyList().update(), 3000)

def test_with_check():

    check_proxies(ProxyList().update(check = True), 800)

def test_with_specified_parsers():

    from proxy_list.parsers.free_proxy_list_net import free_proxy_list_net

    check_proxies(ProxyList().update(parsers = [free_proxy_list_net]), 800)

def test_with_disabled_parsers():

    from proxy_list.parsers.spys_one import spys_one

    check_proxies(ProxyList().update(disabled_parsers = [spys_one]), 2000)

def test_with_specified_url():

    check_proxies(ProxyList().update(check = True, url ='google.com'), 1000000)

def test_with_selector():

    selector = {'country': 'US', 'port': ['80', '8080']}

    check_proxies(ProxyList().update(selector = selector), 150, selector)

def test_with_interval():

    proxy_list = ProxyList()

    proxy_list.update(interval = 120)

    proxies_first = proxy_list.get()

    check_proxies(proxies_first, 3000)

    proxies_second = proxy_list.get()

    check_proxies(proxies_second, 3000)

    assert proxies_first != proxies_second

