from proxy_list.parsers.spys_one import spys_one
from proxy_list.parsers.hidester_com import hidester_com
from proxy_list.parsers.free_proxy_list_net import free_proxy_list_net

def check_proxies(proxies, min_number):

    assert len(proxies) >= min_number

    for proxy in proxies:

        assert 'ip' and 'port' and 'type' and 'country' in proxy

def test_spys_one():

    check_proxies(spys_one(), 2500)

def test_hidester_com():

    check_proxies(hidester_com(), 1200)

def test_free_proxy_list_net():

    check_proxies(free_proxy_list_net(), 800)



