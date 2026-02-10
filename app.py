from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Calculator API</title></head>
    <body>
        <h1>Calculator Web App</h1>
        <p>DAST тестирование демо</p>
        <h2>Endpoints:</h2>
        <ul>
            <li>GET /api/add?a=5&b=3</li>
            <li>GET /api/subtract?a=5&b=3</li>
            <li>POST /api/calculate { "operation": "add", "a": 5, "b": 3 }</li>
            <li>GET /api/users (требует auth)</li>
        </ul>
    </body>
    </html>
    '''

@app.route('/api/add')
def add():
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    return jsonify({'result': a + b})

@app.route('/api/subtract')
def subtract():
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    return jsonify({'result': a - b})

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    op = data.get('operation', 'add')
    a = data.get('a', 0)
    b = data.get('b', 0)
    
    if op == 'add':
        result = a + b
    elif op == 'subtract':
        result = a - b
    else:
        return jsonify({'error': 'Unknown operation'}), 400
    
    return jsonify({'result': result})

@app.route('/api/users')
def users():
    # Эмуляция endpoint, требующего аутентификацию
    auth = request.headers.get('Authorization')
    if auth != 'Bearer secret-token':
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'users': ['user1', 'user2']})

@app.route('/api/login', methods=['POST'])
def login():
    # Уязвимый endpoint для тестирования
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == 'admin' and password == 'admin123':
        return jsonify({'token': 'secret-token'})
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
