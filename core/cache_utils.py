from django.core.cache import cache
import hashlib

def make_cache_key(path, user_id="anon", prefix="page"):
    base = f"{prefix}:{path}:{user_id}"
    return hashlib.md5(base.encode("utf-8")).hexdigest()

def set_cache(path, user_id, data, prefix="page", timeout=300):
    key = make_cache_key(path, user_id, prefix)
    cache.set(key, data, timeout)
    return key

def get_cache(path, user_id, prefix="page"):
    key = make_cache_key(path, user_id, prefix)
    return cache.get(key)

def clear_cache(prefix=None, pattern=None):
    if prefix and pattern:
        search = f"{prefix}:{pattern}"
    elif prefix:
        search = f"{prefix}:*"
    else:
        search = "*"

    try:
        keys = cache.keys(search)
        if keys:
            cache.delete_many(keys)
            print(f"🧹 Очистка кеша: {len(keys)} ключей ({search})")
        else:
            print(f"🧹 Кеш {search} уже пуст")
    except Exception as e:
        print(f"⚠️ Ошибка очистки кеша: {e}")
