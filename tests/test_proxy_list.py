from proxy_list import ProxyList

proxy_list = ProxyList()

proxy_list.update()

def test_get_with_selector():

    proxy = proxy_list.get({'port': ['80', '8080'], 'country': 'US'})

    assert proxy['country'] == 'US' and proxy['port'] == '80' or '8080'

def test_get_all_with_selector():

    proxies = proxy_list.get_all({'port': ['80', '8080'], 'country': 'US'})

    for proxy in proxies:

        assert proxy['country'] == 'US' and proxy['port'] == '80' or '8080'
