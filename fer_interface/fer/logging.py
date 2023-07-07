import csv

from fer_interface.fer.constants import my_resources
from fer_interface.fer.util import generate_time_now_str


def _write_log_to_file(log_entry, file_path):
    """
    Scrierea un log într-un fișier.
    :param log_entry: Log-ul care trebuie scris.
    :param file_path: Fișierul în care trebuie scris log-ul.
    """
    fieldnames = ["time", "message"]
    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(log_entry)


def log_error(error_message):
    """
    Scrierea un log de eroare.
    """
    log_entry = {
        "time": generate_time_now_str(),
        "message": error_message
    }
    _write_log_to_file(log_entry, my_resources + 'data_output/logs/error_logs.csv')


def log_success(success_message):
    """
    Scrierea un log de succes.
    """
    log_entry = {
        "time": generate_time_now_str(),
        "message": success_message
    }
    _write_log_to_file(log_entry, my_resources + 'data_output/logs/success_logs.csv')
