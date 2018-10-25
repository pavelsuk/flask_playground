from flask import Flask, jsonify
from werkzeug.routing import BaseConverter, ValidationError

_USERS = {'1': 'Tarek', '2': 'Freya'}
_IDS = {val: id for id, val in _USERS.items()}


class RegisteredUser(BaseConverter):
    ''' Test it via
    curl localhost:5000/api/person/1
    curl localhost:5000/api/person/2
    curl localhost:5000/api/person/0
    
    '''

    def to_python(self, value):
        if value in _USERS:
            return _USERS[value]
        else:
            print(value)
            try:
                id = int(value)
                name_prefix = 'Great {}' if (id > 0) else 'Zero {}' if (id == 0) else 'Minor {}'
                return name_prefix.format(id)
            except ValueError:
                raise ValidationError()

    def to_url(self, value):
        return _IDS[value]


app = Flask(__name__)
app.url_map.converters['registered'] = RegisteredUser


@app.route('/api/person/<registered:name>')
def person(name):
    response = jsonify({'Hello hey': name})
    return response


if __name__ == '__main__':
    app.run()
