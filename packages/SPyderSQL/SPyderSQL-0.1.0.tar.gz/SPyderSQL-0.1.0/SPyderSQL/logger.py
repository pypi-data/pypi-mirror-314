import logging


class Logger:
    """
    Класс для настройки и использования логирования в проекте.
    """
    def __init__(self, name: str, level: int = logging.INFO):
        """
        Инициализация логгера.

        :param name: Имя логгера (обычно __name__ модуля).
        :param level: Уровень логирования (по умолчанию INFO).
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Создаём консольный обработчик
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Формат сообщений
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру (если не добавлен ранее)
        if not self.logger.handlers:

            self.logger.addHandler(console_handler)


    def get_logger(self):
        """
        Возвращает настроенный логгер.
        """
        return self.logger