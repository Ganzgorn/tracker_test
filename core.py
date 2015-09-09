from cache import set_keys_for_search_track_id, get_keys_for_search_track_id, set_result_for_search_track_id, \
    get_result_for_search_track_id
from tasks import req_search_for_track_id
from tk import TK_dict


class Manager(object):

    def __init__(self):
        self.tk_dict = TK_dict

    def search_for_track_id(self, track_id, tk_id=None):
        """
        Если удалось определить ТК по трэк номеру и в кеше результата ещё нет, запускает таск с запросом к ТК
        """
        if not tk_id:
            tk_id = self.identify_tk(track_id)
            if not tk_id:
                return {'choose_tk': True}

        result = self.get_result_for_track_id(tk_id, track_id)
        if result:
            return result

        tk_item = self.tk_dict[tk_id]
        req_data = tk_item.get_search_track_data(track_id)

        result = req_search_for_track_id.delay(
            req_data.get('url'),
            req_data.get('data'),
            req_data.get('header'),
            req_data.get('auth')
        )

        set_keys_for_search_track_id(result.id, tk_id, track_id)
        return {}

    def post_search_for_track_id(self, task_id, message):
        """
        Получает результат запроса к ТК сохраняет в кеш и в базу
        """
        track_key = get_keys_for_search_track_id(task_id)

        tk_id, track_id = track_key.split(':')
        tk_item = self.tk_dict[tk_id]

        set_result_for_search_track_id(track_key, message, tk_item.cache_timeout)

        # save into DB
        from models import UserRequests
        user_req = UserRequests()
        user_req.track_id = track_id
        user_req.tk_id = tk_id
        user_req.message = message
        user_req.save()

    def get_result_for_track_id(self, tk_id, track_id):
        """
        Получает из кеша и десериализует сообщение
        """
        message = get_result_for_search_track_id(tk_id, track_id)
        if message:
            result = self.tk_dict[tk_id].deserialization(message)
            return result

    def identify_tk(self, track_id):
        """
        Определяет ТК по трэк номеру
        """
        for tk_id, tk in self.tk_dict.items():
            if tk.check_track_id(track_id):
                return tk_id