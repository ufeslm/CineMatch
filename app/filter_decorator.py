from abc import ABC, abstractmethod
from typing import List, Dict

class RecommendationFilter(ABC):
    @abstractmethod
    def apply_filter(self, recommendations: List[Dict]) -> List[Dict]:
        pass

class GenreFilter(RecommendationFilter):
    def __init__(self, genre: str):
        self.genre = genre

    def apply_filter(self, recommendations: List[Dict]) -> List[Dict]:
        return [rec for rec in recommendations if self.genre in rec.get('genre_ids', [])]

class RatingFilter(RecommendationFilter):
    def __init__(self, min_rating: float):
        self.min_rating = min_rating

    def apply_filter(self, recommendations: List[Dict]) -> List[Dict]:
        filtered = [rec for rec in recommendations if rec.get('vote_average', 0) >= self.min_rating]
        print(f"Rating filter: {len(recommendations)} -> {len(filtered)} (min rating: {self.min_rating})")
        return filtered

class YearFilter(RecommendationFilter):
    def __init__(self, year: int):
        self.year = year

    def apply_filter(self, recommendations: List[Dict]) -> List[Dict]:
        filtered = []
        skipped = 0
        for rec in recommendations:
            release_date = rec.get('release_date', '')
            if release_date and len(release_date) >= 4:
                try:
                    movie_year = int(release_date[:4])
                    if movie_year >= self.year:
                        filtered.append(rec)
                    else:
                        skipped += 1
                except ValueError:
                    # Skip if release_date doesn't start with a valid year
                    skipped += 1
            else:
                skipped += 1
        
        print(f"Year filter: {len(recommendations)} -> {len(filtered)} (min year: {self.year}, skipped: {skipped})")
        return filtered

class FilteredRecommendation:
    def __init__(self, recommendations: List[Dict]):
        self.recommendations = recommendations
        self.filters = []

    def add_filter(self, filter: RecommendationFilter):
        self.filters.append(filter)

    def get_filtered_recommendations(self) -> List[Dict]:
        filtered = self.recommendations
        for filter in self.filters:
            filtered = filter.apply_filter(filtered)
            # If filtering results in no movies, skip this filter
            if not filtered:
                print(f"Warning: Filter {filter.__class__.__name__} resulted in no movies, skipping this filter")
                continue
        return filtered 