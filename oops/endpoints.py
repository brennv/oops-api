from .data import get_help
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


class Help(Resource):
    def get(self, issue):
        """
        Search issues
        ---
        tags:
          - help
        parameters:
          - name: issue
            in: path
            type: string
            required: true
            default: openshift Warning Failed sync Error syncing pod, skipping
        responses:
         200:
           description: Search issues
        """
        return get_help(issue), 200
