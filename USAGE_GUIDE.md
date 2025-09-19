# 🎬 MyNextMovie - Complete Usage Guide

## Quick Start Guide

### 1. Command Line Interface (CLI)
The easiest way to get started is with the command line interface:

```bash
# Interactive mode
python main.py

# Demo mode (see all algorithms in action)
python main.py demo
```

### 2. Jupyter Notebook GUI
For an interactive experience with visual widgets:

```bash
# Start Jupyter notebook
jupyter notebook

# Open the interactive GUI notebook
# Navigate to: notebooks/interactive_gui.ipynb
```

### 3. Standalone Desktop GUI
For a Netflix-like desktop application:

```bash
# Activate virtual environment first
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Run the desktop GUI
python gui_app.py
```

## Interface Options

### 🖥️ Command Line Interface (main.py)

**Features:**
- Menu-driven interface
- All 3 recommendation algorithms
- Data analytics
- Easy to use for quick testing

**Example Session:**
```
🎬 Welcome to MyNextMovie Recommendation System!
Choose your recommendation method:

==================================================
RECOMMENDATION OPTIONS:
1. 🔥 Popular Movies by Genre
2. 🎯 Similar Movies (Content-based)
3. 👥 Personalized Recommendations (Collaborative)
4. 🌟 Hybrid Recommendations
5. 📊 Data Summary
6. 🚪 Exit
==================================================

Enter your choice (1-6): 1
Enter genre (e.g., Action, Comedy, Drama): Action
Enter minimum number of reviews (e.g., 20): 50
Enter number of recommendations (e.g., 10): 5

🔥 Top 5 Popular Action Movies
===============================
1. The Matrix (1999)
   Rating: 4.26 | Reviews: 259
2. Terminator 2: Judgment Day (1991)  
   Rating: 4.23 | Reviews: 194
...
```

### 📓 Jupyter Interactive GUI (interactive_gui.ipynb)

**Features:**
- Visual widgets (dropdowns, sliders, buttons)
- Real-time data visualization
- Charts and analytics
- Perfect for experimentation

**Key Components:**
- **Popularity Recommender Widget**: Genre selection, rating thresholds
- **Content-Based Widget**: Movie search with autocomplete
- **Collaborative Widget**: User selection with activity charts
- **Hybrid Widget**: Algorithm weight adjustment
- **Analytics Dashboard**: Data visualization and statistics

### 🖼️ Desktop GUI Application (gui_app.py)

**Features:**
- Netflix-inspired dark theme
- Tabbed interface for each algorithm
- Quick selection buttons
- Real-time results display
- Movie poster placeholders

**Tabs:**
1. **🔥 Popular Movies**: Genre filtering with review thresholds
2. **🎯 Similar Movies**: Content-based similarity search
3. **👥 Personal Picks**: User-based collaborative filtering
4. **🌟 Hybrid Picks**: Combined algorithm recommendations
5. **📊 Analytics**: Data insights and statistics

## Recommendation Algorithms

### 1. 🔥 Popularity-Based Recommender

**How it works:**
- Filters movies by genre
- Applies minimum review threshold
- Ranks by average rating
- Returns top N popular movies

**Input Parameters:**
- `genre`: Movie genre (Action, Comedy, Drama, etc.)
- `min_reviews`: Minimum number of reviews (default: 50)
- `num_recommendations`: Number of results (1-20)

**Example Output:**
| S.No. | Movie Title | Average Rating | Num Reviews |
|-------|-------------|----------------|-------------|
| 1 | The Matrix (1999) | 4.26 | 259 |
| 2 | Terminator 2 (1991) | 4.23 | 194 |

**Best for:**
- New users without rating history
- Finding critically acclaimed movies
- Genre-specific browsing

### 2. 🎯 Content-Based Recommender

**How it works:**
- Analyzes movie genres using TF-IDF
- Calculates cosine similarity
- Finds movies with similar genre profiles
- Returns most similar movies

**Input Parameters:**
- `movie_title`: Reference movie title
- `num_recommendations`: Number of similar movies

**Example Output:**
| S.No. | Movie Title |
|-------|-------------|
| 1 | Toy Story 2 (1999) |
| 2 | Bug's Life, A (1998) |

**Best for:**
- Users who liked specific movies
- Finding movies in same genre/style
- Exploring similar content

### 3. 👥 Collaborative Filtering Recommender

**How it works:**
- Finds K most similar users
- Uses cosine similarity on rating patterns
- Predicts ratings for unrated movies
- Returns highest predicted ratings

**Input Parameters:**
- `user_id`: Target user ID (1-668)
- `num_recommendations`: Number of recommendations
- `k_similar_users`: Number of similar users (default: 100)

**Example Output:**
| S.No. | Movie Title |
|-------|-------------|
| 1 | Shawshank Redemption (1994) |
| 2 | Godfather, The (1972) |

**Best for:**
- Personalized recommendations
- Users with rating history
- Discovering new genres

### 4. 🌟 Hybrid Recommender

**How it works:**
- Combines collaborative filtering and popularity
- Uses weighted average of algorithm scores
- Balances personalization with popular content
- Reduces cold start problems

**Input Parameters:**
- `user_id`: Target user ID
- `num_recommendations`: Number of recommendations
- `weights`: Algorithm weights (collaborative: 0.6, popularity: 0.4)

**Best for:**
- Balanced recommendations
- New users with some data
- Most robust results

## Data Analytics

### 📊 Available Metrics

**Basic Statistics:**
- Total movies: 10,329
- Total users: 668  
- Total ratings: 105,339
- Average rating: 3.52
- Unique genres: 20
- Data sparsity: 98.47%

**Top Genres:**
1. Drama (4,361 movies)
2. Comedy (3,756 movies) 
3. Thriller (1,894 movies)
4. Romance (1,596 movies)
5. Action (1,828 movies)

**Visualizations Available:**
- Rating distribution histograms
- Genre popularity charts
- User activity patterns
- Movie release trends
- Top-rated movies analysis

## Troubleshooting

### Common Issues

**1. "Movie not found" Error**
```
Solution: Check movie title spelling
- Use exact titles from dataset
- Check for case sensitivity
- Try partial matches
```

**2. "User not found" Error**
```
Solution: Valid user IDs are 1-668
- Use existing user IDs only
- Check user activity first
```

**3. Import Errors**
```
Solution: Activate virtual environment
Windows: .venv\Scripts\activate
macOS/Linux: source .venv/bin/activate
```

**4. Performance Issues**
```
Solutions:
- Reduce k_similar_users parameter
- Lower number of recommendations
- Use smaller datasets for testing
```

### Performance Tips

**For Large Datasets:**
- Use popularity-based for quick results
- Limit collaborative filtering K parameter
- Cache user-movie matrices
- Consider data sampling

**For Better Accuracy:**
- Increase minimum review thresholds
- Use hybrid approach
- Tune algorithm weights
- Validate with test users

## Advanced Usage

### Custom Algorithm Weights
```python
# In Jupyter or Python script
weights = {
    'collaborative': 0.7,
    'popularity': 0.3
}
recommendations = hybrid_rec.get_combined_recommendations(
    user_id=1, 
    num_recommendations=10, 
    weights=weights
)
```

### Batch Processing
```python
# Get recommendations for multiple users
users = [1, 2, 3, 4, 5]
batch_recommendations = {}

for user_id in users:
    recs = collaborative_rec.recommend(user_id, 10)
    batch_recommendations[user_id] = recs
```

### Custom Data Loading
```python
# Load your own data
custom_loader = DataLoader('path/to/your/data')
movies_df, ratings_df = custom_loader.load_data()
```

## API Reference

### Core Classes

**DataLoader**
```python
loader = DataLoader('data/raw')
movies_df, ratings_df = loader.load_data()
movies_with_stats = loader.preprocess_data()
```

**PopularityRecommender**
```python
recommender = PopularityRecommender(movies_with_stats)
recs = recommender.recommend('Action', 50, 10)
```

**ContentBasedRecommender**
```python
recommender = ContentBasedRecommender(movies_df)
recs = recommender.recommend('Toy Story', 10)
```

**CollaborativeFilteringRecommender**
```python
recommender = CollaborativeFilteringRecommender(ratings_df, movies_df)
recs = recommender.recommend(1, 10, 100)
```

**HybridRecommender**
```python
hybrid = HybridRecommender(pop_rec, content_rec, collab_rec)
recs = hybrid.get_combined_recommendations(1, 10)
```

## Testing

### Run Unit Tests
```bash
python tests/test_recommenders.py
```

### Test Individual Components
```bash
# Test data loading
python -c "from src.data_loader import DataLoader; dl = DataLoader('data/raw'); print('✅ Data loading works!')"

# Test recommendations
python main.py demo
```

## File Structure Reference

```
movie-recommendation-system/
├── main.py                 # CLI application
├── gui_app.py             # Desktop GUI
├── poster_generator.py    # Movie poster creator
├── requirements.txt       # Dependencies
├── README.md             # Project documentation
├── data/
│   └── raw/              # CSV data files
├── notebooks/
│   ├── movie_recommendation_system.ipynb  # Analysis notebook
│   └── interactive_gui.ipynb             # Interactive widgets
├── src/
│   ├── data_loader.py    # Data loading utilities
│   └── recommendation_engine.py  # ML algorithms
├── tests/
│   └── test_recommenders.py  # Unit tests
├── docs/
│   └── my-next-movie.pdf # Requirements document
├── models/               # Model storage
└── posters/             # Generated movie posters
```

## Next Steps

1. **Try the Interactive Notebook**: Open `notebooks/interactive_gui.ipynb` for the best visual experience
2. **Experiment with Parameters**: Adjust sliders and dropdowns to see how recommendations change
3. **Explore Your Data**: Use the analytics dashboard to understand the dataset
4. **Test Different Users**: Try collaborative filtering with various user IDs
5. **Compare Algorithms**: Use the hybrid recommender to see combined results

## Support

- **Documentation**: Check README.md for detailed setup
- **Examples**: All interfaces include working examples
- **Test Suite**: Run tests to validate installation
- **Sample Data**: Demo mode shows all algorithms working

---

**🎬 Happy Movie Discovering with MyNextMovie! 🍿**
