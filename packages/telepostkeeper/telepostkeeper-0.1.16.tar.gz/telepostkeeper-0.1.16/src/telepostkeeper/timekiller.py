import subprocess
import time
import argparse
import logging

# Настройка логгера
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_subprocess(seconds):
    logger.info('🚀 Subprocess.call started')

    # Запуск main.py как отдельного процесса
    process = subprocess.Popen(['telepostkeeper'])

    # Пауза на указанное количество секунд
    time.sleep(seconds)

    logger.info('🔫 Subprocess.kill: killing the process')

    # Завершение процесса
    process.kill()

def main():
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Run and kill a subprocess after a specified time.")
    parser.add_argument("seconds", type=int, help="Time in seconds before killing the subprocess.")
    args = parser.parse_args()

    # Запуск основной функции
    run_subprocess(args.seconds)

if __name__ == "__main__":
    main()