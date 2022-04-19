import requests 
from argparse import ArgumentParser

from cases import _TESTS

parser = ArgumentParser()
parser.add_argument('--url', required=True, 
                    help='The website URL. Specify port if needed. E.g http://localhost:8080')
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

    # Insert all patient records
    print('[INFO] Creating patient records ... ')
    for i, _test in enumerate(_TESTS['patients']):
        r = s.post(f'{args["url"]}/records/create', json=_test, headers=headers)
        
        if('_code' not in r.json() or r.json()['_code'] != 'success'):
            print(f'Test case #{i+1} : {fail}Failed{reset}')
        elif(r.json()['_code'] == 'success'):
            print(f'Test case #{i+1} : {success}Success{reset}')

    # Insert all diagnosis records
    print('[INFO] Creating diagnosis record ... ')
    for i, _test in enumerate(_TESTS['diagnosis']):
        files = {'xray' : open(_test['xray'], 'rb')}
        payload = {'nric' : _test['nric']}

        r = s.post(f'{args["url"]}/records/upload_xray', data=payload, files=files)

        if('_code' not in r.json() or r.json()['_code'] != 'success'):
            print(f'Test case #{i+1} : {fail}Failed{reset}')
        elif(r.json()['_code'] == 'success'):
            print(f'Test case #{i+1} : {success}Success{reset}')