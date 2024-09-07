from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication 

class TokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class JWTTokenAuthentication(JWTAuthentication):
    keyword = 'Bearer'
