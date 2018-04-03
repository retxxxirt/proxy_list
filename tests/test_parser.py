import time

from proxy_list import ProxyList

def check_parse_is_valid(parsers, min_proxies):

    for parser in parsers:

        proxies = parser()

        assert len(proxies) >= min_proxies

        for proxy in proxies:

            assert 'ip' and 'port' and 'type' and 'country' in proxy

        time.sleep(1)

def check_group_parsers_is_valid(group, min_proxies):

    proxy_list = ProxyList()

    proxy_list.update(group)

    proxies = proxy_list.get_all()

    assert len(proxies) >= min_proxies

    for proxy in proxies:

        assert 'address' and 'ip' and 'port' and 'type' and 'country' in proxy

def test_parsers_spys_one():

    from proxy_list.parser.built_in.spys_one import parsers

    check_parse_is_valid(parsers, 500)

def test_parsers_hidester_com():

    from proxy_list.parser.built_in.hidester_com import parsers

    check_parse_is_valid(parsers, 1000)

def test_parsers_free_proxy_list_net():

    from proxy_list.parser.built_in.free_proxy_list_net import parsers

    min_proxies = {

        'free_proxy_list_net': 300,
        'free_proxy_list_net_uk_proxy_html': 100,
        'free_proxy_list_net_anonymous_proxy_html': 100,
        'us_proxy_org': 200,
        'socks_proxy_net': 80,
        'sslproxies_org': 100
    }

    for parser in parsers:

        check_parse_is_valid([parser], min_proxies[parser.__name__])

def test_proxy_list_with_spys_one_parsers():

    check_group_parsers_is_valid('spys.one', 1500)

def test_proxy_list_with_hidester_com_parsers():

    check_group_parsers_is_valid('hidester.com', 1200)

def test_proxy_list_with_free_proxy_list_net_parsers():

    check_group_parsers_is_valid('free-proxy-list.net', 600)

