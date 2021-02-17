# pylint: disable=invalid-name
"""This module wrapping and provide easy access to generate JWT key """
import time
import hashlib
import jwt


class JWTGenerator:
    """ This class wrap jwt library """
    def __init__(self, account_id, access_key, secret_key, canonical_path):
        self.account_id = account_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.expire = 3600
        self.canonical_path = canonical_path

    def jwt(self):
        """ create jwt token"""
        payload = {
            'sub': self.account_id,
            'qsh': hashlib.sha256(self.canonical_path.encode('utf-8')).hexdigest(),
            'iss': self.access_key,
            'exp': time.time()+self.expire,
            'iat': time.time()
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')

        return token

    def headers(self):
        """This generate standard header dict for jwt request"""
        headers = {
            'Authorization': 'JWT ' + self.jwt(),
            # 'Authorization': self.jwt(),
            'Content-Type': 'application/json',
            'zapiAccessKey': self.access_key
        }
        return headers
