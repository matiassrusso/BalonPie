from cache import TTLCache, NoDataAvailableError


def test_first_call_fetches_and_returns_fresh_value():
    calls = []

    def fetch_fn():
        calls.append(1)
        return "valor-fresco"

    cache = TTLCache(now_fn=lambda: 1000.0)
    entry = cache.get_or_refresh("clave", ttl_seconds=60, fetch_fn=fetch_fn)

    assert entry.value == "valor-fresco"
    assert entry.fetched_at == 1000.0
    assert entry.is_stale is False
    assert len(calls) == 1


def test_second_call_within_ttl_does_not_refetch():
    calls = []
    now = {"t": 1000.0}

    def fetch_fn():
        calls.append(1)
        return "valor"

    cache = TTLCache(now_fn=lambda: now["t"])
    cache.get_or_refresh("clave", ttl_seconds=60, fetch_fn=fetch_fn)

    now["t"] = 1030.0
    entry = cache.get_or_refresh("clave", ttl_seconds=60, fetch_fn=fetch_fn)

    assert entry.value == "valor"
    assert len(calls) == 1


def test_call_after_ttl_expires_refetches():
    calls = []
    now = {"t": 1000.0}

    def fetch_fn():
        calls.append(1)
        return f"valor-{len(calls)}"

    cache = TTLCache(now_fn=lambda: now["t"])
    primero = cache.get_or_refresh("clave", ttl_seconds=60, fetch_fn=fetch_fn)

    now["t"] = 1061.0
    segundo = cache.get_or_refresh("clave", ttl_seconds=60, fetch_fn=fetch_fn)

    assert primero.value == "valor-1"
    assert segundo.value == "valor-2"
    assert segundo.fetched_at == 1061.0
    assert len(calls) == 2


def test_refresh_failure_after_ttl_returns_stale_value():
    now = {"t": 1000.0}
    should_fail = {"v": False}

    def fetch_fn():
        if should_fail["v"]:
            raise RuntimeError("API-Football no responde")
        return "valor-original"

    cache = TTLCache(now_fn=lambda: now["t"])
    cache.get_or_refresh("clave", ttl_seconds=60, fetch_fn=fetch_fn)

    now["t"] = 1100.0
    should_fail["v"] = True
    entry = cache.get_or_refresh("clave", ttl_seconds=60, fetch_fn=fetch_fn)

    assert entry.value == "valor-original"
    assert entry.fetched_at == 1000.0
    assert entry.is_stale is True


def test_refresh_failure_with_no_previous_value_raises():
    def fetch_fn():
        raise RuntimeError("API-Football no responde")

    cache = TTLCache(now_fn=lambda: 1000.0)

    try:
        cache.get_or_refresh("clave-nueva", ttl_seconds=60, fetch_fn=fetch_fn)
        assert False, "esperaba NoDataAvailableError"
    except NoDataAvailableError:
        pass
