## Запуск
Версия python - 3.4.0

Перед запуском нужно создать базу "test_db"

Запустить create_db.py для создания таблиц

Запустить celery

Запускаем runserver.py

## Техническое задание:
Реализовать трекинг заявок для любой ТК на выбор: 

Деловые Линии,
ПЭК

#### Use case:
1) На веб-странице находится поле для ввода номера отслеживания и кнопка «Найти».
Пользователь вводит номер и нажимает кнопку «Найти».

2) Backend по возможности определяет, какой ТК принадлежит номер, после чего отправляет асинхронный запрос к API соответствующей ТК.

3) Если опознать номер не удалось, то пользователь должен самостоятельно выбрать ТК, после чего запускается поиск.
Пользователь видит форму поиска + индикатор загрузки.

4) Frontend периодически опрашивает сервер в ожидании результатов поиска.
После окончания поиска отображается найденный результат или сообщение об отсутствии данных. 

5) Результаты поиска сохраняются в кеш на время, определенное для каждой ТК отдельно. Например, для X результаты кешируются на 3 часа, а для Y на 5 минут.
Если результат поиска есть в кеше, то показывать результат сразу без запуска задач.

6) Также сохранять запускаемые пользователями поиски в базу данных.

Реализация должна подразумеваеть поддержку множества ТК в будущем. Добавление новой ТК должно сводиться к написанию обертки для API ТК.

Необходимо использовать технологии из следующего набора: 
Flask,
SQLAlchemy,
PostgreSQL,
Celery,
Redis
