

def makeup_columns(arguments: dict, columns: str = '') -> str:
    """
    Создание макета столбцов для таблиц базы данных

    :param arguments: Словарь аргументов столбцов таблицы. Ключи - названия столбцов, значения - их типы.
    :param columns: Уже существующие колонки
    :return: отформатированные столбцы в типе данных str
    """
    columns += ", ".join(
       ["{column_name} {column_type}".format
        (column_name=column_name, column_type=column_type)
        for column_name, column_type in arguments.items()])

    return columns


class SQLite:


    def __init__(self):

        self.query = ""


    def __str__(self):

        return self.query


    def create(self, name_table: str, append_columns: dict, id_primary_key: bool = False):
        """
        Создает SQL-запрос для создания таблицы, если она не существует, и возвращает его.

        :param name_table: Название создаваемой таблицы.
        :param append_columns: Словарь столбцов таблицы. Ключи - названия столбцов, значения - их типы.
        :param id_primary_key: Добавить ли в начале таблицы уникальный id, для идентификации каждой записи. По умолчанию False - не добавлять, True - добавить
        :return: Экземпляр класса SQLRequests.
        """
        columns = ''

        if id_primary_key:

            columns = 'id INTEGER PRIMARY KEY AUTOINCREMENT, '

        columns = makeup_columns(
            append_columns,
            columns)

        # Создание SQL-запроса
        self.query = ("CREATE TABLE IF NOT EXISTS {name_table} "
                      "({columns})".format
                      (name_table=name_table, columns=columns))

        return self


    def alter(self, name_table: str, add_column: dict):
        """
        Создает SQL-запрос для изменения таблицы. Добавляет новые колонки.

        :param name_table: Название таблицы.
        :param add_column: Словарь должен содержать элементы одного нового столбца для созданной таблицы. Ключи - название столбца, значения - их типы.
        :return: Экземпляр класса SQLRequests.
        """
        column = makeup_columns(
            add_column)

        # Создание SQL-запроса
        self.query = ("ALTER TABLE {name_table} "
                      "ADD {column}".format
                      (name_table=name_table, column=column))

        return self


    def drop(self, name_table: str):
        """
        Создает SQL-запрос для удаления существующей таблицы.

        :param name_table: Название таблицы, которую нужно удалить.
        :return: Экземпляр класса SQLRequests.
        """
        # Создание SQL-запроса
        self.query = ("DROP TABLE IF EXISTS {name_table}".format
                      (name_table=name_table))

        return self


    def insert(self, name_table: str, names_columns: list):
        """
        Создает INSERT запрос. Для заполнения уже созданной таблицы новыми данными.

        :param name_table: Название таблицы.
        :param names_columns: Названия колонок таблиц.
        :return: Экземпляр класса SQLRequests.
        """
        # Выписывание названий колонок
        names_columns = ", ".join(names_columns)

        # Подсчет колонок, с которыми будут взаимодействовать
        count_columns : int = len(names_columns) + 1

        values_columns = []

        for _ in 0, count_columns:
            values_columns.append('?')

        # Переход списка знаков "?" в формат str
        values_columns = ', '.join(values_columns)

        # Создание SQL-запроса
        self.query = ("INSERT INTO {name_table} ({name_columns}) VALUES ({value_colomns})".format
                      (name_table=name_table, name_columns=names_columns, value_colomns=values_columns))

        return self


    def select(self, name_table: str, names_columns = '*'):
        """
        Создает базовый SELECT запрос. Для выборки данных из таблицы.

        :param name_table: Название таблицы.
        :param names_columns: Список названий столбцов для выборки или строка "*", означающая вывод всех столбцов.
        :return: Экземпляр класса SQLRequests.
        """
        names_columns = ", ".join(names_columns)

        # Создание SQL-запроса
        self.query = ("SELECT {columns} "
                      "FROM {name_table}".format
                      (columns=names_columns,
                       name_table=name_table))

        return self


    def where(self, conditions: dict):
        """
        Добавляет WHERE условия в запрос. Для поиска записей.

        :param conditions: Строка или словарь условий.
        :return: Экземпляр класса SQLRequests.
        """
        cond = " AND ".join("{key} = {value}".format(key=key, value=value) if isinstance(value, (int, bool))
            else "{key} = '{value}'".format(key=key, value=value)
            for key, value in conditions.items()
        )

        self.query += (" WHERE {cond}".format
                       (cond=cond))

        return self


    def limit(self, count: int):
        """
        Добавляет LIMIT в запрос.

        :param count: Количество строк для ограничения выборки.
        :return: Экземпляр класса SQLRequests.
        """
        self.query += (" LIMIT {count}".format
                       (count=count))

        return self


    def order_by(self, columns: list, order: str = "ASC"):
        """
        Добавляет ORDER BY в запрос.

        :param columns: Список колонок для сортировки.
        :param order: Порядок сортировки, "ASC" или "DESC".
        :return: Экземпляр класса SQLRequests.
        """
        columns = ", ".join(columns)

        self.query += (" ORDER BY {columns} {order}".format
                       (columns=columns, order=order))

        return self


    def update(self, name_table: str, data_set: dict, conditions: dict = None):
        """
        Создает UPDATE запрос. Для обновления данных конкретной записи или записей.

        :param name_table: Название таблицы.
        :param data_set: Словарь данных для обновления.
        :param conditions: Условия для обновления.
        :return: Экземпляр класса SQLRequests.
        """
        updates = ", ".join("{key} = '{value}'".format(key=key, value=value)
                            for key, value in data_set.items())

        self.query = ("UPDATE {name_table} SET {updates}".format
                      (name_table=name_table, updates=updates))

        if conditions:

            self.where(conditions)

        return self


    def delete(self, name_table: str, conditions: dict = None):
        """
        Создает DELETE запрос. Удаление записи из таблицы

        :param name_table: Название таблицы.
        :param conditions: Условия для удаления.
        :return: Экземпляр класса SQLRequests.
        """
        self.query = ("DELETE FROM {name_table}".format
                      (name_table=name_table))

        if conditions:

            self.where(conditions)

        return self


    def reset(self):
        """
        Сбрасывает текущий запрос.
        """
        self.query = ""

        return self


    def build(self):
        """
        Возвращает финальный SQL запрос.

        :return: Строка SQL-запроса.
        """
        query = self.query

        self.reset()

        return query


