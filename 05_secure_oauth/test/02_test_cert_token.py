import jwt
import datetime
import time

with open('pubkey.pem') as f:
    PUBKEY = f.read()

with open('privkey.pem') as f:
    PRIVKEY = f.read()


def create_token(**data):
    return jwt.encode(data, PRIVKEY, algorithm='RS512')


def read_token(token):
    return jwt.decode(token, PUBKEY, algorithm='RS512')


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
