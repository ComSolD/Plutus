from parser.NBA.parser import ParsingNBA
from parser.NHL.parser import ParsingNHL
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename=".log",  # Логи будут записываться в файл
    encoding="utf-8",
)

if __name__ == "__main__":
    logging.info("Программа запускается")

    ParsingNHL('2025-01-16','2025-01-16').date_cycle()
    
    logging.info("Программа завершила работу")