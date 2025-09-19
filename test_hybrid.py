import sys
sys.path.append('src')
from data_loader import DataLoader
from recommendation_engine import *

print("Testing HybridRecommender with complete data...")

dl = DataLoader('data/raw')
movies, ratings = dl.load_data()
movies_stats = dl.preprocess_data()

# Create individual recommenders
popularity_rec = PopularityRecommender(movies_stats)
content_rec = ContentBasedRecommender(movies_stats)
collab_rec = CollaborativeFilteringRecommender(ratings, movies_stats)

# Create hybrid recommender
hybrid_rec = HybridRecommender(popularity_rec, content_rec, collab_rec)

# Test hybrid recommendations
print("\n=== HybridRecommender (Updated) ===")
hybrid_result = hybrid_rec.get_combined_recommendations(1, 3)
print("Columns:", hybrid_result.columns.tolist())
if len(hybrid_result) > 0:
    print("\nSample data:")
    print(hybrid_result.iloc[0][['Movie Title', 'Average Movie Rating', 'Num Reviews', 'genres']])
    print("\nAll recommendations:")
    for _, row in hybrid_result.iterrows():
        print(f"- {row['Movie Title']} | Rating: {row['Average Movie Rating']:.1f} | Reviews: {row['Num Reviews']} | Genres: {row['genres']}")
