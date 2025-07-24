import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os 
from dotenv import load_dotenv
import logging 
from typing import Optional, List, Dict, Any

Base = declarative_base()

class DatabaseManager:
    def __init__(self):
        load_dotenv()
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        self.engine = self._create_engine()
        self.Session = sessionmaker(bind=self.engine)
        self._init_logging()

    def _create_engine(self):
        connection_string = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
        return create_engine(connection_string, pool_pre_ping=True)
    
    def _init_logging(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
    
    def upset_data(self, df: pd.DataFrame, table_name: str) -> bool:
        """Realize an UPSERT """
        try:
            with self.engine.begin() as connection:
                # Create a temporary table
                df.to_sql(f'temp_{table_name}',
                          connection,
                          if_exists='replace',
                          index=False)
                
                # Build a query qith a UPSERT dynamic 
                columns = list(df.columns)
                update_set = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns])

                upsert_query = f""" INSERT INTO {table_name} ({", ".join(columns)})
                SELECT {", ".join(columns)} FROM temp_{table_name}
                ON CONFLICT (github_id) DO UPDATE SET
                {update_set},
                last_updated = CURRENT_TIMESTAMP;
                DROP TABLE temp{table_name};
                """
                connection.execute(text(upsert_query))
            self.logger.info(f"Data was updated {table_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error in upsert process:{e}")
            return False
    def execute_query(self, query: str, params: Optional[dict]= None) -> pd.DataFrame:
        """Excute the query and return a DataFrame"""
        try:
            return pd.read_sql_query(text(query), self.engine,params = params)
        except Exception as e:
            self.logger.error(f"Error when execute the query : {e}")
            return pd.DataFrame()
    def get_most_active_repos(self, days: int = 30, limit: int = 10) -> pd.DataFrame:
        """Get the most active repositories"""
        query= """
        SELECT name, full_name, stargazers_count, starts_per_day, ai_category
        html_url,pushed_at
        FROM repositories 
        WHERE pushed_at >= NOW() - INTERVAL :day DAY
        ORDER BY stars_per_day DESC
        LIMIT :limit
        """
        return self.execute_query(query,{'days':days, 'limit':limit})
    def close(self):
        """Close the connection to the database"""
        self.engine.dispose()
        self.logger.info("The connection with the database was closed")
