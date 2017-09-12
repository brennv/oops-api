import os

host = os.getenv('OOPS_API_HOST', '127.0.0.1:5000')
scheme = [x for x in [os.getenv('OOPS_API_SCHEME')] if x]

template = {
  # "host": "oops.vonapp.co",
  "host": host,
  # "schemes": ["https"],
  "schemes": scheme,
  # "schemes": ["https", "http"],
  "swagger": "2.0",
  "info": {
    "title": "Issue Finder API",
    "description": "API endpoints for " + host,
    "version": "0.1.0"
  },
  "basePath": "/",
  "operationId": "get_data",
  # set tag order
  "tags": [
      {"name": "search", "description": ""},
      {"name": "openshift", "description": ""},
      {"name": "status", "description": ""},
  ]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'spec',
            "name": 'oops',
            "route": '/api/spec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/spec/",
    'title': 'Issue Finder API',
}

if host == '127.0.0.1:5000':
    _debug = True
    _threaded = False
else:
    _debug = False
    _threaded = True

print(' * Host:', host)
print(' * Scheme:', scheme)
print(' * Debug:', _debug)
print(' * Threaded:', _threaded)
