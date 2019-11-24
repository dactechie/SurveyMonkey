import logging
import requests
from requests.exceptions import HTTPError
from .constants import LOGIC_APP_URI


def forward_results(results_json):
  try:
    r = requests.post(LOGIC_APP_URI, json=results_json)
    # If the response was successful, no Exception will be raised
    r.raise_for_status()
    
  except HTTPError as http_err:
    logging.error(f'HTTP error occurred: {http_err}') 
  except Exception as err:
    logging.exception(f'Other error occurred: {err}')
  else:
    logging.info(f"Succesfully transmitted json to Logic App. Status code {r.status_code}")
    #r.json()

# {'args': {},
#  'data': '{"key": "value"}',
#  'files': {},
#  'form': {},
#  'headers': {'Accept': '*/*',
#              'Accept-Encoding': 'gzip, deflate',
#              'Connection': 'close',
#              'Content-Length': '16',
#              'Content-Type': 'application/json',
#              'Host': 'httpbin.org',
#              'User-Agent': 'python-requests/2.4.3 CPython/3.4.0',
#              'X-Request-Id': 'xx-xx-xx'},
#  'json': {'key': 'value'},
#  'origin': 'x.x.x.x',
#  'url': 'http://httpbin.org/post'}