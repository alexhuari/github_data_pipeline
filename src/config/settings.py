import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()
class Settings:
    #Settings of the database 
    DB_HOST: str = os.getenv("DB_HOST","localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD","")

    #Settings of Github API 
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_API_VERSION: str = os.getenv("GITHUB_API_VERSION", "2022-11-28")
    GITHUB_PER_PAGE: int = int(os.getenv("GITHUB_PER_PAGE", "100"))
    GITHUB_TIMEOUT: int = int(os.getenv("GITHUB_TIMEOUT","30"))

    #Settings of the project
    MAX_REPOS: int = int(os.getenv("MAX_REPOS","500"))
    TOPICS: List[str] = os.getenv("TOPICS","llm,generative-ai,machine-learning,deep-learning, computer-vision,nlp").split(",")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    #Settings of reports
    REPORT_OUTPUT_DIR: str = os.getenv("REPORT_OUTPUT_DIR","reports")
    DAYS_FOR_TREND_ANALYSIS: int = int(os.getenv("DAYS_FOR_TREND_ANALYSIS","30"))

    #Thresholds for analysis
    STAR_THRESHOLD: int = int(os.getenv("STAR_THRESHOLD","100"))
    FORKS_PER_STAR_THRESHOLLD = float = float(os.getenv("FORKS_PER_STAR_THRESHOLD","0.1"))

    #Classification of IA categories
    AI_CATEGORIES: Dict[str,List[str]] = {
        "LLM": ["llm", "large language model", "gpt", "transformer"],
        "Generative-AI": ["generative", "diffusion", "gan", "stable diffusion"],
        "Computer-Vision": ["computer vision", "cv", "object detection", "yolo"],
        "NLP": ["nlp", "natural language", "text processing", "sentiment analysis"]

    }

    #Settings of logging
    LOGGING_CONFIG: Dict[str, Any] = {
        "version":1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard":{
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
        },
        "handlers":{
            "console":{
                "class": "logging.StreamHandler",
                "formatter":"standard",
                "level":LOG_LEVEL,
                "stream":"ext://sys:stdout"
            },
            "file":{
                "class":"logging.handler.RotatingFileHandler",
                "formatter":"standard",
                "filename":"logs/github_analysis.log",
                "maxBytes":10485760, #10MB
                "backupCount":5,
                "level":LOG_LEVEL
            }
        },
        "loggers":{
            "":{ #root logger
                "handlers": ["console", "file"],
                "level": LOG_LEVEL,
                "propagate": False
            },
            "src":{
                "handlers":["console", "file"],
                "level": LOG_LEVEL,
                "propagate": False
            },
            "sqlalchemy":{
                "handlers":["file"],
                "level":"WARNING",
                "propagate": False
            }
        }   
    }
# Single configuration instance
settings = Settings()
