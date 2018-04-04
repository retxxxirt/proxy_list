import time

from proxy_list import ProxyList
import proxy_list.parsers.spys_one as spys_one
import proxy_list.parsers.hidester_com as hidester_com
import proxy_list.parsers.free_proxy_list_net as free_proxy_list_net

def check_parser_valid(parsers, min_proxies):

    for parser in parsers:

        proxies = parser()

        assert len(proxies) >= min_proxies

        for proxy in proxies:

            assert 'ip' and 'port' and 'type' and 'country' in proxy

        time.sleep(1)

def check_group_valid(group, min_proxies):

    proxy_list = ProxyList()

    proxy_list.update(group)

    proxies = proxy_list.get_all()

    assert len(proxies) >= min_proxies

    for proxy in proxies:

        assert 'address' and 'ip' and 'port' and 'type' and 'country' in proxy

def test_parsers_spys_one():

    check_parser_valid(spys_one.parsers, 500)

def test_parsers_hidester_com():

    check_parser_valid(hidester_com.parsers, 1000)

def test_parsers_free_proxy_list_net():

    min_proxies = {

        'free_proxy_list_net': 300,
        'free_proxy_list_net_uk_proxy_html': 100,
        'free_proxy_list_net_anonymous_proxy_html': 100,
        'us_proxy_org': 200,
        'socks_proxy_net': 80,
        'sslproxies_org': 100
    }

    for parser in free_proxy_list_net.parsers:

        check_parser_valid([parser], min_proxies[parser.__name__])

def test_proxy_list_with_spys_one_parsers():

    check_group_valid('spys.one', 1500)

def test_proxy_list_with_hidester_com_parsers():

    check_group_valid('hidester.com', 1200)

def test_proxy_list_with_free_proxy_list_net_parsers():

    check_group_valid('free-proxy-list.net', 600)

