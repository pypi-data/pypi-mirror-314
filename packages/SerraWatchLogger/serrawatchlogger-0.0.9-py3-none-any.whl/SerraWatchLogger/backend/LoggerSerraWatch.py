import logging
import os
from datetime import datetime


class LoggerSerraWatch:
    _instance = None
    logger: logging.Logger
    def __new__(self, name: str = __name__):
        # Vérifie si une instance existe déjà
        if LoggerSerraWatch._instance is not None:
            return

        LoggerSerraWatch._instance = self

        # Initialisation du logge
        self.logger = logging.getLogger(name)

        # Création du répertoire de base pour les logs
        base_log_directory = "logs"
        if not os.path.exists(base_log_directory):
            os.makedirs(base_log_directory)

        # Création d'un sous-dossier pour les logs avec la date et l'heure actuelles
        log_directory = os.path.join(base_log_directory, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # Configuration des handlers pour le logger
        log_filename = os.path.join(log_directory, "application.log")
        file_handler = logging.FileHandler(log_filename)
        stream_handler = logging.StreamHandler()

        # Configuration des formats pour les logs
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # Stockage du répertoire pour les logs spécifiques à un topic
        self.log_directory = log_directory

        # Ajout des handlers au logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.DEBUG)

    @staticmethod
    def get_instance(name: str = __name__):
        if LoggerSerraWatch._instance is None:
            LoggerSerraWatch(name)
        return LoggerSerraWatch._instance

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

    def add_topic_log(self, topic: str, message: str):
        safe_topic_name = topic.replace("/", "_")
        topic_log_filename = os.path.join(self.log_directory, f"{safe_topic_name}.log")
        with open(topic_log_filename, "a") as topic_log_file:
            topic_log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    def update_log_file(self, new_log_path):
        """Met à jour dynamiquement le fichier dans lequel le logger écrit."""
        for handler in self.logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                self.logger.removeHandler(handler)
                handler.close()

        # Ajoute un nouveau gestionnaire pour le nouveau fichier
        file_handler = logging.FileHandler(new_log_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)