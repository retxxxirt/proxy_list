from .proxy_list import ProxyList

proxy_list = ProxyList()

update = proxy_list.update
stop_update = proxy_list.stop_update

get = proxy_list.get

check = proxy_list.check
check_many = proxy_list.check_many
