"""
Recommendation Engine Module for MyNextMovie

This module implements three types of recommendation systems:
1. Popularity-based recommender
2. Content-based recommender
3. Collaborative filtering recommender
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class PopularityRecommender:
    """Popularity-based movie recommendation system"""
    
    def __init__(self, movies_with_stats: pd.DataFrame):
        """
        Initialize popularity recommender
        
        Args:
            movies_with_stats (pd.DataFrame): Movies dataframe with statistics
        """
        self.movies_with_stats = movies_with_stats
        
    def recommend(self, genre: str, min_reviews_threshold: int, num_recommendations: int) -> pd.DataFrame:
        """
        Recommend top N popular movies within a specific genre
        
        Args:
            genre (str): Genre to filter movies
            min_reviews_threshold (int): Minimum number of reviews required
            num_recommendations (int): Number of recommendations to return
            
        Returns:
            pd.DataFrame: Top N movies with S.No., Movie Title, Average Rating, and Num Reviews
        """
        # Filter movies by genre
        if genre and isinstance(genre, str):
            # Filter by genre if specified
            genre_movies = self.movies_with_stats[
                self.movies_with_stats['genres'].str.contains(genre, case=False, na=False)
            ]
        else:
            # No genre filter - use all movies
            genre_movies = self.movies_with_stats.copy()
        
        # Filter by minimum reviews threshold
        popular_movies = genre_movies[genre_movies['num_ratings'] >= min_reviews_threshold]
        
        if len(popular_movies) == 0:
            return pd.DataFrame(columns=['S.No.', 'Movie Title', 'Average Movie Rating', 'Num Reviews'])
        
        # Sort by average rating (descending) and then by number of ratings (descending)
        popular_movies = popular_movies.sort_values(['avg_rating', 'num_ratings'], ascending=[False, False])
        
        # Select top N recommendations
        top_movies = popular_movies.head(num_recommendations)
        
        # Create result dataframe
        result = pd.DataFrame({
            'S.No.': range(1, len(top_movies) + 1),
            'Movie Title': top_movies['title'].values,
            'Average Movie Rating': top_movies['avg_rating'].values,
            'Num Reviews': top_movies['num_ratings'].astype(int).values,
            'year': top_movies['year'].values if 'year' in top_movies.columns else [None] * len(top_movies),
            'genres': top_movies['genres'].values if 'genres' in top_movies.columns else ['N/A'] * len(top_movies)
        })
        
        return result


class ContentBasedRecommender:
    """Content-based movie recommendation system using genre similarity"""
    
    def __init__(self, movies_df: pd.DataFrame):
        """
        Initialize content-based recommender
        
        Args:
            movies_df (pd.DataFrame): Movies dataframe
        """
        self.movies_df = movies_df
        self.movies_expanded = None
        self.genre_columns = None
        self._prepare_genre_features()
        
    def _prepare_genre_features(self) -> None:
        """Prepare genre features for similarity calculation"""
        # Get all unique genres
        all_genres_set = set()
        for genres_str in self.movies_df['genres'].dropna():
            genres = genres_str.split('|')
            all_genres_set.update(genres)
        
        # Create binary columns for each genre
        self.movies_expanded = self.movies_df.copy()
        for genre in all_genres_set:
            self.movies_expanded[f'genre_{genre}'] = self.movies_expanded['genres'].str.contains(genre, na=False).astype(int)
        
        self.genre_columns = [col for col in self.movies_expanded.columns if col.startswith('genre_')]
        
    def recommend(self, movie_title: str, num_recommendations: int) -> pd.DataFrame:
        """
        Recommend movies similar to a given movie based on genre similarity
        
        Args:
            movie_title (str): Title of the input movie (without year)
            num_recommendations (int): Number of recommendations to return
            
        Returns:
            pd.DataFrame: Top N similar movies with S.No. and Movie Titles
        """
        # Clean the input movie title (remove year if present)
        clean_input_title = movie_title
        if '(' in clean_input_title and ')' in clean_input_title:
            clean_input_title = clean_input_title.split('(')[0].strip()
        
        # Find the movie in the dataset (case-insensitive partial matching)
        # First try exact match
        movie_matches = self.movies_expanded[
            self.movies_expanded['title'].str.contains(f'^{clean_input_title}$', case=False, na=False, regex=True)
        ]
        
        # If no exact match, try partial match
        if len(movie_matches) == 0:
            movie_matches = self.movies_expanded[
                self.movies_expanded['title'].str.contains(clean_input_title, case=False, na=False)
            ]
        
        if len(movie_matches) == 0:
            print(f"Movie '{movie_title}' not found in the dataset.")
            return pd.DataFrame(columns=['S.No.', 'Movie Title'])
        
        # If multiple matches, take the first one
        input_movie = movie_matches.iloc[0]
        input_movie_id = input_movie['movieId']
        
        print(f"Found movie: {input_movie['title']}")
        print(f"Genres: {input_movie['genres']}")
        
        # Get genre features for the input movie
        input_features = input_movie[self.genre_columns].values.reshape(1, -1)
        
        # Calculate similarity with all other movies
        all_features = self.movies_expanded[self.genre_columns].values
        similarity_scores = cosine_similarity(input_features, all_features).flatten()
        
        # Create similarity dataframe
        similarity_df = pd.DataFrame({
            'movieId': self.movies_expanded['movieId'],
            'title': self.movies_expanded['title'],
            'genres': self.movies_expanded['genres'],
            'year': self.movies_expanded['year'] if 'year' in self.movies_expanded.columns else [None] * len(self.movies_expanded),
            'avg_rating': self.movies_expanded['avg_rating'] if 'avg_rating' in self.movies_expanded.columns else [0] * len(self.movies_expanded),
            'num_ratings': self.movies_expanded['num_ratings'] if 'num_ratings' in self.movies_expanded.columns else [0] * len(self.movies_expanded),
            'similarity': similarity_scores
        })
        
        # Remove the input movie itself
        similarity_df = similarity_df[similarity_df['movieId'] != input_movie_id]
        
        # Sort by similarity score (descending)
        similarity_df = similarity_df.sort_values('similarity', ascending=False)
        
        # Select top N recommendations
        top_similar = similarity_df.head(num_recommendations)
        
        # Create result dataframe
        result = pd.DataFrame({
            'S.No.': range(1, len(top_similar) + 1),
            'Movie Title': top_similar['title'].values,
            'year': top_similar['year'].values,
            'genres': top_similar['genres'].values,
            'Average Movie Rating': top_similar['avg_rating'].values,
            'Num Reviews': top_similar['num_ratings'].values
        })
        
        return result


class CollaborativeFilteringRecommender:
    """Collaborative filtering recommendation system using user-based approach"""
    
    def __init__(self, ratings_df: pd.DataFrame, movies_df: pd.DataFrame):
        """
        Initialize collaborative filtering recommender
        
        Args:
            ratings_df (pd.DataFrame): Ratings dataframe
            movies_df (pd.DataFrame): Movies dataframe
        """
        self.ratings_df = ratings_df
        self.movies_df = movies_df
        self.user_movie_matrix = None
        self.user_movie_matrix_filled = None
        self._prepare_user_movie_matrix()
        
    def _prepare_user_movie_matrix(self) -> None:
        """Prepare user-movie rating matrix"""
        # Handle different possible column names for rating
        rating_col = None
        for col in ['rating', "'rating'", '"rating"', 'Rating']:
            if col in self.ratings_df.columns:
                rating_col = col
                break
        
        if rating_col is None:
            raise KeyError(f"No rating column found. Available columns: {self.ratings_df.columns.tolist()}")
        
        # Handle different possible column names for userId and movieId
        user_col = None
        for col in ['userId', "'userId'", '"userId"', 'user_id', 'UserID']:
            if col in self.ratings_df.columns:
                user_col = col
                break
                
        movie_col = None
        for col in ['movieId', "'movieId'", '"movieId"', 'movie_id', 'MovieID']:
            if col in self.ratings_df.columns:
                movie_col = col
                break
        
        if user_col is None or movie_col is None:
            raise KeyError(f"Required columns not found. Available: {self.ratings_df.columns.tolist()}")
        
        self.user_movie_matrix = self.ratings_df.pivot_table(
            index=user_col, 
            columns=movie_col, 
            values=rating_col
        )
        self.user_movie_matrix_filled = self.user_movie_matrix.fillna(0)
        
    def recommend(self, user_id: int, num_recommendations: int, k_similar_users: int = 100) -> pd.DataFrame:
        """
        Recommend movies based on K similar users for a target user
        
        Args:
            user_id (int): Target user ID
            num_recommendations (int): Number of recommendations to return
            k_similar_users (int): Number of similar users to consider
            
        Returns:
            pd.DataFrame: Top N movie recommendations with S.No. and Movie Titles
        """
        # Check if user exists
        if user_id not in self.user_movie_matrix.index:
            print(f"User {user_id} not found in the dataset.")
            return pd.DataFrame(columns=['S.No.', 'Movie Title'])
        
        # Get the target user's ratings
        target_user_ratings = self.user_movie_matrix_filled.loc[user_id].values.reshape(1, -1)
        
        # Calculate similarity with all other users
        user_similarities = cosine_similarity(target_user_ratings, self.user_movie_matrix_filled.values).flatten()
        
        # Create similarity dataframe
        similarity_df = pd.DataFrame({
            'userId': self.user_movie_matrix_filled.index,
            'similarity': user_similarities
        })
        
        # Remove the target user and sort by similarity
        similarity_df = similarity_df[similarity_df['userId'] != user_id]
        similarity_df = similarity_df.sort_values('similarity', ascending=False)
        
        # Get top K similar users
        top_k_users = similarity_df.head(k_similar_users)['userId'].values
        
        print(f"Found {len(top_k_users)} similar users for User {user_id}")
        print(f"Top 5 similar users: {top_k_users[:5]}")
        
        # Get movies that the target user hasn't rated
        target_user_rated_movies = self.user_movie_matrix.loc[user_id].dropna().index
        all_movies = set(self.user_movie_matrix.columns)
        unrated_movies = list(all_movies - set(target_user_rated_movies))
        
        # Calculate weighted average ratings for unrated movies
        movie_scores = {}
        
        for movie_id in unrated_movies:
            # Get ratings from similar users for this movie
            similar_users_ratings = []
            similar_users_similarities = []
            
            for sim_user_id in top_k_users:
                if movie_id in self.user_movie_matrix.columns and sim_user_id in self.user_movie_matrix.index:
                    rating = self.user_movie_matrix.loc[sim_user_id, movie_id]
                    if pd.notna(rating):  # If the similar user has rated this movie
                        user_sim = similarity_df[similarity_df['userId'] == sim_user_id]['similarity'].iloc[0]
                        similar_users_ratings.append(rating)
                        similar_users_similarities.append(user_sim)
            
            # Calculate weighted average if we have ratings
            if len(similar_users_ratings) > 0:
                # Check if all weights are zero
                if sum(similar_users_similarities) == 0:
                    # Use simple average if all similarities are zero
                    weighted_rating = np.mean(similar_users_ratings)
                else:
                    weighted_rating = np.average(similar_users_ratings, weights=similar_users_similarities)
                movie_scores[movie_id] = weighted_rating
        
        if len(movie_scores) == 0:
            print("No recommendations could be generated.")
            return pd.DataFrame(columns=['S.No.', 'Movie Title'])
        
        # Sort movies by predicted rating
        sorted_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top N recommendations
        top_movie_ids = [movie_id for movie_id, score in sorted_movies[:num_recommendations]]
        
        # Get movie titles
        recommended_movies = self.movies_df[self.movies_df['movieId'].isin(top_movie_ids)]
        
        # Preserve the order of recommendations
        recommended_movies = recommended_movies.set_index('movieId').loc[top_movie_ids].reset_index()
        
        # Create result dataframe
        result = pd.DataFrame({
            'S.No.': range(1, len(recommended_movies) + 1),
            'Movie Title': recommended_movies['title'].values,
            'year': recommended_movies['year'].values if 'year' in recommended_movies.columns else [None] * len(recommended_movies),
            'genres': recommended_movies['genres'].values if 'genres' in recommended_movies.columns else ['N/A'] * len(recommended_movies),
            'Average Movie Rating': recommended_movies['avg_rating'].values if 'avg_rating' in recommended_movies.columns else [0] * len(recommended_movies),
            'Num Reviews': recommended_movies['num_ratings'].values if 'num_ratings' in recommended_movies.columns else [0] * len(recommended_movies)
        })
        
        return result


class HybridRecommender:
    """Hybrid recommendation system combining multiple approaches"""
    
    def __init__(self, popularity_rec: PopularityRecommender, 
                 content_rec: ContentBasedRecommender, 
                 collaborative_rec: CollaborativeFilteringRecommender):
        """
        Initialize hybrid recommender
        
        Args:
            popularity_rec: Popularity-based recommender instance
            content_rec: Content-based recommender instance
            collaborative_rec: Collaborative filtering recommender instance
        """
        self.popularity_rec = popularity_rec
        self.content_rec = content_rec
        self.collaborative_rec = collaborative_rec
        
    def recommend(self, method: str, **kwargs) -> pd.DataFrame:
        """
        Unified interface for all recommendation methods
        
        Args:
            method (str): 'popularity', 'content', or 'collaborative'
            **kwargs: Method-specific arguments
            
        Returns:
            pd.DataFrame: Recommendations based on the specified method
        """
        if method.lower() == 'popularity':
            required_args = ['genre', 'min_reviews_threshold', 'num_recommendations']
            if not all(arg in kwargs for arg in required_args):
                raise ValueError(f"Missing required arguments for popularity-based recommender: {required_args}")
            
            return self.popularity_rec.recommend(
                kwargs['genre'], 
                kwargs['min_reviews_threshold'], 
                kwargs['num_recommendations']
            )
        
        elif method.lower() == 'content':
            required_args = ['movie_title', 'num_recommendations']
            if not all(arg in kwargs for arg in required_args):
                raise ValueError(f"Missing required arguments for content-based recommender: {required_args}")
            
            return self.content_rec.recommend(
                kwargs['movie_title'], 
                kwargs['num_recommendations']
            )
        
        elif method.lower() == 'collaborative':
            required_args = ['user_id', 'num_recommendations']
            if not all(arg in kwargs for arg in required_args):
                raise ValueError(f"Missing required arguments for collaborative filtering recommender: {required_args}")
            
            k_similar_users = kwargs.get('k_similar_users', 100)
            return self.collaborative_rec.recommend(
                kwargs['user_id'], 
                kwargs['num_recommendations'], 
                k_similar_users
            )
        
        else:
            raise ValueError("Invalid recommendation method. Choose from: 'popularity', 'content', 'collaborative'")
    
    def get_combined_recommendations(self, user_id: int, num_recommendations: int, 
                                   weights: Dict[str, float] = None) -> pd.DataFrame:
        """
        Get combined recommendations from multiple methods
        
        Args:
            user_id (int): Target user ID
            num_recommendations (int): Number of recommendations to return
            weights (Dict[str, float]): Weights for combining different methods
            
        Returns:
            pd.DataFrame: Combined recommendations
        """
        if weights is None:
            weights = {'collaborative': 0.6, 'popularity': 0.4}
        
        # Get collaborative recommendations
        collab_recs = self.collaborative_rec.recommend(user_id, num_recommendations * 2)
        
        # Get popular movies (assuming user likes popular content)
        # This is a simplified approach - in practice, you'd use user's genre preferences
        pop_recs = self.popularity_rec.recommend('Drama', 20, num_recommendations * 2)
        
        # Simple weighted combination (this could be more sophisticated)
        combined_movies = []
        
        # Add collaborative recommendations with weight
        if not collab_recs.empty:
            for _, row in collab_recs.iterrows():
                combined_movies.append({
                    'title': row['Movie Title'],
                    'year': row.get('year', ''),
                    'genres': row.get('genres', 'N/A'),
                    'avg_rating': row.get('Average Movie Rating', 0),
                    'num_reviews': row.get('Num Reviews', 0),
                    'score': weights.get('collaborative', 0.6),
                    'source': 'collaborative'
                })
        
        # Add popularity recommendations with weight
        if not pop_recs.empty:
            for _, row in pop_recs.iterrows():
                combined_movies.append({
                    'title': row['Movie Title'],
                    'year': row.get('year', ''),
                    'genres': row.get('genres', 'N/A'),
                    'avg_rating': row.get('Average Movie Rating', 0),
                    'num_reviews': row.get('Num Reviews', 0),
                    'score': weights.get('popularity', 0.4),
                    'source': 'popularity'
                })
        
        # Remove duplicates and sort by score
        seen_titles = set()
        unique_movies = []
        for movie in combined_movies:
            if movie['title'] not in seen_titles:
                unique_movies.append(movie)
                seen_titles.add(movie['title'])
        
        # Sort by score and take top N
        unique_movies.sort(key=lambda x: x['score'], reverse=True)
        top_movies = unique_movies[:num_recommendations]
        
        # Create result dataframe
        result = pd.DataFrame({
            'S.No.': range(1, len(top_movies) + 1),
            'Movie Title': [movie['title'] for movie in top_movies],
            'year': [movie['year'] for movie in top_movies],
            'genres': [movie['genres'] for movie in top_movies],
            'Average Movie Rating': [movie['avg_rating'] for movie in top_movies],
            'Num Reviews': [movie['num_reviews'] for movie in top_movies]
        })
        
        return result
