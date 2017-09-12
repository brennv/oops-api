from .openshift import get_results
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
