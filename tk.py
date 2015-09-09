import json
import re


class TK(object):
    id = NotImplemented

    def __init__(self):
        self.track_pattern = NotImplemented

    def get_search_track_data(self, track_id):
        """
        Возвращает данные необходимые для запроса к ТК
        """
        raise NotImplementedError

    def deserialization(self, message):
        """
        Десериализация ответа от ТК
        """
        raise NotImplementedError

    def check_track_id(self, track_id):
        """
        По шаблону определяет принадлежит ли track_id данной ТК
        """
        result = re.match(self.track_pattern, track_id)
        if result:
            return True

        return False


class TKDellin(TK):
    """
    ТК Деловыне линии
    """
    id = 'dellin.ru'

    def __init__(self):
        super().__init__()
        self.name = 'Деловые линии'
        self.site = 'dellin.ru'
        self.key = 'CE6DF07A-509E-11E5-97D2-00505683A6D3'
        self.cache_timeout = 360
        self.track_pattern = '\d{2}-\d{11}'

    def get_search_track_data(self, track_id):
        data = {
            'appKey': self.key,
            'docId': track_id
        }

        result = {
            'url': 'https://api.dellin.ru/v1/public/tracker.json',
            'data': json.dumps(data),
            'header': {
                'Content-type': 'application/json',
                'Accept': 'text/plain'
            }
        }
        return result

    def deserialization(self, message):
        response = json.loads(message)

        if 'errors' in response:
            return {'success': False, 'message': response['errors']}

        elif 'state' in response:
            return {'success': True, 'message': response['state']}


class TKPecom(TK):
    """
    ТК ПЭК
    """
    id = 'pecom.ru'

    def __init__(self):
        super().__init__()
        self.name = 'ПЭК'
        self.site = 'pecom.ru'
        self.login = 'vlpotapov'
        self.key = 'E6FE9189181BB71A34BB0C697926709C73B1B73B'
        self.cache_timeout = 36000
        self.track_pattern = '^[А-Я0-9]{7}-./\d{4}$'

    def get_search_track_data(self, track_id):
        data = {
            'cargoCodes': [track_id]
        }

        result = {
            'url': 'https://kabinet.pecom.ru/api/v1/cargos/basicstatus/',
            'data': json.dumps(data),
            'header': {
                'Content-type': 'application/json',
                'Accept': 'text/plain'
            },
            'auth': (self.login, self.key)
        }
        return result

    def deserialization(self, message):
        response = json.loads(message)
        if isinstance(response, list) and response:
            # Так как была задача сделать только для 1 трэк кода
            return {'success': True, 'message': response[0]['info']['cargoStatus']}
        else:
            if 'error' in response:
                return {'success': False, 'message': response['error']['title']}


TK_dict = {
    TKDellin.id: TKDellin(),
    TKPecom.id: TKPecom()

}
