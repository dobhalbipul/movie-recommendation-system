import sys
sys.path.append('src')
from data_loader import DataLoader
from recommendation_engine import PopularityRecommender

# Load data
dl = DataLoader('data/raw')
movies, ratings = dl.load_data()
movies_stats = dl.preprocess_data()

# Test PopularityRecommender with different minimum review thresholds
pop_rec = PopularityRecommender(movies_stats)

print("Testing minimum reviews filter:")
print("================================")

# Test with min_reviews=10
result1 = pop_rec.recommend('Action', 10, 3)
print(f"\nMin reviews=10, got {len(result1)} movies:")
if len(result1) > 0:
    print(result1[['Movie Title', 'Num Reviews']].to_string())

# Test with min_reviews=100
result2 = pop_rec.recommend('Action', 100, 3)
print(f"\nMin reviews=100, got {len(result2)} movies:")
if len(result2) > 0:
    print(result2[['Movie Title', 'Num Reviews']].to_string())

# Test with min_reviews=500
result3 = pop_rec.recommend('Action', 500, 3)
print(f"\nMin reviews=500, got {len(result3)} movies:")
if len(result3) > 0:
    print(result3[['Movie Title', 'Num Reviews']].to_string())
