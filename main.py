from parser.NBA.parser import ParsingNBA
from parser.NHL.parser import ParsingNHL
from parser.NFL.parser import ParsingNFL

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

    ParsingNFL('2023', [5, 3], 'past').date_cycle()
    
    logging.info("Программа завершила работу")