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
## 📁 Project Structure

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
- **ML**: Cosine Similarity, K-Nearest Neighbors
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

