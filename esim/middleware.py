import redis
from django.http import JsonResponse


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0)

        self.limit = 100
        self.fixed_window_seconds = 60
    
    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR", "unknown")
        key = f"rate_limit:{ip}"

        try:
            # increment counter first to be accurate on race conditions
            current_count = self.redis_client.incr(key)

            # if first request, set expiry (ttl, I am giving it as 60 seconds for the fixed window)
            if current_count == 1:
                self.redis_client.expire(key, self.fixed_window_seconds)

            # block if exceeds limit
            if current_count > self.limit:
                return JsonResponse(
                    {
                        "error": "Rate limit exceeded",
                        "limit": self.limit,
                        "window_seconds": self.fixed_window_seconds,
                    },
                    status=429, #429 is the status code for rate limit exceeded
                )

        except Exception:
            # If Redis fails, DO NOT block the user (fail-open)
            pass

        response = self.get_response(request)
        return response