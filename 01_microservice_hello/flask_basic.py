from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/api/hello')
def hello():
    ''' First Hello World
    Test it by: curl -v http://127.0.0.1:5000/api/hello
    '''

    return jsonify({'Hello': 'World'})


@app.route('/api/printdetails')
def printdetails():
    ''' First Hello World
    Test it by: curl -v http://127.0.0.1:5000/api/printdetails
    '''
    print(request)
    print(request.environ)
    response = jsonify({'Hello': 'World!'})
    print(response)
    print(response.data)
    return response


@app.route('/api/person/<int:person_id>')
def person(person_id: int):
    ''' returns details about specific person, based on id
    Built-in converters are
    - string (the default, a Unicode string), int, float, path, any, and uuid.
    
    Arguments:
        person_id {int}
    Test it by:
        curl -v http://127.0.0.1:5000/api/person/0
        curl -v http://127.0.0.1:5000/api/person/1
        curl -v http://127.0.0.1:5000/api/person/
        curl -v http://127.0.0.1:5000/api/person/a
        curl -v http://127.0.0.1:5000/api/person/-1 -> doesn't work: see flask_with_converter.py

    '''
    if (person_id > 0):
        response = jsonify({'Name': 'Great {}'.format(person_id)})
    elif (person_id > 0):
        response = jsonify({'Name': 'Negative {}'.format(person_id)})
        # negative number doesn't work - see the fix in flask_with_converter.py
    else:
        response = jsonify({'Name': 'Zero'})
    return response


if __name__ == '__main__':
    app.run()
