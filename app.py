import os
import psycopg2
import jwt
import time
import bcrypt
import datetime
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify, g
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'Goooooooosseeeee')
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=1)

DB_HOST = os.getenv('DB_HOST', 'db')  
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        cursor_factory=RealDictCursor
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS calculations (
            id SERIAL PRIMARY KEY,
            a INTEGER,
            b INTEGER,
            result INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
    print("BD working))")

init_db()

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
def generate_token(username: str) -> str:
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print(f"Decoded data: {data}")  # добавить
            g.current_user = data['username']
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            print(f"Token error: {e}")  # добавить
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(*args, **kwargs)
    return decorated
    
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    hashed = hash_password(password)
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed)
        )
        conn.commit()
    except psycopg2.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 409
    finally:
        cur.close()
        conn.close()
    return jsonify({'message': 'User created successfully'}), 201
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user or not check_password(password, user['password_hash']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = generate_token(username)
    return jsonify({'token': token}), 200
    
@app.route('/profile', methods=['GET'])
@token_required
def profile():
    return jsonify({'username': g.current_user}), 200
    
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_COUNT.labels(request.method, request.path).inc()
    REQUEST_LATENCY.labels(request.method, request.path).observe(latency)
    return response

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain'}

@app.route('/api/add')
def add():
    try:
        a = int(request.args.get('a', 0))
        b = int(request.args.get('b', 0))
    except (TypeError, ValueError):
        return jsonify({'error': 'Parameters a and b must be integers'}), 400

    result = a + b

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO calculations (a, b, result) VALUES (%s, %s, %s)",
        (a, b, result)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(result=result)

@app.route('/')
def home():
    return "krivoy test"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
