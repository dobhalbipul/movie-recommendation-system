import sys
sys.path.append('src')
from data_loader import DataLoader
from recommendation_engine import PopularityRecommender

# Test the genre fix
dl = DataLoader('data/raw')
movies, ratings = dl.load_data()
movies_stats = dl.preprocess_data()

pop_rec = PopularityRecommender(movies_stats)
result = pop_rec.recommend('Action', 50, 2)

print("Columns in result:", result.columns.tolist())
print("\nFirst movie data:")
print(result.iloc[0].to_dict())
print("\nGenres for first movie:", result.iloc[0]['genres'])
