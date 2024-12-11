import logging
import os

class Logger:
    def __init__(self, name: str, log_file: str = 'app.log', level: int = logging.DEBUG):
        """
        Konstruktor untuk inisialisasi objek Logger.
        
        :param name: Nama logger
        :param log_file: Nama file log yang digunakan untuk mencatat log
        :param level: Level log yang digunakan (default: logging.DEBUG)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Membuat format log yang digunakan
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)

        # Membuat handler untuk mencatat log ke file
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # Membuat handler untuk mencatat log ke konsol (stdout)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Menambahkan handler ke logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Jika ukuran file log melebihi batas tertentu, rotasi file log
        log_size = 10 * 1024 * 1024  # 10MB
        if os.path.getsize(log_file) > log_size:
            self.rotate_log(log_file)

    def rotate_log(self, log_file: str):
        """
        Melakukan rotasi file log jika ukuran file melebihi batas tertentu.
        
        :param log_file: Nama file log yang akan dirotasi
        """
        # Backup file log yang lama dengan menambahkan timestamp
        backup_log_file = f"{log_file}.{self._get_timestamp()}"
        if os.path.exists(log_file):
            os.rename(log_file, backup_log_file)
            self.logger.info(f"File log lama dipindahkan ke {backup_log_file}")

    def _get_timestamp(self):
        """Menghasilkan timestamp untuk rotasi log."""
        from datetime import datetime
        return datetime.now().strftime('%Y%m%d%H%M%S')

    def debug(self, msg: str):
        """Menulis log dengan level DEBUG."""
        self.logger.debug(msg)

    def info(self, msg: str):
        """Menulis log dengan level INFO."""
        self.logger.info(msg)

    def warning(self, msg: str):
        """Menulis log dengan level WARNING."""
        self.logger.warning(msg)

    def error(self, msg: str):
        """Menulis log dengan level ERROR."""
        self.logger.error(msg)

    def critical(self, msg: str):
        """Menulis log dengan level CRITICAL."""
        self.logger.critical(msg)

# Contoh penggunaan class Logger
if __name__ == '__main__':
    log = Logger(name='MyAppLogger', log_file='app.log')

    log.debug("This is a debug message.")
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
    log.critical("This is a critical message.")
