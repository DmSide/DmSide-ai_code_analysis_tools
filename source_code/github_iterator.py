import requests

session = requests.Session()

def get_jobs():
    url = 'https://api.github.com/search/repositories?q=machine+learning+language:python'
    first_page = session.get(url).json()
    yield first_page
    num_pages = first_page['last_page']

    for page in range(2, num_pages + 1):
        next_page = session.get(url, params={'page': page}).json()
        yield next_page['page']

for page in get_jobs():

    np = page
    x = 0

x = 0