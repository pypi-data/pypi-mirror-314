import logging
import os
from typing import Any

_logger = logging.getLogger(__name__)

enable_api_caching = os.environ.get("ENABLE_API_CACHE", "false").lower() == "true"

try:
    import cachetools
    from shelved_cache import PersistentCache, cachedasyncmethod

    _pc = PersistentCache(
        filename="/tmp/qcanvas_cache",
        wrapped_cache_cls=cachetools.LRUCache,
        maxsize=10000,
    )
except ModuleNotFoundError:
    _logger.warning(
        "API caching is enabled but shelved cache and/or cachetools are not installed"
    )
    enable_api_caching = False


def cachedasyncmethod_for_development(autotuple: bool = False, **kwargs) -> Any:
    if enable_api_caching and autotuple:
        from shelved_cache.keys import autotuple_hashkey

        kwargs["key"] = autotuple_hashkey

    def decorate(fn) -> Any:
        return (
            (cachedasyncmethod(lambda x: _pc, **kwargs))(fn)
            if enable_api_caching
            else fn
        )

    return decorate
