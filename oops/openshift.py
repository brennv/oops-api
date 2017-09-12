import yaml
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


site_groups = '''
docs:
  - docs.openshift.com/container-platform/3.6
  - access.redhat.com/solutions
  - access.redhat.com/articles
  - kubernetes.io
  - docs.docker.com
bugs:
  - bugzilla.redhat.com
  - github.com/openshift
  - github.com/moby/moby
  - github.com/kubernetes/kubernetes
  - stackoverflow.com
  - trello.com
'''

openshift = yaml.load(site_groups)
openshift['all'] = openshift['bugs'] + openshift['docs']
openshift['none'] = []
options = webdriver.ChromeOptions()
# options.binary_location = '/usr/bin/google-chrome-unstable'
options.add_argument('headless')
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(chrome_options=options)


def make_url(issue, sites=[]):
    """ Compose search terms and sites with url safe encoding. """
    print('issue', issue)
    terms = issue.strip().split()
    terms = [quote(x, safe='') for x in terms]  # TODO test with just spaces
    url = 'https://duckduckgo.com/?q=' + '+'.join(terms)
    if sites:
        url += '+' + quote('site:' + ','.join(sites)) + '&ia=web'
    print(url)
    return url


def text_format(results):
    text_results = ''
    for r in results:
        spacer = ' ' * len(str(r['id']))
        blob = f"""
            {r['id']} {r['title']}
            spacer {r['snip']}
            spacer {r['url']}""".strip() + '\n'
        text_results += blob
    return text_results


def get_results(issue, include, style='dict'):
    url = make_url(issue, sites=openshift[include])
    driver.get(url)
    print('page title', driver.title)
    divs = driver.find_elements_by_class_name('result__body')
    print('div count', len(divs))
    print()
    results = []
    for div in divs:
        hit = div.find_element_by_class_name('result__a')
        title = hit.text
        link = hit.get_attribute('href')
        try:
            snippet = div.find_element_by_class_name('result__snippet').text
        except NoSuchElementException:
            snipppet = ''
        result = {'title': title, 'url': link, 'snippet': snippet}
        # print(result)
        results.append(result)
    return results


# driver.close()
