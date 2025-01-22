from parser.NBA.parser import ParsingNBA
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

    ParsingNBA('2025-01-17','2025-01-17').date_cycle()
    
    logging.info("Программа завершила работу")