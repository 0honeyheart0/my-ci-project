from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import time

app = Flask(__name__)

# Метрики
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

@app.route('/api/add') #d
def add():
    try:
        a = int(request.args.get('a', 0))
        b = int(request.args.get('b', 0))
    except (TypeError, ValueError):
        return jsonify({'error': 'Parameters a and b must be integers'}), 400
    return jsonify(result=a + b)

@app.route('/')
def home():
    return "Hello, DAST with Prometheus!"

if __name__ == '__main__':
    # Важно: слушаем все интерфейсы (0.0.0.0), чтобы контейнер был доступен
    app.run(host='0.0.0.0', port=5000, debug=False)
