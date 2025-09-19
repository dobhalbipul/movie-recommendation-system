# 🎬 Movie Recommendation System

An AI-powered movie recommendation system implementing multiple machine learning algorithms with an interactive web interface.

**Developer:** [Bipul Kumar Dobhal](https://github.com/dobhalbipul)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## � Features

- **🔥 Popularity-Based**: Trending movies by genre and ratings
- **🎭 Content-Based**: Similar movies using genre similarity (Cosine Similarity)
- **👥 Collaborative Filtering**: Personalized recommendations via user similarity
- **🌟 Hybrid**: Combined approach for optimal results
- **🎨 Interactive GUI**: Streamlit web interface with Netflix-style design
## 🚀 Quick Start

```bash
# Clone repository
git clone <repository-url>
cd movie-recommendation-system

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Download dataset from Kaggle
# Place movies.csv and ratings.csv in data/raw/

# Launch application
streamlit run streamlit_app.py
```

## 📊 Dataset
- **Movies**: 10,329 movies with genres and metadata
- **Ratings**: 105,339 ratings from 668 users (0.5-5.0 scale)
- **Source**: [Kaggle Movie Dataset](https://www.kaggle.com/code/ayushimishra2809/movie-recommendationsystem/data)

## 🧠 Algorithms

### Popularity-Based
- **Method**: Statistical ranking by average rating and review count
- **Use Case**: Trending movies, cold start users
- **Complexity**: O(n log n)

### Content-Based
- **Method**: Cosine similarity on binary genre vectors
- **Use Case**: "Movies like X" recommendations
- **Example**: Action+Drama movies → similar genre combinations

### Collaborative Filtering
- **Method**: User-based similarity with K-nearest neighbors
- **Use Case**: Personalized recommendations
- **Formula**: `predicted_rating = Σ(similarity × rating) / Σ(similarity)`

### Hybrid
- **Method**: Weighted combination of algorithms
- **Default**: 60% collaborative + 40% popularity
- **Benefit**: Balanced personalization and diversity
## � Notebooks

### 1. Step-by-Step Development (`movie_recommendation_system.ipynb`)

A comprehensive Jupyter notebook that walks through the entire development process of building three different recommendation systems:

**What it covers:**
- **Data Exploration & Analysis** - Understanding the MovieLens dataset structure
- **Data Preprocessing** - Cleaning and preparing data for algorithms
- **Algorithm Implementation** - Building all three recommendation systems from scratch
- **Performance Analysis** - Comparing different approaches with visualizations

**Key Learning Sections:**
1. **Data Insights** - Statistics on movies, users, ratings, and genre distributions
2. **Popularity-Based System** - Genre-filtered recommendations based on average ratings
3. **Content-Based System** - Movie similarity using genre features and cosine similarity
4. **Collaborative Filtering** - User-based recommendations using rating patterns
5. **Visualizations** - Charts showing rating distributions, genre popularity, and user activity

### 2. Interactive GUI (`interactive_gui.ipynb`)

A user-friendly interface using ipywidgets that lets you test all recommendation systems interactively:

**Features:**
- 🔥 **Popularity Recommender** - Filter by genre, minimum reviews, and get top-rated movies
- 🎯 **Content-Based Recommender** - Enter a movie title to find similar movies
- 👥 **Collaborative Filtering** - Get personalized recommendations based on user ID
- 🌟 **Hybrid Recommender** - Combine multiple algorithms with custom weights
- 📊 **Analytics Dashboard** - Visualize dataset statistics and trends

**Interactive Controls:**
- Dropdown menus for genre selection
- Sliders for parameters (number of recommendations, similarity thresholds)
- Text inputs for movie titles and user IDs
- Real-time weight adjustment for hybrid recommendations
- Progress bars and loading indicators

### How to Use the Notebooks

1. **For Learning/Development:**
   ```bash
   jupyter notebook notebooks/movie_recommendation_system.ipynb
   ```

2. **For Interactive Testing:**
   ```bash
   jupyter notebook notebooks/interactive_gui.ipynb
   ```

**Requirements for Notebooks:**
- All dependencies from `requirements.txt`
- Additional for GUI: `ipywidgets`, `matplotlib`, `seaborn`

**Install additional dependencies:**
```bash
pip install ipywidgets matplotlib seaborn
```

## �📁 Project Structure

```
movie-recommendation-system/
├── src/
│   ├── data_loader.py           # Data processing
│   └── recommendation_engine.py # ML algorithms
├── data/raw/
│   ├── movies.csv              # Movie metadata
│   └── ratings.csv             # User ratings
├── notebooks/                  # Jupyter analysis
├── streamlit_app.py           # Web interface
└── requirements.txt           # Dependencies
```

## 🛠️ Tech Stack

- **Backend**: Python, Pandas, NumPy, Scikit-learn
- **Frontend**: Streamlit with Netflix-style UI
- **ML**: Cosine Similarity, User-based Collaborative Filtering
- **Visualization**: Plotly charts and analytics

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## � Acknowledgments

- [Kaggle Dataset](https://www.kaggle.com/code/ayushimishra2809/movie-recommendationsystem/data) by Ayushi Mishra
- MovieLens for data format standards
- Streamlit for the web framework

---

⭐ **Star this repo if you found it helpful!**

