# test_grissli.ru
test task for vacancy python-developer in company grissli.ru

Выполнение тестового задания было начато 8.04.2016 11.30 +7 GMT.

### Задание

1. Создать Django приложение в котором можно добавлять URL’s в административном разделе (/admin/). С возможностью указать сдвиг во времени (минуты, секунды) через сколько какой URL когда будет обработан (timeshift).
  - Frontend
  - Сделать два окна textarea.
  - В первое окно выводить информацию об успехе или ошибке обработки URL’a (для backend можно воспользоваться очередями Queue).
  - Во второе вывести данные полученные из пункта 2.
2. Создать сервер для парсинга сайтов по URL’ам указанным в базе Django приложения (п. 1), в указанный сдвиг времени или сразу запускать если не указан сдвиг.
  - На сайтах получить
  - Заголовок (title)
  - Определить кодировку страницы
  - Если есть, найти и получить H1
  - Вывести данные во второе окно.

### Решение

Для организации пула потоков использовалаль очередь Queue.
Задержки по времени перед выполнением парсинга реализованы с помощью time.sleep().
Заголовок `User-Agent` использован лишь для уменьшения риска отказов при запросе страниц.
Парсинг HTML посредствам BeautifulSoup.
Для отображения данных в real-time используется django_sockets.

#### Использование WebSockets

После выполнения очередной задачи, и после удаления из базы всех результатов запускается обновление результатов на всех клиентах `socketio_api.updateClientsData()`. В ходе которого через socket отправляется сообщение содержащее обновленные данные по состоянию базы.

Клиент может запросить очистить результаты, для этого нужно отправить сообщение через WebSockets `socket.send('drop_results_request');`.

С клиента можно загрузить список URL-ов для парсинга. Мне не удалось реащизовать прием файла в Django при отправке через AJAX. Поэтому было принято решение сделать временный вариант: прочитываем файл средствами JS (на выходе просто текст), заворачиваем в JSON и отправляем через AJAX.

#### Demo

Посмотреть demo можно по адресу [http://sdlmer.tk:8080/](http://sdlmer.tk:8080/).

Не успел разобраться как подружить django_sockets с его `runserver_socketio` с uwsgi. Поэтому сервер запущен в demo режиме через `manage.py runserver_socketio`.

#### Запуск

```bash
pip install -r ./requests.txt
./manage.py runserver_socketio
```

Сервер будет запущен на localhost:8080.

#### tips and tricks

c virtualenv может возникнуть проблема "name 'PROTOCOL_SSLv3' is not defined"
решение см. здесь https://github.com/mistio/mist.io/issues/434


# Второе задание

Написать SQL запрос в базу (один запрос) который выберет данные из таблиц 1,2,3 и запишет в таблицу 4

### Решение

Запрос:
```sql
select
  p.internal_number as InternalNumber,
  CONCAT(e.name, '/', e.surname) as 'Name/Surname',
  p.position as Position,
  round(e.salary_year/12, 2) as 'Salary/Month',
  round(sum(r.taxe)/count(r.id), 2) as Tax,
  count(r.month) as Month
from
  employee e,
  position p,
  rate r
where
  p.employee_id = e.id
  and r.employee_id = e.id
group by e.id;
```

Результат
| InternalNumber | Name/Surname | Position | Salary/Month | Tax | Month |
| ---: | :--- | :--- | ---: | ---: | ---: |
|          32894 | John/Terrible    | Manager        |       916.67 | 258.50 |     2 |
|          23409 | Maggie/Woodstock | Top Manager    |      1250.00 | 325.00 |     2 |
|          23908 | Joel/Muegos      | CEO            |      1833.33 | 337.67 |     3 |
|            128 | Jeroen/van Kapf  | Board Chairman |      3666.67 | 301.00 |     2 |

[Скриншот выполнения](http://i.imgur.com/WKBGk4N.png)