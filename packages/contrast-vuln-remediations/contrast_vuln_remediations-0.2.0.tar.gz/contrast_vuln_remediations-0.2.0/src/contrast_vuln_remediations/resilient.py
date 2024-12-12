"""
Enhanced error handling and retry logic for API requests.
"""

import asyncio
from typing import TypeVar, Callable, Optional, Any
import logging
from functools import wraps
from datetime import datetime

import httpx

logger = logging.getLogger(__name__)

T = TypeVar('T')

class RetryConfig:
    """Configuration for retry behavior"""
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        jitter: float = 0.1,
        retry_codes: "set[int]" = {408, 429, 500, 502, 503, 504}
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
        self.retry_codes = retry_codes

class APIRateLimiter:
    """Rate limiter for API requests"""
    def __init__(self, requests_per_second: float = 10.0):
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time: Optional[datetime] = None
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire permission to make a request, waiting if necessary"""
        async with self._lock:
            if self.last_request_time is not None:
                elapsed = datetime.now() - self.last_request_time
                sleep_time = max(0, self.min_interval - elapsed.total_seconds())
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
            self.last_request_time = datetime.now()

def with_retry(config: Optional[RetryConfig] = None):
    """Decorator for adding retry logic to async functions"""
    if config is None:
        config = RetryConfig()

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            
            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except httpx.HTTPError as e:
                    response = getattr(e, "response", None)
                    status_code = response.status_code if response is not None else None
                    
                    if attempt == config.max_retries or (
                        status_code and status_code not in config.retry_codes
                    ):
                        raise
                    
                    delay = min(
                        config.base_delay * (2 ** attempt) + 
                        config.jitter * (2 * asyncio.get_event_loop().time() - 1),
                        config.max_delay
                    )
                    
                    logger.warning(
                        f"Request failed with status {status_code}. "
                        f"Retrying in {delay:.2f}s (attempt {attempt + 1}/{config.max_retries})"
                    )
                    
                    await asyncio.sleep(delay)
                    last_exception = e
                except Exception as e:
                    if attempt == config.max_retries:
                        raise
                    logger.warning(
                        f"Unexpected error: {str(e)}. "
                        f"Retrying (attempt {attempt + 1}/{config.max_retries})"
                    )
                    await asyncio.sleep(config.base_delay * (2 ** attempt))
                    last_exception = e
            
            if last_exception:
                raise last_exception
            return None

        return wrapper
    return decorator

class TimeoutConfig:
    """Configuration for request timeouts"""
    def __init__(self, 
                 connect_timeout: float = 10.0,
                 read_timeout: float = 30.0,
                 write_timeout: float = 10.0,
                 pool_timeout: float = 10.0):
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout 
        self.write_timeout = write_timeout
        self.pool_timeout = pool_timeout

class EnhancedAsyncClient(httpx.AsyncClient):
    """Enhanced HTTP client with retry logic and rate limiting"""
    def __init__(self, 
                 timeout_config: Optional[TimeoutConfig] = None,
                 rate_limiter: Optional[APIRateLimiter] = None,
                 *args: Any, 
                 **kwargs: Any):
        if timeout_config is None:
            timeout_config = TimeoutConfig()
        
        timeout = httpx.Timeout(
            connect=timeout_config.connect_timeout,
            read=timeout_config.read_timeout,
            write=timeout_config.write_timeout,
            pool=timeout_config.pool_timeout
        )
        
        super().__init__(*args, timeout=timeout, **kwargs)
        self.rate_limiter = rate_limiter or APIRateLimiter()

    @with_retry()
    async def get(self, *args: Any, **kwargs: Any) -> httpx.Response:
        """Enhanced GET request with retry logic and rate limiting"""
        await self.rate_limiter.acquire()
        return await super().get(*args, **kwargs)

    @with_retry()
    async def post(self, *args: Any, **kwargs: Any) -> httpx.Response:
        """Enhanced POST request with retry logic and rate limiting"""
        await self.rate_limiter.acquire()
        return await super().post(*args, **kwargs)

    @with_retry()
    async def put(self, *args: Any, **kwargs: Any) -> httpx.Response:
        """Enhanced PUT request with retry logic and rate limiting"""
        await self.rate_limiter.acquire()
        return await super().put(*args, **kwargs)

    @with_retry()
    async def delete(self, *args: Any, **kwargs: Any) -> httpx.Response:
        """Enhanced DELETE request with retry logic and rate limiting"""
        await self.rate_limiter.acquire()
        return await super().delete(*args, **kwargs)