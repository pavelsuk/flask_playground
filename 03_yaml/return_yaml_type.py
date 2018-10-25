from flask import Flask
import yaml  # requires PyYAML

app = Flask(__name__)


def yamlify(data, status=200, headers=None):
    _headers = {'Content-Type': 'application/x-yaml'}
    if headers is not None:
        _headers.update(headers)
    return yaml.safe_dump(data), status, _headers


@app.route('/api')
def my_microservice():
    '''[summary]
    test it by curl -v http://localhost:5000/api
    '''

    return yamlify(['Hello', 'YAML', 'World!'])


if __name__ == '__main__':
    app.run()
