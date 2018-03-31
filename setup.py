from distutils.core import setup

setup(

    name = 'proxy_list',
    packages = ['proxy_list'],
    version = '0.1.4',
    description = 'Free proxy lists',
    author = 'retxxxirt',
    author_email = 'retxxirt@gmail.com',
    url = 'https://github.com/retxxxirt/proxy_list',
    keywords = ['proxy', 'proxies', 'proxy list', 'free proxy', 'free proxies'],
    install_requires = ['requests', 'pyquery', 'iso3166']
)