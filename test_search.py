"""
Quick test script to verify the movie title/year separation is working correctly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import DataLoader
from recommendation_engine import ContentBasedRecommender

def test_movie_search():
    print("🧪 Testing Movie Search Functionality")
    print("=" * 50)
    
    # Load data
    data_loader = DataLoader('data/raw')
    movies_df, ratings_df = data_loader.load_data()
    
    print(f"\n📊 Data loaded:")
    print(f"   Movies: {len(movies_df)}")
    print(f"   Ratings: {len(ratings_df)}")
    
    # Check if title separation worked
    print(f"\n🔍 Sample movie data:")
    sample_movies = movies_df.head(5)
    for _, movie in sample_movies.iterrows():
        print(f"   Original: {movie.get('original_title', 'N/A')}")
        print(f"   Clean Title: {movie.get('title', 'N/A')}")
        print(f"   Year: {movie.get('year', 'N/A')}")
        print(f"   Movie Name: {movie.get('movie_name', 'N/A')}")
        print()
    
    # Test content-based search
    content_rec = ContentBasedRecommender(movies_df)
    
    print("🎯 Testing Content-Based Search:")
    test_movies = ["Toy Story", "The Matrix", "Titanic"]
    
    for movie in test_movies:
        print(f"\n   Searching for: '{movie}'")
        try:
            recommendations = content_rec.recommend(movie, 3)
            if not recommendations.empty:
                print(f"   ✅ Found {len(recommendations)} recommendations")
                for _, rec in recommendations.iterrows():
                    print(f"      - {rec.get('Movie Title', 'N/A')}")
            else:
                print(f"   ❌ No recommendations found")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_movie_search()
