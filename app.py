from oops.config import swagger_config, template, debug, threaded
from oops.endpoints import (Health, Search, SearchOpenshift,
                            SearchOpenshiftDocs, SearchOpenshiftBugs)
from flask import Flask, jsonify, redirect
from flask_restful import Api, Resource
from flasgger import Swagger

import os


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
    for dirname, dirnames, filenames in os.walk('/usr/bin/'):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            path = os.path.join(dirname, subdirname)
            if 'chrom' in path:
                print(path)
        # print path to all filenames.
        for filename in filenames:
            path = os.path.join(dirname, filename)
            if 'chrom' in path:
                print(path)

    app.run(debug=debug, threaded=False)
