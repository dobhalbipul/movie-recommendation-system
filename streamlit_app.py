import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add src directory to path
sys.path.append('src')

from data_loader import DataLoader
from recommendation_engine import (
    PopularityRecommender, 
    ContentBasedRecommender, 
    CollaborativeFilteringRecommender, 
    HybridRecommender
)

# Netflix-inspired styling
st.set_page_config(
    page_title="CinemaAI - Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Netflix-inspired CSS
netflix_css = """
<style>
    /* Import better fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --netflix-red: #e50914;
        --netflix-dark-red: #b20710;
        --netflix-black: #141414;
        --netflix-dark-gray: #2d2d2d;
        --netflix-gray: #564d4d;
        --netflix-light-gray: #b3b3b3;
        --netflix-white: #ffffff;
        --netflix-background: #0a0a0a;
        --netflix-card-bg: #1f1f1f;
    }
    
    /* Global styles */
    .main > div {
        background: linear-gradient(135deg, var(--netflix-background) 0%, var(--netflix-black) 100%);
        min-height: 100vh;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar styling */
    .css-1d391kg, .css-1cypcdb {
        background: linear-gradient(180deg, var(--netflix-black) 0%, var(--netflix-background) 100%);
        border-right: 2px solid var(--netflix-dark-gray);
    }
    
    /* Custom header */
    .cinema-header {
        background: linear-gradient(135deg, var(--netflix-black) 0%, var(--netflix-dark-gray) 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid var(--netflix-dark-gray);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .cinema-title {
        color: var(--netflix-white);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
    }
    
    .cinema-subtitle {
        color: var(--netflix-light-gray);
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-weight: 400;
    }
    
    .cinema-accent {
        color: var(--netflix-red);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--netflix-white) !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
    }
    
    h1 { color: var(--netflix-red) !important; }
    h2 { color: var(--netflix-red) !important; }
    
    /* Movie cards */
    .movie-card {
        background: linear-gradient(145deg, var(--netflix-card-bg) 0%, var(--netflix-dark-gray) 100%);
        border: 1px solid var(--netflix-gray);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--netflix-red), var(--netflix-dark-red));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .movie-card:hover {
        border-color: var(--netflix-red);
        box-shadow: 0 8px 30px rgba(229,9,20,0.4);
        transform: translateY(-4px);
    }
    
    .movie-card:hover::before {
        opacity: 1;
    }
    
    .movie-title {
        color: var(--netflix-white);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    .movie-details {
        color: var(--netflix-light-gray);
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
    
    .movie-year-badge {
        background: linear-gradient(135deg, var(--netflix-red), var(--netflix-dark-red));
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .rating-section {
        margin-bottom: 0.8rem;
    }
    
    .movie-rating {
        color: var(--netflix-red);
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
    }
    
    .info-section {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }
    
    .movie-reviews {
        color: var(--netflix-light-gray);
        font-size: 0.85rem;
    }
    
    .movie-genre {
        color: var(--netflix-light-gray);
        font-size: 0.85rem;
        font-style: italic;
    }
    
    .movie-year {
        background: var(--netflix-dark-gray);
        color: var(--netflix-light-gray);
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--netflix-red) 0%, var(--netflix-dark-red) 100%);
        color: var(--netflix-white);
        border: none;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(229,9,20,0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--netflix-dark-red) 0%, #900c0c 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(229,9,20,0.5);
    }
    
    /* Form inputs */
    .stSelectbox > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: var(--netflix-dark-gray) !important;
        border: 1px solid var(--netflix-gray) !important;
        color: var(--netflix-white) !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif;
    }
    
    .stSelectbox > div > div:focus-within, .stTextInput > div > div:focus-within {
        border-color: var(--netflix-red) !important;
        box-shadow: 0 0 0 1px var(--netflix-red) !important;
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, var(--netflix-card-bg) 0%, var(--netflix-dark-gray) 100%);
        border: 1px solid var(--netflix-gray);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    .metric-value {
        color: var(--netflix-red);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: var(--netflix-light-gray);
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--netflix-dark-gray);
        border-radius: 8px;
        padding: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--netflix-light-gray);
        border-radius: 6px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 12px 24px !important;
        margin: 0 4px;
        min-width: 180px;
        text-align: center;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--netflix-red) !important;
        color: var(--netflix-white) !important;
        padding: 12px 28px !important;
        box-shadow: 0 2px 8px rgba(229, 9, 20, 0.3);
    }
    
    /* Messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.1), rgba(0, 200, 0, 0.1));
        border: 1px solid #00cc00;
        color: #00ff00;
        border-radius: 8px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(229, 9, 20, 0.1), rgba(180, 7, 16, 0.1));
        border: 1px solid var(--netflix-red);
        color: var(--netflix-red);
        border-radius: 8px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(255, 152, 0, 0.1));
        border: 1px solid #ffc107;
        color: #ffc107;
        border-radius: 8px;
    }
    
    /* Tables */
    .dataframe {
        background-color: var(--netflix-card-bg) !important;
        color: var(--netflix-white) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    .dataframe th {
        background-color: var(--netflix-red) !important;
        color: var(--netflix-white) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border: none !important;
    }
    
    .dataframe td {
        background-color: var(--netflix-card-bg) !important;
        color: var(--netflix-white) !important;
        border-bottom: 1px solid var(--netflix-gray) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Sidebar labels */
    .css-qrbaxs, .css-1cpxqw2 {
        color: var(--netflix-white) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* Welcome section */
    .welcome-section {
        background: linear-gradient(135deg, var(--netflix-card-bg) 0%, var(--netflix-dark-gray) 100%);
        border: 1px solid var(--netflix-gray);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .feature-card {
        background: var(--netflix-dark-gray);
        border: 1px solid var(--netflix-gray);
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        border-color: var(--netflix-red);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        color: var(--netflix-white);
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: var(--netflix-light-gray);
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        line-height: 1.4;
    }
</style>
"""

st.markdown(netflix_css, unsafe_allow_html=True)

# Enhanced header
st.markdown("""
<div class="cinema-header">
    <h1 class="cinema-title">🎬 My CinemaAI <span class="cinema-accent">Movies</span></h1>
    <p class="cinema-subtitle">AI-Powered Movie Recommendations | Discover Your Perfect Match</p>
</div>
""", unsafe_allow_html=True)

# Temporarily disable cache to pick up data loader fixes
# @st.cache_data
def load_movie_data():
    """Load and cache movie data"""
    try:
        data_loader = DataLoader('data/raw')
        movies, ratings = data_loader.load_data()
        movies_stats = data_loader.preprocess_data()
        return movies, ratings, movies_stats, data_loader
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None, None

@st.cache_data
def get_available_genres(_movies_stats):
    """Get list of available genres"""
    genres = set()
    for genre_list in _movies_stats['genres'].dropna():
        genres.update([g.strip() for g in genre_list.split('|')])
    return sorted(list(genres))

def create_movie_card(movie_data):
    """Create a professional movie card"""
    # Handle different column naming conventions from different recommenders
    title = (movie_data.get('Movie Title') or 
             movie_data.get('movie_name') or 
             movie_data.get('title') or 
             'Unknown Movie')
    
    year = movie_data.get('year', 'N/A')
    
    rating = (movie_data.get('Average Movie Rating') or 
              movie_data.get('avg_rating') or 
              0)
    
    reviews = (movie_data.get('Num Reviews') or 
               movie_data.get('num_ratings') or 
               0)
    
    genres = movie_data.get('genres', 'N/A')
    
    # Truncate long genre lists
    if len(str(genres)) > 40:
        genres = str(genres)[:37] + "..."
    
    # Generate star rating
    star_rating = "⭐" * int(rating) if rating > 0 else "☆☆☆☆☆"
    
    card_html = f"""
    <div class="movie-card">
        <div class="movie-title">{title}</div>
        <div class="movie-year-badge">📅 {year}</div>
        <div class="movie-details">
            <div class="rating-section">
                <span class="movie-rating">{star_rating} {rating:.1f}/5</span>
            </div>
            <div class="info-section">
                <span class="movie-reviews">👥 {int(reviews):,} reviews</span>
                <span class="movie-genre">🎭 {genres}</span>
            </div>
        </div>
    </div>
    """
    return card_html

def display_recommendations_grid(recommendations, title):
    """Display recommendations in a grid layout"""
    st.markdown(f"### {title}")
    
    if recommendations.empty:
        st.warning("No recommendations found. Try adjusting your criteria.")
        return
    
    # Create columns for grid layout
    cols = st.columns(2)
    
    for idx, (_, movie) in enumerate(recommendations.iterrows()):
        col = cols[idx % 2]
        with col:
            st.markdown(create_movie_card(movie), unsafe_allow_html=True)

def create_analytics_dashboard(movies_stats, recommendations):
    """Create analytics dashboard"""
    st.markdown("### 📊 Analytics Dashboard")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{:,}</div>
            <div class="metric-label">Total Movies</div>
        </div>
        """.format(len(movies_stats)), unsafe_allow_html=True)
    
    with col2:
        # Use correct column name
        rating_col = 'avg_rating' if 'avg_rating' in movies_stats.columns else 'Average Movie Rating'
        avg_rating = movies_stats[rating_col].mean()
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{:.1f}</div>
            <div class="metric-label">Avg Rating</div>
        </div>
        """.format(avg_rating), unsafe_allow_html=True)
    
    with col3:
        # Use correct column name
        reviews_col = 'num_ratings' if 'num_ratings' in movies_stats.columns else 'Num Reviews'
        total_reviews = movies_stats[reviews_col].sum()
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{:,}</div>
            <div class="metric-label">Total Reviews</div>
        </div>
        """.format(int(total_reviews)), unsafe_allow_html=True)
    
    with col4:
        if not recommendations.empty:
            # Use correct column name for recommendations
            rec_rating_col = 'avg_rating' if 'avg_rating' in recommendations.columns else 'Average Movie Rating'
            if rec_rating_col in recommendations.columns:
                rec_avg = recommendations[rec_rating_col].mean()
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{:.1f}</div>
                    <div class="metric-label">Rec Avg Rating</div>
                </div>
                """.format(rec_avg), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Recommendations</div>
                </div>
                """.format(len(recommendations)), unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Rating distribution
        if not recommendations.empty:
            rec_rating_col = 'avg_rating' if 'avg_rating' in recommendations.columns else 'Average Movie Rating'
            if rec_rating_col in recommendations.columns:
                fig = px.histogram(
                    recommendations, 
                    x=rec_rating_col,
                    title='Rating Distribution of Recommendations',
                    nbins=20,
                    color_discrete_sequence=['#e50914']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(26,26,26,1)',
                    font_color='white',
                    title_font_color='#e50914',
                    title_font_size=16,
                    xaxis_title='Rating',
                    yaxis_title='Count'
                )
                st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Year distribution
        if not recommendations.empty and 'year' in recommendations.columns:
            year_counts = recommendations['year'].value_counts().head(10)
            if not year_counts.empty:
                fig = px.bar(
                    x=year_counts.index,
                    y=year_counts.values,
                    title='Top Years in Recommendations',
                    color_discrete_sequence=['#e50914']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(26,26,26,1)',
                    font_color='white',
                    title_font_color='#e50914',
                    title_font_size=16,
                    xaxis_title='Year',
                    yaxis_title='Number of Movies'
                )
                st.plotly_chart(fig, width='stretch')

def main():
    # Load data
    with st.spinner("🎬 Loading movie database..."):
        movies, ratings, movies_stats, data_loader = load_movie_data()
    
    if movies_stats is None:
        st.error("Failed to load movie data. Please check if the data files exist.")
        return
    
    st.success(f"✅ Loaded {len(movies):,} movies and {len(ratings):,} ratings!")
    
    # Sidebar controls
    st.sidebar.markdown("## 🎯 Recommendation Settings")
    
    # Recommendation type
    rec_type = st.sidebar.selectbox(
        "Choose Recommendation Type",
        ["Popularity-Based", "Content-Based", "Collaborative Filtering", "Hybrid"],
        help="Select the type of recommendation algorithm"
    )
    
    # Type-specific parameters
    user_id = None
    movie_title = None
    min_reviews = None
    k_similar_users = None
    
    if rec_type == "Popularity-Based":
        # Popularity: Genre, minimum reviews, num recommendations
        genres = get_available_genres(movies_stats)
        selected_genre = st.sidebar.selectbox(
            "Select Genre",
            ["All"] + genres,
            help="Filter movies by genre"
        )
        
        min_reviews = st.sidebar.number_input(
            "Minimum Reviews Threshold",
            min_value=1,
            max_value=1000,
            value=50,
            help="Minimum number of reviews required for a movie to be considered"
        )
        
        num_recommendations = st.sidebar.slider(
            "Number of Recommendations",
            min_value=5,
            max_value=50,
            value=10,
            help="How many movies to recommend"
        )
    
    elif rec_type == "Content-Based":
        # Content: Movie title, num recommendations
        available_movies = movies_stats['movie_name'].dropna().tolist()
        movie_title = st.sidebar.selectbox(
            "Select a Movie You Liked",
            available_movies[:100],  # Limit to first 100 for performance
            help="Select a movie you enjoyed for similar recommendations"
        )
        
        num_recommendations = st.sidebar.slider(
            "Number of Recommendations",
            min_value=5,
            max_value=50,
            value=10,
            help="How many movies to recommend"
        )
    
    elif rec_type == "Collaborative Filtering":
        # Collaborative: User ID, num recommendations, threshold of similar users
        user_id = st.sidebar.number_input(
            "User ID",
            min_value=1,
            max_value=ratings['userId'].max(),
            value=1,
            help="Enter a user ID for collaborative filtering"
        )
        
        num_recommendations = st.sidebar.slider(
            "Number of Recommendations",
            min_value=5,
            max_value=50,
            value=10,
            help="How many movies to recommend"
        )
        
        k_similar_users = st.sidebar.number_input(
            "Number of Similar Users",
            min_value=10,
            max_value=500,
            value=100,
            help="How many similar users to consider for recommendations"
        )
    
    elif rec_type == "Hybrid":
        # Hybrid: Can have all filters
        genres = get_available_genres(movies_stats)
        selected_genre = st.sidebar.selectbox(
            "Select Genre",
            ["All"] + genres,
            help="Filter movies by genre"
        )
        
        user_id = st.sidebar.number_input(
            "User ID",
            min_value=1,
            max_value=ratings['userId'].max(),
            value=1,
            help="Enter a user ID for hybrid recommendations"
        )
        
        num_recommendations = st.sidebar.slider(
            "Number of Recommendations",
            min_value=5,
            max_value=50,
            value=10,
            help="How many movies to recommend"
        )
        
        min_reviews = st.sidebar.number_input(
            "Minimum Reviews Threshold",
            min_value=1,
            max_value=1000,
            value=50,
            help="Minimum number of reviews required for a movie to be considered"
        )
        
        k_similar_users = st.sidebar.number_input(
            "Number of Similar Users",
            min_value=10,
            max_value=500,
            value=100,
            help="How many similar users to consider for collaborative part"
        )
    
    # Generate recommendations button
    if st.sidebar.button("🎬 Get Recommendations", type="primary"):
        try:
            recommendations = None
            
            # Initialize recommender based on type
            if rec_type == "Popularity-Based":
                with st.spinner("🔥 Analyzing movie popularity trends..."):
                    recommender = PopularityRecommender(movies_stats)
                    genre_filter = None if selected_genre == "All" else selected_genre
                    recommendations = recommender.recommend(genre_filter, min_reviews, num_recommendations)
                st.success(f"✅ Generated {len(recommendations)} popularity-based recommendations")
            
            elif rec_type == "Content-Based":
                with st.spinner("🎭 Analyzing movie content and similarities..."):
                    recommender = ContentBasedRecommender(movies_stats)
                    recommendations = recommender.recommend(movie_title, num_recommendations)
                st.success(f"✅ Generated {len(recommendations)} content-based recommendations")
            
            elif rec_type == "Collaborative Filtering":
                with st.spinner("👥 Analyzing user preferences and finding similar users..."):
                    # Correct order: ratings_df first, then movies_df
                    recommender = CollaborativeFilteringRecommender(ratings, movies_stats)
                    recommendations = recommender.recommend(user_id, num_recommendations, k_similar_users)
                st.success(f"✅ Generated {len(recommendations)} collaborative filtering recommendations")
            
            elif rec_type == "Hybrid":
                with st.spinner("🚀 Combining multiple AI algorithms for best results..."):
                    # HybridRecommender needs individual recommender instances
                    popularity_rec = PopularityRecommender(movies_stats)
                    content_rec = ContentBasedRecommender(movies)
                    collab_rec = CollaborativeFilteringRecommender(ratings, movies_stats)
                    recommender = HybridRecommender(popularity_rec, content_rec, collab_rec)
                    recommendations = recommender.get_combined_recommendations(user_id, num_recommendations)
                st.success(f"✅ Generated {len(recommendations)} hybrid recommendations")
            
            # Store recommendations in session state
            if recommendations is not None and not recommendations.empty:
                st.session_state.recommendations = recommendations
                st.session_state.rec_type = rec_type
                st.balloons()  # Celebration animation
            else:
                st.warning("No recommendations generated. Try different parameters.")
            
        except Exception as e:
            st.error(f"❌ Error generating recommendations: {str(e)}")
            st.error("Please try different parameters or contact support.")
            import traceback
            st.code(traceback.format_exc(), language="python")
    
    # Display recommendations if available
    if hasattr(st.session_state, 'recommendations') and not st.session_state.recommendations.empty:
        recommendations = st.session_state.recommendations
        rec_type = st.session_state.rec_type
        
        # Main content area with professional tabs
        tab1, tab2, tab3 = st.tabs([
            "🎬  Movie Recommendations  🎬", 
            "📊  Analytics Dashboard  📊", 
            "📋  Detailed View  📋"
        ])
        
        with tab1:
            display_recommendations_grid(
                recommendations, 
                f"🎯 {rec_type} Recommendations"
            )
        
        with tab2:
            create_analytics_dashboard(movies_stats, recommendations)
        
        with tab3:
            st.markdown("### 📋 Detailed Recommendations Table")
            
            # Style the dataframe
            styled_df = recommendations.style.set_properties(**{
                'background-color': '#2d2d2d',
                'color': 'white',
                'border-color': '#444'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#e50914'), ('color', 'white')]}
            ])
            
            st.dataframe(styled_df, width='stretch')
            
            # Download button
            csv = recommendations.to_csv(index=False)
            st.download_button(
                label="📥 Download Recommendations as CSV",
                data=csv,
                file_name=f"{rec_type.lower()}_recommendations.csv",
                mime="text/csv"
            )
    
    else:
        # Welcome section when no recommendations yet
        st.markdown("## 🌟 Welcome to My Next Movies!")
        
        st.markdown("""
        This AI-powered recommendation system offers four different algorithms to help you discover your next favorite movie:
        """)
        
        # Create feature cards in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔥 Popularity-Based**  
            Get the most popular movies by genre and rating
            
            **🎭 Content-Based**  
            Find movies similar to ones you already love
            """)
        
        with col2:
            st.markdown("""
            **👥 Collaborative Filtering**  
            Get recommendations based on users with similar tastes
            
            **🚀 Hybrid**  
            Combines multiple approaches for the best results
            """)
        
        st.markdown("---")
        st.markdown("**👈 Use the sidebar to configure your preferences and get started!**")
        
        # Show some sample popular movies
        try:
            # Use correct column name for sorting
            rating_col = 'avg_rating' if 'avg_rating' in movies_stats.columns else 'Average Movie Rating'
            sample_popular = movies_stats.nlargest(6, rating_col)
            st.markdown("### 🏆 Top Rated Movies (Sample)")
            display_recommendations_grid(sample_popular, "Highest Rated Movies")
        except Exception as e:
            st.info("Sample movies will be displayed after the first recommendation request.")

if __name__ == "__main__":
    main()
