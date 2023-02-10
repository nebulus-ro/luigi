import os
from getpass import getpass
import urllib.parse

password = getpass()

proxy = f'http://felecni:{urllib.parse.quote(password)}@ps-bxl-usr.cec.eu.int:8012'

# os.environ['http_proxy'] = proxy 
# os.environ['https_proxy'] = proxy

print(f'set http_proxy={proxy}')
print(f'set https_proxy={proxy}')