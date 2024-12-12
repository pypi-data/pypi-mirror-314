import os
from nacos import NacosClient

from easyuse_nacos import NacosConfigProperty, NacosConfig

os.environ['NACOS_SERVER'] = '43.144.249.194:8848'
os.environ['NACOS_NAMESPACE_ID'] = '792a9de5-764c-45cc-81c0-0fe53deb95af'
os.environ['NACOS_USERNAME'] = 'AKIDkPyQk9SqQs66sWyCrOhlhQEwVzXx9Zpz'
os.environ['NACOS_PASSWORD'] = '5ybHtGXikbQ6sY8dw2uZq0xhDXcT68pJ'



# client = NacosClient(server_addresses=os.environ['NACOS_SERVER'],
#                      namespace=os.environ['NACOS_NAMESPACE_ID'],
#                      username=os.environ['NACOS_USERNAME'],
#                      password=os.environ['NACOS_PASSWORD'])


class MyData(NacosConfig):
    for_nacos_test:int = NacosConfigProperty(default_value=1)

print(MyData.for_nacos_test)
print(MyData.for_nacos_test)
# import time

# while True:
#     print(MyData.for_nacos_test + 100)
#     time.sleep(3)
