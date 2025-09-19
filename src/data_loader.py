"""
Data Loader Module for MyNextMovie Recommendation System

This module handles loading and preprocessing of movie and rating data.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict
import os

class DataLoader:
    """Handles loading and preprocessing of movie recommendation data"""
    
    def __init__(self, data_path: str = "../data/raw"):
        """
        Initialize DataLoader with data path
        
        Args:
            data_path (str): Path to raw data directory
        """
        self.data_path = data_path
        self.movies_df = None
        self.ratings_df = None
        self.movies_with_stats = None
        self.user_movie_matrix = None
        self.unique_genres = None
        
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load movies and ratings datasets
        
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Movies and ratings dataframes
        """
        try:
            movies_path = os.path.join(self.data_path, "movies.csv")
            ratings_path = os.path.join(self.data_path, "ratings.csv")
            
            self.movies_df = pd.read_csv(movies_path)
            self.ratings_df = pd.read_csv(ratings_path)
            
            # Clean column names (remove any extra quotes or whitespace)
            self.movies_df.columns = self.movies_df.columns.str.strip().str.strip("'\"")
            self.ratings_df.columns = self.ratings_df.columns.str.strip().str.strip("'\"")
            
            # Separate movie title and year
            self.movies_df = self._separate_title_and_year(self.movies_df)
            
            print(f"Movies loaded: {self.movies_df.shape[0]} records")
            print(f"Ratings loaded: {self.ratings_df.shape[0]} records")
            
            return self.movies_df, self.ratings_df
            
        except FileNotFoundError as e:
            print(f"Error loading data: {e}")
            raise
    
    def _separate_title_and_year(self, movies_df: pd.DataFrame) -> pd.DataFrame:
        """
        Separate movie title and year into different columns
        
        Args:
            movies_df (pd.DataFrame): Movies dataframe with combined title
            
        Returns:
            pd.DataFrame: Movies dataframe with separate title and year columns
        """
        movies_df = movies_df.copy()
        
        # Extract year from title (pattern: "Movie Title (YYYY)")
        movies_df['year'] = movies_df['title'].str.extract(r'\((\d{4})\)$').astype('Int64')
        
        # Remove year from title to get clean movie name
        movies_df['movie_name'] = movies_df['title'].str.replace(r'\s*\(\d{4}\)$', '', regex=True)
        
        # Keep original title for backward compatibility
        movies_df['original_title'] = movies_df['title']
        
        # Update title to be the clean movie name
        movies_df['title'] = movies_df['movie_name']
        
        return movies_df
            
    def preprocess_data(self) -> pd.DataFrame:
        """
        Preprocess data for recommendation systems
        
        Returns:
            pd.DataFrame: Movies dataframe with statistics
        """
        if self.movies_df is None or self.ratings_df is None:
            raise ValueError("Data must be loaded first using load_data()")
            
        # Create movie statistics
        self._create_movie_statistics()
        
        # Create user-movie matrix
        self._create_user_movie_matrix()
        
        # Extract unique genres
        self._extract_unique_genres()
        
        print("Data preprocessing completed successfully!")
        
        return self.movies_with_stats
        
    def _create_movie_statistics(self) -> None:
        """Create movie statistics including average rating and count"""
        movie_stats = self.ratings_df.groupby('movieId').agg({
            'rating': ['mean', 'count', 'std']
        }).round(2)
        
        # Flatten column names
        movie_stats.columns = ['avg_rating', 'num_ratings', 'rating_std']
        movie_stats = movie_stats.reset_index()
        
        # Merge with movies dataframe
        self.movies_with_stats = self.movies_df.merge(movie_stats, on='movieId', how='left')
        self.movies_with_stats = self.movies_with_stats.fillna(0)
        
    def _create_user_movie_matrix(self) -> None:
        """Create user-movie rating matrix for collaborative filtering"""
        self.user_movie_matrix = self.ratings_df.pivot_table(
            index='userId', 
            columns='movieId', 
            values='rating'
        )
        
    def _extract_unique_genres(self) -> None:
        """Extract unique genres from movies dataset"""
        all_genres = []
        for genres_str in self.movies_df['genres'].dropna():
            genres = genres_str.split('|')
            all_genres.extend(genres)
        
        self.unique_genres = list(set(all_genres))
        
    def expand_genres(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Expand the genres column into separate binary columns for each genre
        
        Args:
            df (pd.DataFrame): Movies dataframe
            
        Returns:
            Tuple[pd.DataFrame, List[str]]: Expanded dataframe and unique genres list
        """
        # Get all unique genres
        all_genres_set = set()
        for genres_str in df['genres'].dropna():
            genres = genres_str.split('|')
            all_genres_set.update(genres)
        
        # Create binary columns for each genre
        df_expanded = df.copy()
        for genre in all_genres_set:
            df_expanded[f'genre_{genre}'] = df_expanded['genres'].str.contains(genre, na=False).astype(int)
        
        return df_expanded, list(all_genres_set)
    
    def get_data_summary(self) -> Dict[str, any]:
        """
        Get summary statistics of the loaded data
        
        Returns:
            Dict[str, any]: Summary statistics
        """
        if self.movies_df is None or self.ratings_df is None:
            raise ValueError("Data must be loaded first using load_data()")
            
        summary = {
            'total_movies': self.movies_df['movieId'].nunique(),
            'total_users': self.ratings_df['userId'].nunique(),
            'total_ratings': len(self.ratings_df),
            'average_rating': self.ratings_df['rating'].mean(),
            'min_rating': self.ratings_df['rating'].min(),
            'max_rating': self.ratings_df['rating'].max(),
            'unique_genres': len(self.unique_genres) if self.unique_genres else 0,
            'sparsity': (len(self.ratings_df) / (self.movies_df['movieId'].nunique() * self.ratings_df['userId'].nunique())) * 100
        }
        
        return summary
    
    def validate_data(self) -> bool:
        """
        Validate the loaded data for consistency
        
        Returns:
            bool: True if data is valid, False otherwise
        """
        if self.movies_df is None or self.ratings_df is None:
            return False
            
        # Check for missing required columns
        required_movie_cols = ['movieId', 'title', 'genres']
        required_rating_cols = ['userId', 'movieId', 'rating', 'timestamp']
        
        if not all(col in self.movies_df.columns for col in required_movie_cols):
            print("Missing required columns in movies dataset")
            return False
            
        if not all(col in self.ratings_df.columns for col in required_rating_cols):
            print("Missing required columns in ratings dataset")
            return False
            
        # Check for valid movie IDs in both datasets
        movie_ids_in_movies = set(self.movies_df['movieId'])
        movie_ids_in_ratings = set(self.ratings_df['movieId'])
        
        if not movie_ids_in_ratings.issubset(movie_ids_in_movies):
            print("Warning: Some movie IDs in ratings are not in movies dataset")
            
        print("Data validation successful!")
        return True
