import json
from flask import render_template, request
from runserver import app
from tk import TK_dict


@app.route('/')
def main():
    """
    Главная страница
    """
    template = 'main.html'
    tk_list = []
    for key, value in TK_dict.items():
        tk_list.append({
            'id': key,
            'name': value.name,
        })
    context = {
        'tk_list': tk_list,
    }
    return render_template(template, **context)


@app.route('/search/')
def search():
    """
    Поиск по трэк номеру
    """
    track_id = request.values.get('track_id')
    tk_id = request.values.get('tk_id')

    result = app.manager.search_for_track_id(track_id, tk_id)
    return json.dumps(result)


@app.route('/check/')
def check():
    """
    Проверка результа по трэк номеру
    """
    track_id = request.values.get('track_id')
    tk_id = request.values.get('tk_id')

    if not tk_id:
        tk_id = app.manager.identify_tk(track_id)

    result = app.manager.get_result_for_track_id(tk_id, track_id)
    if result:
        return json.dumps(result)
    else:
        return json.dumps({})


@app.route('/result_celery/', methods=['POST'])
def result_celery():
    """
    Результат запроса к ТК, вызывается из селери
    """
    task_id = request.values.get('task_id')
    message = request.values.get('message')
    app.manager.post_search_for_track_id(task_id, message)