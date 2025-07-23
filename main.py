import pandas as pd
import requests
from datetime import datetime
import matplotib.pyplot as plt

def get_ia_repos():
    """Extract data from the Github API"""

    topics = ["machine-learning","deep-learning","llm","generative-ai","computer-vision"]
    repos = []

    for topic in topics:
        url = "https://api.github.com/search/repositories"
        params = {
            "q":f"language:{lang}",
            "sort":"stars",
            "order":"desc",
            "per_page":100,
            "page":1
        }
        try:
            response = requests.get(url,params=params, timeout = 10)
            response.raise_for_status()
            data = response.json()

            for item in data["items"]:
                all_repos.append( 
                    {"language": lang,
                    "name":item["name"],
                    "stars":item["stargazers_count"],
                    "owner": item["owner"]["login"],
                    "forks": item["forks_count"],
                    "updated_at":item["updated_at"]})
        except requests.exceptions.RequestException as e:
            print(f"Error in network with {lang}: {e}")
        except ValueError as ve:
            print(f"Error in JSON with {lang}: {ve}")
        except Exception as ex:
            print(f"Unexpected error with {lang}: {ex}")

    return all_repos
def transform_data(raw_data):
    if not raw_data:
        return pd.DataFrame()
    df = pd.DataFrame(raw_data)
    df["updated_at"] = pd.to_datetime(df["updated_at"], utc=True)
    df["updated_at"] = df["updated_at"].dt.tz_localize(None)
    df["year_month"] = df["updated_at"].dt.to_period("M").astype(str)
    return df 

if __name__ == "__main__":
    results = extract_data()
    transformed_results = transform_data(results)

