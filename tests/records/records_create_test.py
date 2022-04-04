import requests
from records_create_cases import _CASES
from argparse import ArgumentParser 

parser = ArgumentParser()
parser.add_argument('--url', required=True, 
                    help='The website URL. Specify port if needed. E.g http://localhost:8080')
parser.add_argument('--endpoint', required=True, 
                    help='The URL endpoint to perform tests')
args = vars(parser.parse_args())

with requests.Session() as s:
    # Login with test username and password
    payload = {
        'username' : 'nong003',
        'password' : 'qazwsx007'
    }
    p = s.post(f'{args["url"]}/auth/login', data=payload)

    # Perform tests
    headers = {
        'Content-Type' : 'application/json'
    }

    # Some color code
    success = '\033[92m'
    fail = '\033[31m'
    reset = '\033[0m'
    
    for _test in _CASES:
        _desc = _test['description']
        _payload = _test['payload']

        r = s.post(f'{args["url"]}{args["endpoint"]}', json=_payload, headers=headers)

        if('_code' not in r.json() or r.json()['_code'] != 'success'):
            print(f'{_desc} : {fail}Failed{reset}')
        elif(r.json()['_code'] == 'success'):
            print(f'{_desc} : {success}Success{reset}')