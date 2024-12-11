from redis_helper import RedisHelper

class HandshakeCheck():
    def __init__(self):
        self.redis = RedisHelper()

    def check_handshake(self, service_id):
        try:
            # Get the value from the redis
            value = self.redis.get_value(service_id)
            if value:
                return True
            else:
                return False
        except Exception as e:
            return False

    def negate_handshake(self, service_id):
        try:
            # Delete the key from the redis
            self.redis.delete_key(service_id)
            return True
        except Exception as e:
            return False
