from proxy_list import ProxyList

proxy_list = ProxyList()

def test_stop_update():

    proxy_list.update(5)

    proxy_list.stop_update()