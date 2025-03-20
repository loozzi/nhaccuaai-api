import google.oauth2.id_token as gid_token
from google.auth.transport import requests


class FirebaseService:
    def __init__(self):
        pass

    def verify(self, token: str) -> gid_token:
        """
        Verify a Firebase token
        :param token: The token to be verified
        :return: The token claims if the token is valid, None otherwise
        """
        try:
            claims = gid_token.verify_firebase_token(token, requests.Request())
            if not claims:
                return None

            return claims
        except ValueError:
            raise ValueError("Invalid token")
