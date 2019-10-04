""" file:    resolve.py (igsn-registry-mvp.api_namespaces)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019
    description: Demo resolver for when we don't want things to hook up to handle
"""
# pylint: disable=C0103

from pathlib import Path
import logging

from flask import current_app
from flask_restplus import Resource, Namespace, reqparse

from .. import validate

namespace = Namespace('igsn', description='IGSN registry/resolution', path='/igsn')

# Registration parsing
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument(
    'url',
    required=True,
    location=('values', 'json', 'form')
)
post_parser.add_argument(
    'registrant',
    required=True,
    location=('values', 'json', 'form')
)
post_parser.add_argument(
    'relatedResourceIdentifier',
    required=False,
    location=('values', 'json', 'form')
)
post_parser.add_argument(
    'log',
    required=False,
    location=('values', 'json', 'form')
)

# Todo: validate route using IGSN validator, with pluggable view, see http://flask.pocoo.org/docs/1.0/views/#views
@namespace.route('/<string:sampleNumber>')
class IGSN(Resource):

    def get(self, sampleNumber):
        "Resolve a sample"
        return {'sampleNumber': sampleNumber}

    @namespace.expect(post_parser)
    def post(self, sampleNumber):
        "Register a sample"
        data = post_parser.parse_args()
        current_app.logger.debug('Payload: %s', data)
        try:
            # Do the registration
            current_app.logger.info(f'Registering {sampleNumber}')
            return {'message': f'Registered sample {sampleNumber}'}

        except Exception as err:  # pylint: disable=W0703
            logging.exception('Hit exception, dumping debug info')
            return {"message": str(err)}, 422
