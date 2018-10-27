import jwt
import datetime
import time
# from jwt.algorithms import RSAAlgorithm
from private_config import priv_audience, priv_issuer, priv_token

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

with open('pubkey.pem') as f:
    PUBKEY = f.read()

with open('privkey.pem') as f:
    PRIVKEY = f.read()

with open('public_auth0.pem') as f:
    PUBKEY_AUTH0 = f.read()

with open('pubkey_auth0.pem', 'rb') as f:
    certificate_text = f.read()
    print(certificate_text)
    # certBytes = list(certificate_text.encode())
    # print(certBytes)
    certificate = load_pem_x509_certificate(certificate_text, default_backend())
    PUBKEY_AUTH0_509 = certificate.public_key()
    print('PUBKEY_AUTH0_509: {}'.format(PUBKEY_AUTH0_509))


def create_token(**data):
    return jwt.encode(data, PRIVKEY, algorithm='RS512')


def read_token(token):
    return jwt.decode(token, PUBKEY, algorithm='RS512')


def read_token_256(token, pubk=PUBKEY_AUTH0, verify=True, options=None):
    return jwt.decode(
        token,
        pubk,
        algorithm='RS256',
        verify=verify,
        options=options,
        audience=priv_audience,
        issuer=priv_issuer)


def test_token():
    token = priv_token
    options = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': True,
        'verify_iat': True,
        'verify_aud': False,
        'verify_iss': True,
        'require_exp': False,
        'require_iat': False,
        'require_nbf': False
    }
    read = read_token_256(token, PUBKEY_AUTH0_509, options)
    print(read)

    read = read_token_256(token)
    print(read)

    token = create_token(some='data are', inthe='token')
    print(token)

    read = read_token(token)
    print(read)

    # adding expiration time to token

    expire_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
    token = create_token(exp=expire_time)
    print(token)

    time.sleep(5)

    read = read_token(token)
    print(read)

    time.sleep(6)

    # the signature should be expired now
    try:
        read = read_token(token)
        print(read)
    except jwt.ExpiredSignatureError:
        print('# Signature has expired')


if __name__ == '__main__':
    test_token()
