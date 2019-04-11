import sys
import requests
from bs4 import BeautifulSoup

def destroy(screen_name, password):
    if not is_exists_account(screen_name):
        return print('the account is not found.')

    session = requests.session()
    authenticity_token = fetch_authenticity_token(session)
    login(session, screen_name, password, authenticity_token)

    url = 'https://twitter.com/settings/account/deactivate'
    headers = {
        'referer': 'https://twitter.com/settings/accounts/confirm_deactivation',
    }
    data = {
        '_method': 'delete',
        'authenticity_token': authenticity_token,
        'auth_password': password,
    }
    session.post(url, headers=headers, data=data)

    if is_exists_account(screen_name):
        return print('failed to destroy.')

    return screen_name

def fetch_authenticity_token(session):
    url = 'https://twitter.com'
    soup = BeautifulSoup(session.get(url).text, 'lxml')
    return soup.find(attrs={'name': 'authenticity_token'}).get('value')

def login(session, screen_name, password, authenticity_token):
    url = 'https://twitter.com/sessions'
    data = {
        'session[username_or_email]': screen_name,
        'session[password]': password,
        'authenticity_token': authenticity_token,
    }
    res = session.post(url, data=data)

def is_exists_account(screen_name):
    url = 'https://twitter.com/{}'.format(screen_name)
    return (requests.get(url).status_code == 200)

def usage():
    print('usage: python destroy.py [screen name] [password]')

def main():
    if len(sys.argv) != 3:
        return usage()

    if destroy(sys.argv[1], sys.argv[2]):
        print('successfully destroyed.')

if __name__ == '__main__':
    main()
