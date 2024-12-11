# user_management/middlewares/prometheus_middleware.py
import time
from prometheus_client import Counter, Histogram

http_requests_total = Counter(
    name='http_requests_total',
    documentation='Total number of HTTP requests',
    labelnames=['method', 'path', 'status'],
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'path'],
)

class PrometheusMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.prometheus_start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - request.prometheus_start_time

        http_requests_total.labels(
            method=request.method,
            path=request.path,
            status=response.status_code,
        ).inc()

        http_request_duration_seconds.labels(
            method=request.method,
            path=request.path,
        ).observe(duration)

        return response