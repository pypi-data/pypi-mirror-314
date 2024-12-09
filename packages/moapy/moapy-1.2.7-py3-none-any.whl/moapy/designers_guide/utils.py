from functools import wraps
from diskcache import Cache

CACHE_DIR = ".cache"

cache = Cache(CACHE_DIR)


def cache_result(func):
    @wraps(func)
    def wrapper(latex_str: str):
        result = cache.get(latex_str)
        if result is not None:
            return result
        result = func(latex_str)
        try:
            cache.set(latex_str, result)
        except:
            # TODO: 캐시저장 실패시 로그처리
            pass
        return result

    return wrapper
