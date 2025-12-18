import requests
from bs4 import BeautifulSoup as bs
from requests.auth import HTTPBasicAuth


username='rishabhverma3648@gmail.com'
password='rishi@2003'

url="https://www.linkedin.com/jobs/view/research-engineer-ai-at-shl-4194768899/?originalSubdomain=in"

response=requests.get(url,auth=HTTPBasicAuth(username,password))

print(response)
print(response.text)
