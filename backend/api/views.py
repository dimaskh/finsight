from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connections
from django.db.utils import OperationalError
from redis import Redis
from redis.exceptions import RedisError
import psutil
import os

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint that verifies:
    1. API is responsive
    2. Database connection is working
    3. Redis connection is working
    4. System resources (memory, CPU)
    """
    # Check database connection
    db_healthy = True
    try:
        connections['default'].cursor()
    except OperationalError:
        db_healthy = False
    
    # Check Redis connection
    redis_healthy = True
    try:
        redis_client = Redis.from_url(os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0'))
        redis_client.ping()
    except RedisError:
        redis_healthy = False
    
    # System resources
    memory = psutil.virtual_memory()
    cpu_usage = psutil.cpu_percent(interval=1)
    
    status = {
        'status': 'healthy' if (db_healthy and redis_healthy) else 'unhealthy',
        'database': 'connected' if db_healthy else 'disconnected',
        'redis': 'connected' if redis_healthy else 'disconnected',
        'system': {
            'memory_usage': f"{memory.percent}%",
            'cpu_usage': f"{cpu_usage}%"
        }
    }
    
    return Response(status)
