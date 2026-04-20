from src.extract import extract_all
from src.transform import transform_all
from src.load import load_all
from src.utils import setup_logger


def main():
    logger = setup_logger()

    try:
        logger.info("Iniciando extração dos arquivos CSV...")
        raw_data = extract_all()
        logger.info("Extração concluída.")

        logger.info("Iniciando transformações da camada Silver...")
        transformed_data = transform_all(raw_data)
        logger.info("Transformações concluídas.")

        logger.info("Iniciando carga no PostgreSQL...")
        load_all(transformed_data)
        logger.info("Carga concluída com sucesso.")

    except Exception as e:
        logger.exception(f"Erro durante execução do pipeline: {e}")
        raise


if __name__ == "__main__":
    main()