from .SQLite import pragma_table, create_table, alter_table, drop_table, insert_table, update_table, select_table
from .SQLite import TypesSQLite
from .logger import Logger

__version__ = "0.1.0"
__author__ = "Emil Artemev"
__email__ = "jordanman1300@gmail.com"


logger = Logger(__name__).get_logger()


# logger.info("Информационное сообщение")
# logger.warning("Предупреждение")
# logger.error("Ошибка")
