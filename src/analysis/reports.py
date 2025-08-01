import pandas as pd
from typing import Dict, Any
from src.database.db_manager import DatabaseManager
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GitHubReporter:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def generate_trend_report(self) -> Dict[str, pd.DataFrame]:
        """Generated  reports about the trends in github repositories focus on AI"""
        reports = {}
        
        # 1. Most popular languages
        reports['top_languages'] = self.db.execute_query("""
            SELECT language, COUNT(*) as repo_count, 
                   AVG(stars_per_day) as avg_growth
            FROM repositories
            GROUP BY language
            HAVING COUNT(*) >= 5
            ORDER BY avg_growth DESC
            LIMIT 10
        """)
        
        # 2. Categories with much growth
        reports['ai_categories'] = self.db.execute_query("""
            SELECT ai_category, COUNT(*) as repo_count,
                   AVG(stars_per_day) as avg_growth,
                   AVG(forks_per_star) as adoption_rate
            FROM repositories
            GROUP BY ai_category
            ORDER BY avg_growth DESC
        """)
        
        # 3. More active repositories 
        reports['most_active'] = self.db.get_most_active_repos(days=30, limit=10)
        
        logger.info("All reports were generated correctly")
        return reports
    
    def save_reports_to_csv(self, reports: Dict[str, pd.DataFrame], output_dir: str = "reports"):
        """Saved reposts in CSV documents"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for name, df in reports.items():
            file_path = f"{output_dir}/{name}.csv"
            df.to_csv(file_path, index=False)
            logger.info(f"Reporte guardado: {file_path}")