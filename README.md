# SQL Запросы для Обновления Статусов Файлов


## Вариант 1: Использование Регулярных Выражений

Этот запрос сравнивает имя файла из таблицы `full_names` с именем из таблицы `short_names` и использует регулярное выражение для поиска совпадений. Он обновляет статус в `full_names`, если имя файла начинается с имени из `short_names` и за ним следует точка и любое расширение.

```sql
UPDATE full_names fn
SET status = sn.status
FROM short_names sn
WHERE fn.name ~ ('^' || sn.name || '\.[a-zA-Z0-9]+$');
```
## Вариант 2: Использование Оператора `LIKE`

Этот запрос использует оператор `LIKE` для поиска совпадений. Он обновляет статус в `full_names`, если имя файла начинается с имени из `short_names`, независимо от расширения.

```sql
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE full_names.name LIKE short_names.name || '%';
