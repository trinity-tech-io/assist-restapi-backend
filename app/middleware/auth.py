# -*- coding: utf-8 -*-

from app import config
from app.errors import UnauthorizedError


class AuthMiddleware(object):

    def process_request(self, req, res):
        token = req.get_header('Authorization')

        if token is None:
            description = 'Please provide an auth token as part of the request'
            raise UnauthorizedError(description)

        if not self._token_is_valid(token):
            description = 'The provided auth token is not valid'
            raise UnauthorizedError(description)

    def _token_is_valid(self, token):
        if config.SECRET_KEY != token:
            return False
        return True
