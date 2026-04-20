import logging
import os
import re


def setup_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("etl")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler = logging.FileHandler("logs/etl.log", encoding="utf-8")
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger


def to_snake_case(column_name: str) -> str:
    column_name = column_name.strip().lower()
    column_name = re.sub(r"[^\w\s]", "", column_name)
    column_name = re.sub(r"\s+", "_", column_name)
    return column_name