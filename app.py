from oops.config import swagger_config, template, debug, threaded
# from oops.endpoints import (Health, Search, SearchOpenshift,
#                             SearchOpenshiftDocs, SearchOpenshiftBugs)
from flask import Flask, jsonify, redirect
from flask_restful import Api, Resource
from flasgger import Swagger

import yaml
from urllib.parse import quote
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os


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
options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
print(os.getenv("GOOGLE_CHROME_BIN"))
print(os.getenv("GOOGLE_CHROME_SHIM"))
options.add_argument('headless')
# options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(chrome_options=options)
# chrome_options=options,


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


from flask_restful import Resource


class Health(Resource):
    def get(self):
        """
        API health check
        ---
        tags:
          - status
        responses:
         200:
           description: Status check
        """
        return {'status': 'ok'}, 200


class Search(Resource):
    def get(self, issue):
        """
        Search
        ---
        tags:
          - search
        parameters:
          - name: issue
            in: path
            type: string
            required: true
            default: foo bar
        responses:
         200:
           description: Search
        """
        return get_results(issue, include='none', style='dict'), 200


class SearchOpenshift(Resource):
    def get(self, issue):
        """
        Search openshift docs and bugs
        ---
        tags:
          - openshift
        parameters:
          - name: issue
            in: path
            type: string
            required: true
            default: error syncing pod
        responses:
         200:
           description: Search openshift
        """
        if 'openshift' not in issue.lower():
            issue += ' openshift'
        return get_results(issue, include='all', style='dict'), 200


class SearchOpenshiftDocs(Resource):
    def get(self, issue):
        """
        Search openshift docs
        ---
        tags:
          - openshift
        parameters:
          - name: issue
            in: path
            type: string
            required: true
            default: error syncing pod
        responses:
         200:
           description: Search openshift docs
        """
        if 'openshift' not in issue.lower():
            issue += ' openshift'
        return get_results(issue, include='docs', style='dict'), 200


class SearchOpenshiftBugs(Resource):
    def get(self, issue):
        """
        Search openshift bugs
        ---
        tags:
          - openshift
        parameters:
          - name: issue
            in: path
            type: string
            required: true
            default: error syncing pod
        responses:
         200:
           description: Search openshift bugs
        """
        if 'openshift' not in issue.lower():
            issue += ' openshift'
        return get_results(issue, include='bugs', style='dict'), 200



app = Flask(__name__)
api = Api(app)
swagger = Swagger(app, template=template, config=swagger_config)

api.add_resource(Health, '/api/health')
api.add_resource(Search, '/api/search/<string:issue>')
api.add_resource(SearchOpenshift, '/api/search/openshift/<string:issue>')
api.add_resource(SearchOpenshiftDocs, '/api/search/openshift/docs/<string:issue>')
api.add_resource(SearchOpenshiftBugs, '/api/search/openshift/bugs/<string:issue>')


@app.route('/')
def index():
    return redirect('/api/spec/')


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Not found"}), 404


if __name__ == '__main__':
    try:
        app.run(debug=True, threaded=False)
    finally:
        driver.close()
