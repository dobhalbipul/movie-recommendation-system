import sys
sys.path.append('src')
from data_loader import DataLoader
from recommendation_engine import ContentBasedRecommender, CollaborativeFilteringRecommender

# Test current outputs
print("Testing current recommendation outputs...")

dl = DataLoader('data/raw')
movies, ratings = dl.load_data()
movies_stats = dl.preprocess_data()

# Test ContentBased
print("\n=== ContentBasedRecommender ===")
cb = ContentBasedRecommender(movies_stats)
cb_result = cb.recommend('Toy Story', 2)
print("Columns:", cb_result.columns.tolist())
if len(cb_result) > 0:
    print("Sample data:", cb_result.iloc[0].to_dict())

# Test CollaborativeFiltering  
print("\n=== CollaborativeFilteringRecommender ===")
cf = CollaborativeFilteringRecommender(ratings, movies_stats)
cf_result = cf.recommend(1, 2, 50)
print("Columns:", cf_result.columns.tolist())
if len(cf_result) > 0:
    print("Sample data:", cf_result.iloc[0].to_dict())
