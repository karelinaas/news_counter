# Скрипт для отслеживания обновлений сайта

ТЗ: необходимо написать консольный скрипт, который будет получать количество новых новостей с html-страницы по URL раз в n минут, сохранять в БД это количество и заголовок последней новости.

## Детали
- URL могут быть разные
- к URL необходимо обращаться через прокси, прокси нужно менять раз в час
- структура html страницы такова: есть `div` с определенным id (id может быть разным), внтури него коллекция элементов `div.post` (новости), внутри каждого `div.post`, кроме последнего, есть элемент `div.title`
- новые `div.post` появляются сверху при появлении на сайте новой новости
- заголовки новостей в `div.title` всегда разные

## Работа скрипта

Перед первым запуском необходимо создать БД (SQLite) и таблицы:

```python migrate.py```

Структура БД:

```
+-----------------------------------+
|updates                            |
+-----+-------+---------------------+
|date |text   |дата и время проверки|
+-----+-------+---------------------+
|delta|integer|кол-во новых новостей|
+-----+-------+---------------------+
```
```
+-----------------------------------+
|last_titles                        |
+-----+-------+---------------------+
|date |text   |дата и время проверки|
+-----+-------+---------------------+
|title|integer|последний заголовок  |
+-----+-------+---------------------+
```
```
+--------------------+
|proxies             |
+-----+----+---------+
|proxy|text|IP прокси|
+-----+----+---------+
```

Нужно добавить работающие прокси в таблицу `proxies`.

Запуск скрипта:

```python scrap_it.py [url] [div_id] [minutes]```

Все параметры обязательны:

- `[url]` - URL страницы с новостями
- `[div_id]` - id родительского div на странице
- `[minutes]` - число, раз в сколько минут повторять проверку

Результатом работы скрипта будут записи в таблицах `updates` и `last_titles`.
