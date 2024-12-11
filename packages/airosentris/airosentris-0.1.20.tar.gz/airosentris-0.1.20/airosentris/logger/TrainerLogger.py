import json
from datetime import datetime
from threading import Lock, Thread
import time
from airosentris.client.RabbitMQClient import RabbitMQClient
from airosentris.config.ConfigFetcher import get_config
from airosentris.logger.Logger import Logger


class TrainerLogger:
    """
    Logger khusus untuk mencatat aktivitas pelatihan model ke RabbitMQ.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Ensure only one instance of TrainerLogger is created.
        """
        if not cls._instance:
            with cls._lock:  # Thread-safe initialization
                if not cls._instance:  # Double-checked locking
                    cls._instance = super(TrainerLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, config=None):
        """
        Ensures initialization happens only once.
        """
        if not hasattr(self, "initialized"):
            config = get_config()
            self.rabbitmq_client = RabbitMQClient(config=config)
            self.rabbitmq_client.connect()
            self.exchange_name = "airosentris.status"
            self.initialized = True
        self.current_status = None
        self.logger = Logger(__name__)
        self.logger.info("TrainerLogger initialized successfully.")

    def _prepare_log_message(self, project_id: str, run_id: str, log_type: str, data: dict | str) -> str:
        """
        Membuat pesan log dalam format JSON.

        Args:
            project_id (str): ID proyek.
            run_id (str): ID pelatihan atau proses.
            log_type (str): Jenis log (command, metric, atau status).
            data (dict | str): Data log.

        Returns:
            str: Pesan log dalam format JSON.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return json.dumps({
            "project_id": project_id,
            "run_id": run_id,
            "type": log_type,
            "time": current_time,
            "data": data if isinstance(data, str) else json.dumps(data)
        })

    def log_command(self, project_id: str, run_id: str, command: str) -> None:
        """
        Mencatat perintah pelatihan.

        Args:
            project_id (str): ID proyek.
            run_id (str): ID pelatihan atau proses.
            command (str): Perintah yang dijalankan.
        """
        message = self._prepare_log_message(project_id, run_id, "command", command)
        self.rabbitmq_client.publish_message(self.exchange_name, "", message)
        self.logger.info(f"Command log sent: {message}")

    def log_metric(self, project_id: str, run_id: str, metrics: dict) -> None:
        """
        Mencatat metrik hasil pelatihan.

        Args:
            project_id (str): ID proyek.
            run_id (str): ID pelatihan atau proses.
            metrics (dict): Data metrik pelatihan.
        """
        message = self._prepare_log_message(project_id, run_id, "metric", metrics)
        self.rabbitmq_client.publish_message(self.exchange_name, "", message)
        self.logger.info(f"Metric log sent: {message}")

    def log_status(self, project_id: str, run_id: str, status: str) -> None:
        """
        Mencatat status pelatihan.

        Args:
            project_id (str): ID proyek.
            run_id (str): ID pelatihan atau proses.
            status (str): Status pelatihan.
        """
        # Membuat koneksi dan saluran RabbitMQ untuk setiap thread
        def status_logging():
            # Membuat client RabbitMQ baru untuk setiap thread
            thread_rmq_client = RabbitMQClient(config=get_config())
            thread_rmq_client.connect()
            
            # Menyimpan status dan mengirim log secara terus-menerus
            while self.current_status == status:
                message = self._prepare_log_message(project_id, run_id, "status", self.current_status)
                thread_rmq_client.publish_message(self.exchange_name, "", message)
                self.logger.info(f"Status log sent from thread: {message}")
                if self.current_status == "End":
                    break
                time.sleep(1)
                
            thread_rmq_client.close()  # Tutup koneksi ketika selesai

        # Start the thread
        status_thread = Thread(target=status_logging)
        status_thread.daemon = True  # Thread berhenti ketika program utama berhenti
        status_thread.start()

        # Perbarui status utama
        with self._lock:
            self.current_status = status
