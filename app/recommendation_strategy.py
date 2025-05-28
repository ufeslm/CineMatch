from abc import ABC, abstractmethod
from typing import List, Dict
import requests
import os

class RecommendationStrategy(ABC):
    def __init__(self):
        self.api_key = os.environ.get('TMDB_API_KEY')
        self.base_url = 'https://api.themoviedb.org/3'

    @abstractmethod
    def get_recommendations(self, user_id: int, num_recommendations: int = 5) -> List[Dict]:
        pass

class CollaborativeFiltering(RecommendationStrategy):
    def get_recommendations(self, user_id: int, num_recommendations: int = 5) -> List[Dict]:
        # Implementation of collaborative filtering using TMDB API
        response = requests.get(
            f'{self.base_url}/movie/popular',
            params={
                'api_key': self.api_key,
                'language': 'en-US'
            }
        )
        return response.json().get('results', [])[:num_recommendations]

class ContentBasedFiltering(RecommendationStrategy):
    def get_recommendations(self, user_id: int, num_recommendations: int = 5) -> List[Dict]:
        # Implementation of content-based filtering using TMDB API
        response = requests.get(
            f'{self.base_url}/movie/top_rated',
            params={
                'api_key': self.api_key,
                'language': 'en-US'
            }
        )
        return response.json().get('results', [])[:num_recommendations]

class HybridRecommendation(RecommendationStrategy):
    def get_recommendations(self, user_id: int, num_recommendations: int = 5) -> List[Dict]:
        # Implementation of hybrid recommendation combining both approaches
        response = requests.get(
            f'{self.base_url}/movie/now_playing',
            params={
                'api_key': self.api_key,
                'language': 'en-US'
            }
        )
        return response.json().get('results', [])[:num_recommendations] 