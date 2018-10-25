import jwt


def create_token(alg='HS256', secret='agent007', **data):
    return jwt.encode(data, secret, algorithm=alg)


def read_token(token, secret='agent007', algs=['HS256']):
    return jwt.decode(token, secret)


def test_token():
    token = create_token(some='data', inthe='token')
    print(token)
    read = read_token(token)
    print(read)


if __name__ == '__main__':
    test_token()
