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


if __name__ == '__main__':
    app.run()
