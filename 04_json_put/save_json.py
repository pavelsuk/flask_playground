from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/api/file', methods=['GET', 'POST', 'PATCH', 'PUT'])
def api_file():
    '''[summary]
    test it by
        curl -v http://localhost:5000/api/file
        curl -vX PUT http://localhost:5000/api/file -d @testdata.json --header "Content-Type: application/json"
    '''
    if request.method == 'GET':
        return "ECHO: GET\n"
    elif request.method in ['POST', 'PATCH', 'PUT']:
        if not request.json:
            return jsonify({'error': '400', 'text': 'Content-Type must be application/json'}), '400'
        return jsonify({'cmd': '{}'.format(request.method), 'data': request.json})


if __name__ == '__main__':
    app.run()
