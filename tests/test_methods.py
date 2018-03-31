from proxy_list import ProxyList

proxy_list = ProxyList()

proxy_list.update(single_executing = True)

def test_get():

    proxy = proxy_list.get()

    assert 'ip' in proxy
    assert 'port' in proxy
    assert 'address' in proxy

    assert 'type' in proxy
    assert 'country' in proxy

def test_get_all():

    assert len(proxy_list.get_all()) != 0