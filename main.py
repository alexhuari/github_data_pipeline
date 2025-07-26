import argparse
from src.database.db_manager import DatabaseManager
from src.etl.extract import GitHubExtractor
from src.etl.transform import GitHubTransformer
from src.analysis.reports import GitHubReporter
from src.utils.logger import get_logger
from src.config import settings

logger = get_logger(__name__)

def run_etl_pipeline():
    """Ejecuta todo el pipeline ETL"""
    db_manager = DatabaseManager()
    try:
        # Extract
        logger.info("Iniciando extracción de datos...")
        extractor = GitHubExtractor()
        topics = settings.TOPICS.split(',')
        raw_data = extractor.get_repos_by_topics(topics, settings.MAX_REPOS)
        
        # Transform
        logger.info("Transformando datos...")
        transformer = GitHubTransformer()
        transformed_data = transformer.transform(raw_data)
        
        # Load
        logger.info("Cargando datos a PostgreSQL...")
        db_manager.upsert_data(transformed_data, 'repositories')
        
        logger.info("Pipeline ETL completado exitosamente!")
    finally:
        db_manager.close()

def generate_reports():
    """Genera y guarda reportes"""
    db_manager = DatabaseManager()
    try:
        reporter = GitHubReporter(db_manager)
        reports = reporter.generate_trend_report()
        reporter.save_reports_to_csv(reports)
    finally:
        db_manager.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GitHub Analysis Pipeline')
    parser.add_argument('action', choices=['extract', 'transform', 'load', 'report', 'all'], 
                        help='Acción a ejecutar')
    
    args = parser.parse_args()
    
    if args.action == 'all':
        run_etl_pipeline()
        generate_reports()
    elif args.action == 'extract':
        extractor = GitHubExtractor()
        topics = settings.TOPICS.split(',')
        extractor.get_repos_by_topics(topics, settings.MAX_REPOS)
    elif args.action == 'transform':
        transformer = GitHubTransformer()
        # Aquí deberías cargar los datos extraídos
    elif args.action == 'load':
        db_manager = DatabaseManager()
        # Aquí deberías cargar los datos transformados
    elif args.action == 'report':
        generate_reports()


