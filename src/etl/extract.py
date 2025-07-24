import requests
import pandas as pd
import os
from typing import List, Dict, Any
from datetime import datetime 
from tqdm import tqdm 
from scr.utils.logger import get_logger
from scr.config import settings 

class GitHubExtractor:
    def __init__(self):
        self.base_url = "https://api.github.com/search/repositories"
        self.headers = {
            "Authorization": f"token{settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
            }
        self.timeout = 30
    def _make_request(self, params: Dict[str, Any]) -> Optional[Dict[str,Any]]:
        try:
            response = requests.get(
                self.base_url,
                headers = self.headers,
                params= params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e :
            logger.error(f"Error in the Github API:{e}")
            return None
    def get_repos_by_topics(self, topics: List[str], max_repos: int = 100) -> pd.DataFrame:
        all_repos = []

        for topic in tqdm(topics, desc= "Extract repositories"):
            params = {
                "q":f"topic:{topic} stars:>100",
                "sort":"stars",
                "order":"desc",
                "per_page": min(100, max_repos),
                "page": 1
            }
            data = self._make_request(params)
            if not data or 'items' not in data:
                continue
        for repo in data['items']:
            repo_data = {
                'github_id': repo['id'],
                'name': repo['name'],
                'html_url': repo['html_url'],
                'description': repo['description'],
                'language': repo['language'],
                'topics': repo['topics'],
                'stargazers_count': repo['stargazers_count'],
                'forks_count': repo['forks_count'],
                'open_issues': repo['open_issues'],
                'created_at': repo['created_at'],
                'pushed_at': repo['pushed_at'],
                'topic_searched': topic,
                'extracted_at': datetime.now().isoformat()
            }
