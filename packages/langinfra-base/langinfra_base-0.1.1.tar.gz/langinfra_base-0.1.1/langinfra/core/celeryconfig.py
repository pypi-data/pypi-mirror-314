# celeryconfig.py
import os

langinfra_redis_host = os.environ.get("LANGINFRA_REDIS_HOST")
langinfra_redis_port = os.environ.get("LANGINFRA_REDIS_PORT")
# broker default user

if langinfra_redis_host and langinfra_redis_port:
    broker_url = f"redis://{langinfra_redis_host}:{langinfra_redis_port}/0"
    result_backend = f"redis://{langinfra_redis_host}:{langinfra_redis_port}/0"
else:
    # RabbitMQ
    mq_user = os.environ.get("RABBITMQ_DEFAULT_USER", "langinfra")
    mq_password = os.environ.get("RABBITMQ_DEFAULT_PASS", "langinfra")
    broker_url = os.environ.get("BROKER_URL", f"amqp://{mq_user}:{mq_password}@localhost:5672//")
    result_backend = os.environ.get("RESULT_BACKEND", "redis://localhost:6379/0")
# tasks should be json or pickle
accept_content = ["json", "pickle"]
