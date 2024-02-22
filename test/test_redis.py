
import redis

r = redis.StrictRedis(host='localhost', port=6379, password='mypassword', db=0)
try:
    r.ping()
    print("Connected to Redis")
except redis.ConnectionError:
    print("Failed to connect to Redis")
