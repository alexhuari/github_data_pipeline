import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GitHubTransformer:
    @staticmethod
    def clean_language(language: str) -> str:
        """Normalize language names"""
        if not language:
            return 'unknown'
        language = language.lower().strip()
        replacements = {
            'c++': 'cpp',
            'jupyter notebook': 'python',
            'typescript': 'javascript'
        }
        return replacements.get(language, language)
    
    @staticmethod
    def classify_repo(repo: Dict[str, Any]) -> str:
        """Clasify the report for category"""
        desc = str(repo.get('description', '')).lower()
        topics = ' '.join(repo.get('topics', [])).lower()
        
        if any(kw in desc + topics for kw in ['llm', 'large language model', 'gpt']):
            return 'LLM'
        elif any(kw in desc + topics for kw in ['generative', 'diffusion', 'gan']):
            return 'Generative-AI'
        elif any(kw in desc + topics for kw in ['computer vision', 'cv', 'object detection']):
            return 'Computer-Vision'
        elif any(kw in desc + topics for kw in ['nlp', 'natural language']):
            return 'NLP'
        return 'General-ML'
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all the transformations"""
        try:
            # Change to a format date
            date_cols = ['created_at', 'pushed_at', 'extracted_at']
            for col in date_cols:
                df[col] = pd.to_datetime(df[col])
            
            # Calculation of metrics
            df['age_days'] = (datetime.now() - df['created_at']).dt.days
            df['days_since_update'] = (datetime.now() - df['pushed_at']).dt.days
            df['stars_per_day'] = np.where(
                df['age_days'] > 0,
                df['stargazers_count'] / df['age_days'],
                0
            )
            df['forks_per_star'] = np.where(
                df['stargazers_count'] > 0,
                df['forks_count'] / df['stargazers_count'],
                0
            )
            
            # Classify repositories 
            df['ai_category'] = df.apply(self.classify_repo, axis=1)
            
            # Leve of activities
            bins = [0, 7, 30, 90, 365, np.inf]
            labels = ['daily', 'weekly', 'monthly', 'yearly', 'inactive']
            df['activity_level'] = pd.cut(
                df['days_since_update'],
                bins=bins,
                labels=labels,
                right=False
            )
            
            # Normalizar lenguaje
            df['language'] = df['language'].apply(self.clean_language)
            
            return df
            
        except Exception as e:
            logger.error(f"Error en transformación: {e}")
            raise