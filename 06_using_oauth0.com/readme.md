# Simple OAuth API client

Source: [auth0.com: Python API Authorization Tutorial](https://auth0.com/docs/quickstart/backend/python/01-authorization)

## Preconditions

- Create account on [oauth0.com](https://auth0.com) and follow tutorials there
- Install following packages:

``` bash
conda install -c conda-forge flask
conda install -c conda-forge python-dotenv
pip install python-jose-cryptodome
conda install -c conda-forge flask-cors
conda install -c conda-forge six
```

## How to test it

- Get token via postman or curl:

``` bash
curl -X POST \
  https://suk.eu.auth0.com/oauth/token \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d @get_token_body.private
```

Example of 'get_token_body.private'

``` json
{
    "client_id":        "<your_client_id>",
    "client_secret":    "<your_client_secret>",
    "audience":         "<audience - url to your API service>",
    "grant_type":       "client_credentials"
}
```

- Copy access token to auth_bearer.private as

``` bash
-H  "Authorization: Bearer <your_token>"
```

and use curl to test it:

``` bash
curl --url 'http://localhost:3010/api/update' --config auth_bearer.private
curl --url 'http://localhost:3010/api/readupdate' --config auth_bearer.private
curl --url 'http://localhost:3010/api/noaccess' --config auth_bearer.private
```
