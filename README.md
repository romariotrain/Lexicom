# SQL Запросы для Обновления Статусов Файлов

Когда я тестировал на полях name обеих таблиц были b-tree индексы

## Вариант 1: Использование Регулярных Выражений

Этот запрос обновляет статус в full_names, используя функцию substring для извлечения части имени файла до точки и сравнивая её с именем из таблицы short_names.

```sql
UPDATE full_names fn
SET status = sn.status
FROM short_names sn
WHERE sn.name = substring(fn.name FROM 1 FOR position('.' IN fn.name) - 1);
```
## Вариант 2: Использование Оператора `LIKE`

Этот запрос использует CTE для создания промежуточной таблицы name_mappings, где сопоставляются имена из full_names и short_names. Затем происходит обновление статусов в full_names на основе этих сопоставлений.

```sql
WITH name_mappings AS (
    SELECT fn.name, sn.status
    FROM full_names fn
    JOIN short_names sn
    ON sn.name = split_part(fn.name, '.', 1)
)
UPDATE full_names fn
SET status = nm.status
FROM name_mappings nm
WHERE fn.name = nm.name;
```

## Были варианты с регулярными выражениями или like, но работало слишком медленно
