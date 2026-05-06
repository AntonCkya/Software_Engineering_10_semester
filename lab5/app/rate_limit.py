import time
from typing import Dict, List, Optional
from collections import deque
import hashlib


class RateLimiter:
    def __init__(self):
        self.sliding_windows: Dict[str, deque] = {}
        self.token_buckets: Dict[str, Dict] = {}

    def _get_key(self, identifier: str, endpoint: str) -> str:
        return f"{endpoint}:{identifier}"

    def _cleanup_sliding_window(self, key: str, window_size: int = 60):
        if key not in self.sliding_windows:
            return

        now = time.time()
        while self.sliding_windows[key] and now - self.sliding_windows[key][0] > window_size:
            self.sliding_windows[key].popleft()

    def check_sliding_window(self, identifier: str, endpoint: str, limit: int, window_size: int = 60) -> tuple[bool, int, int]:
        key = self._get_key(identifier, endpoint)

        if key not in self.sliding_windows:
            self.sliding_windows[key] = deque()

        self._cleanup_sliding_window(key, window_size)

        current_count = len(self.sliding_windows[key])
        allowed = current_count < limit

        if allowed:
            self.sliding_windows[key].append(time.time())

        remaining = max(0, limit - current_count - (0 if allowed else 1))

        reset = 0
        if self.sliding_windows[key]:
            reset = int(window_size - (time.time() - self.sliding_windows[key][0]))
        else:
            reset = window_size

        return allowed, remaining, max(1, reset)

    def _get_token_bucket(self, key: str, capacity: int, refill_rate: float) -> Dict:
        """Получает или создает token bucket"""
        if key not in self.token_buckets:
            self.token_buckets[key] = {
                'tokens': capacity,
                'last_refill': time.time(),
                'capacity': capacity,
                'refill_rate': refill_rate
            }
        return self.token_buckets[key]

    def _refill_tokens(self, bucket: Dict):
        now = time.time()
        time_passed = now - bucket['last_refill']

        new_tokens = time_passed * bucket['refill_rate']
        bucket['tokens'] = min(bucket['capacity'], bucket['tokens'] + new_tokens)
        bucket['last_refill'] = now

    def check_token_bucket(self, identifier: str, endpoint: str, capacity: int, refill_rate: float) -> tuple[bool, int, int]:
        key = self._get_key(identifier, endpoint)
        bucket = self._get_token_bucket(key, capacity, refill_rate)

        self._refill_tokens(bucket)

        allowed = bucket['tokens'] >= 1.0

        if allowed:
            bucket['tokens'] -= 1.0

        remaining = int(bucket['tokens'])

        if bucket['tokens'] < bucket['capacity']:
            tokens_needed = bucket['capacity'] - bucket['tokens']
            reset = int(tokens_needed / bucket['refill_rate']) + 1
        else:
            reset = 0

        return allowed, remaining, max(1, reset)

rate_limiter = RateLimiter()
