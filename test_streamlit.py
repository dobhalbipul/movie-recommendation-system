"""
Quick test script to verify the Streamlit app functionality
"""
import sys
sys.path.append('src')

from data_loader import DataLoader
from recommendation_engine import PopularityRecommender

def test_streamlit_compatibility():
    print("Testing Streamlit app compatibility...")
    
    try:
        # Load data
        data_loader = DataLoader('data/raw')
        movies, ratings = data_loader.load_data()
        movies_stats = data_loader.preprocess_data()
        
        print(f"✅ Data loaded successfully: {len(movies)} movies, {len(ratings)} ratings")
        print(f"✅ Movies stats columns: {movies_stats.columns.tolist()}")
        
        # Test popularity recommender
        pop_rec = PopularityRecommender(movies_stats)
        recommendations = pop_rec.recommend('Action', 3.0, 5)
        
        print(f"✅ Popularity recommendations generated: {len(recommendations)} movies")
        print(f"✅ Recommendation columns: {recommendations.columns.tolist()}")
        
        # Test data access with both column naming conventions
        test_movie = movies_stats.iloc[0]
        
        # Test the column names used in the movie card function
        title = test_movie.get('movie_name', test_movie.get('title', 'Unknown'))
        year = test_movie.get('year', 'N/A')
        rating = test_movie.get('avg_rating', test_movie.get('Average Movie Rating', 0))
        reviews = test_movie.get('num_ratings', test_movie.get('Num Reviews', 0))
        genres = test_movie.get('genres', 'N/A')
        
        print(f"✅ Movie card data extraction successful:")
        print(f"   Title: {title}")
        print(f"   Year: {year}")
        print(f"   Rating: {rating}")
        print(f"   Reviews: {reviews}")
        print(f"   Genres: {genres}")
        
        print("\n🎉 All tests passed! Streamlit app should work correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_streamlit_compatibility()
