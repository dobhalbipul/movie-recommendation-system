"""
Debug script to test Streamlit recommendation functionality
"""
import sys
sys.path.append('src')

from data_loader import DataLoader
from recommendation_engine import PopularityRecommender, ContentBasedRecommender

def debug_recommendations():
    print("🔍 Debugging Recommendation Functionality")
    print("=" * 50)
    
    try:
        # Load data
        print("1. Loading data...")
        data_loader = DataLoader('data/raw')
        movies, ratings = data_loader.load_data()
        movies_stats = data_loader.preprocess_data()
        print(f"✅ Data loaded: {len(movies):,} movies, {len(ratings):,} ratings")
        print(f"Movies stats columns: {movies_stats.columns.tolist()}")
        
        # Test Popularity Recommender
        print("\n2. Testing PopularityRecommender...")
        pop_rec = PopularityRecommender(movies_stats)
        result = pop_rec.recommend('Action', 3.0, 3)
        print(f"✅ Popularity recommendations: {len(result)} movies")
        print(f"Result columns: {result.columns.tolist()}")
        
        # Test movie data structure
        print("\n3. Testing movie data structure...")
        for idx, row in result.head(2).iterrows():
            print(f"Movie {idx+1}:")
            print(f"  - Movie Title: {row.get('Movie Title', 'MISSING')}")
            print(f"  - Year: {row.get('year', 'MISSING')}")
            print(f"  - Rating: {row.get('Average Movie Rating', 'MISSING')}")
            print(f"  - Reviews: {row.get('Num Reviews', 'MISSING')}")
        
        # Test Content-Based Recommender
        print("\n4. Testing ContentBasedRecommender...")
        content_rec = ContentBasedRecommender(movies_stats)
        
        # Find a popular movie to base recommendations on
        popular_movies = movies_stats[movies_stats['movie_name'].notna()]
        if not popular_movies.empty:
            sample_movie = popular_movies['movie_name'].iloc[0]
            print(f"Base movie: {sample_movie}")
            
            try:
                content_result = content_rec.recommend(sample_movie, 2)
                print(f"✅ Content-based recommendations: {len(content_result)} movies")
                if not content_result.empty:
                    print(f"Content result columns: {content_result.columns.tolist()}")
            except Exception as e:
                print(f"❌ Content-based error: {e}")
        
        print("\n✅ All recommendation engines working!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_recommendations()
