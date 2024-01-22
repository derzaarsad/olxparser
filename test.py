import requests
import sys

x = requests.post('http://localhost:9019/2015-03-31/functions/function/invocations', json = {})
print(x.content)
