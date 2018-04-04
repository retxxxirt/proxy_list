from proxy_list import ProxyList

def check_with_specified_arguments(*args, **kwargs):

    proxy_list = ProxyList()

    proxy_list.update(*args, **kwargs)

    proxies = proxy_list.get_all()

    assert len(proxies) != 0

    for proxy in proxies:

        assert 'address' and 'ip' and 'port' and 'type' and 'country' in proxy

def test_default():

    check_with_specified_arguments()

def test_check():

    check_with_specified_arguments(check = True)

def test_specified_parsers():

    check_with_specified_arguments(['free-proxy-list.net', 'hidester.com'])

def test_disabled_parsers():

    check_with_specified_arguments('-spys.one')

def test_unsafe_parse():

    check_with_specified_arguments('free-proxy-list.net', safe_parse = False)