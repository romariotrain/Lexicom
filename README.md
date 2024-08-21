Первый вариант решения:

# Сравнивает имя файла из таблицы full_names с именем из таблицы short_names.
# Использует регулярное выражение для поиска совпадений.

# Если имя файла в full_names начинается с имени из short_names
# и за ним следует точка и любое расширение, тогда статус обновляется.

UPDATE full_names fn
SET status = sn.status
FROM short_names sn
WHERE fn.name ~ ('^' || sn.name || '\.[a-zA-Z0-9]+$');

Второй вариант:

# Сравнивает имя файла из таблицы full_names с именем из таблицы short_names.
# Использует оператор LIKE для поиска совпадений.

UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE full_names.name LIKE short_names.name || '%';

# Если имя файла в full_names начинается с имени из short_names,
# независимо от расширения, статус обновляется.