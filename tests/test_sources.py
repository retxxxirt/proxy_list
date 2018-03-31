from proxy_list.sources import *

def test_free_proxy_list_net():

    assert len(free_proxy_list_net()) != 0

def test_spys_one():

    assert len(spys_one()) != 0

def test_hidester_com():

    assert len(hidester_com()) != 0