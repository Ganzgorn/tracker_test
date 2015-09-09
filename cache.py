import redis
from config import REDIS_HOST, REDIS_PORT

r_cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def set_keys_for_search_track_id(task_id, tk_id, track_id):
    """
    Сохранить ключ 'tk_id:track_id' по номер таска селери
    """
    key = 'keys:{0}'.format(task_id)
    value = '{0}:{1}'.format(tk_id, track_id)
    r_cache.append(key, value)


def get_keys_for_search_track_id(task_id):
    """
    Получить ключ по номеру таска селери
    """
    key = 'keys:{0}'.format(task_id)
    result = r_cache.get(key)
    r_cache.delete(key)
    if result:
        return result.decode("utf-8")


def set_result_for_search_track_id(key, message, expire):
    """
    Сохранить результат запроса к ТК
    :param key: Ключ - "tk_id:track_id" id транспортной компании + трэк номер
    :param message: Сообщение полученное от транспортной комании
    :param expire: Передается в секндуах
    :type expire: int
    """
    r_cache.append(key, message)
    r_cache.expire(key, int(expire))


def get_result_for_search_track_id(tk_id, track_id):
    """
    Получить результат запроса к ТК
    """
    key = '{0}:{1}'.format(tk_id, track_id)
    result = r_cache.get(key)
    if result:
        return result.decode("utf-8")