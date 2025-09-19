"""
Unit Tests for MyNextMovie Recommendation System

This module contains comprehensive tests for all recommendation engines.
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import DataLoader
from recommendation_engine import (
    PopularityRecommender,
    ContentBasedRecommender,
    CollaborativeFilteringRecommender,
    HybridRecommender
)

class TestDataLoader(unittest.TestCase):
    """Test cases for DataLoader class"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample data for testing
        self.sample_movies = pd.DataFrame({
            'movieId': [1, 2, 3, 4, 5],
            'title': ['Movie A (2020)', 'Movie B (2019)', 'Movie C (2021)', 'Movie D (2018)', 'Movie E (2022)'],
            'genres': ['Action|Adventure', 'Comedy', 'Drama|Romance', 'Action', 'Comedy|Drama']
        })
        
        self.sample_ratings = pd.DataFrame({
            'userId': [1, 1, 2, 2, 3, 3, 4, 5],
            'movieId': [1, 2, 1, 3, 2, 4, 5, 1],
            'rating': [4.0, 3.5, 5.0, 4.5, 3.0, 4.0, 2.5, 5.0],
            'timestamp': [123456789, 123456790, 123456791, 123456792, 123456793, 123456794, 123456795, 123456796]
        })
    
    def test_create_user_movie_matrix(self):
        """Test user-movie matrix creation"""
        data_loader = DataLoader("dummy_path")
        data_loader.ratings_df = self.sample_ratings
        data_loader._create_user_movie_matrix()
        matrix = data_loader.user_movie_matrix
        
        # Check matrix dimensions
        self.assertEqual(matrix.shape[0], 5)  # 5 unique users
        self.assertEqual(matrix.shape[1], 5)  # 5 unique movies
        
        # Check specific values
        self.assertEqual(matrix.loc[1, 1], 4.0)
        self.assertEqual(matrix.loc[2, 1], 5.0)
    
    def test_expand_genres(self):
        """Test genre expansion"""
        data_loader = DataLoader("dummy_path")
        expanded, genres_list = data_loader.expand_genres(self.sample_movies)
        
        # Check that genre columns are created
        genre_columns = [col for col in expanded.columns if col.startswith('genre_')]
        self.assertGreater(len(genre_columns), 0)
        
        # Check specific genre presence
        self.assertIn('genre_Action', expanded.columns)
        self.assertIn('genre_Comedy', expanded.columns)


class TestPopularityRecommender(unittest.TestCase):
    """Test cases for PopularityRecommender"""
    
    def setUp(self):
        """Set up test data"""
        self.movies_with_stats = pd.DataFrame({
            'movieId': [1, 2, 3, 4, 5],
            'title': ['Action Movie A', 'Comedy Movie B', 'Drama Movie C', 'Action Movie D', 'Romance Movie E'],
            'genres': ['Action', 'Comedy', 'Drama', 'Action', 'Romance'],
            'avg_rating': [4.5, 3.8, 4.2, 4.0, 3.5],
            'num_ratings': [100, 50, 80, 120, 30]
        })
        
        self.recommender = PopularityRecommender(self.movies_with_stats)
    
    def test_popularity_recommendations(self):
        """Test popularity-based recommendations"""
        # Test normal case
        recommendations = self.recommender.recommend('Action', 50, 2)
        
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertLessEqual(len(recommendations), 2)
        
        # Check column names
        expected_columns = ['S.No.', 'Movie Title', 'Average Movie Rating', 'Num Reviews']
        self.assertEqual(list(recommendations.columns), expected_columns)
        
        # Test that the first recommendation has higher rating
        if len(recommendations) > 1:
            self.assertGreaterEqual(
                recommendations.iloc[0]['Average Movie Rating'],
                recommendations.iloc[1]['Average Movie Rating']
            )
    
    def test_popularity_no_results(self):
        """Test when no movies meet criteria"""
        recommendations = self.recommender.recommend('Sci-Fi', 50, 5)
        self.assertTrue(recommendations.empty)


class TestContentBasedRecommender(unittest.TestCase):
    """Test cases for ContentBasedRecommender"""
    
    def setUp(self):
        """Set up test data"""
        self.movies_df = pd.DataFrame({
            'movieId': [1, 2, 3, 4, 5],
            'title': ['Action Movie A', 'Action Movie B', 'Comedy Movie C', 'Drama Movie D', 'Comedy Movie E'],
            'genres': ['Action|Adventure', 'Action|Thriller', 'Comedy', 'Drama|Romance', 'Comedy|Romance']
        })
        
        self.recommender = ContentBasedRecommender(self.movies_df)
    
    def test_content_recommendations(self):
        """Test content-based recommendations"""
        recommendations = self.recommender.recommend('Action Movie A', 3)
        
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertLessEqual(len(recommendations), 3)
        
        # Check column names
        expected_columns = ['S.No.', 'Movie Title']
        self.assertEqual(list(recommendations.columns), expected_columns)
    
    def test_content_movie_not_found(self):
        """Test when movie is not found"""
        recommendations = self.recommender.recommend('Non-existent Movie', 3)
        self.assertTrue(recommendations.empty)


class TestCollaborativeFilteringRecommender(unittest.TestCase):
    """Test cases for CollaborativeFilteringRecommender"""
    
    def setUp(self):
        """Set up test data"""
        self.ratings_df = pd.DataFrame({
            'userId': [1, 1, 2, 2, 3, 3, 4, 5] * 3,
            'movieId': [1, 2, 1, 3, 2, 4, 5, 1] * 3,
            'rating': [4.0, 3.5, 5.0, 4.5, 3.0, 4.0, 2.5, 5.0] * 3,
            'timestamp': list(range(24))
        })
        
        self.movies_df = pd.DataFrame({
            'movieId': [1, 2, 3, 4, 5],
            'title': ['Movie A', 'Movie B', 'Movie C', 'Movie D', 'Movie E'],
            'genres': ['Action', 'Comedy', 'Drama', 'Action', 'Romance']
        })
        
        self.recommender = CollaborativeFilteringRecommender(self.ratings_df, self.movies_df)
    
    def test_collaborative_recommendations(self):
        """Test collaborative filtering recommendations"""
        recommendations = self.recommender.recommend(1, 3)
        
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertLessEqual(len(recommendations), 3)
        
        # Check column names
        expected_columns = ['S.No.', 'Movie Title']
        self.assertEqual(list(recommendations.columns), expected_columns)
    
    def test_collaborative_user_not_found(self):
        """Test when user is not found"""
        recommendations = self.recommender.recommend(999, 3)
        self.assertTrue(recommendations.empty)


class TestHybridRecommender(unittest.TestCase):
    """Test cases for HybridRecommender"""
    
    def setUp(self):
        """Set up test data and recommenders"""
        # Create sample data
        self.movies_with_stats = pd.DataFrame({
            'movieId': [1, 2, 3, 4, 5],
            'title': ['Action Movie A', 'Comedy Movie B', 'Drama Movie C', 'Action Movie D', 'Romance Movie E'],
            'genres': ['Action', 'Comedy', 'Drama', 'Action', 'Romance'],
            'avg_rating': [4.5, 3.8, 4.2, 4.0, 3.5],
            'num_ratings': [100, 50, 80, 120, 30]
        })
        
        self.movies_df = pd.DataFrame({
            'movieId': [1, 2, 3, 4, 5],
            'title': ['Action Movie A', 'Comedy Movie B', 'Drama Movie C', 'Action Movie D', 'Romance Movie E'],
            'genres': ['Action', 'Comedy', 'Drama', 'Action', 'Romance']
        })
        
        self.ratings_df = pd.DataFrame({
            'userId': [1, 1, 2, 2, 3, 3, 4, 5] * 2,
            'movieId': [1, 2, 1, 3, 2, 4, 5, 1] * 2,
            'rating': [4.0, 3.5, 5.0, 4.5, 3.0, 4.0, 2.5, 5.0] * 2,
            'timestamp': list(range(16))
        })
        
        # Initialize recommenders
        self.pop_rec = PopularityRecommender(self.movies_with_stats)
        self.content_rec = ContentBasedRecommender(self.movies_df)
        self.collab_rec = CollaborativeFilteringRecommender(self.ratings_df, self.movies_df)
        
        self.hybrid_rec = HybridRecommender(self.pop_rec, self.content_rec, self.collab_rec)
    
    def test_hybrid_popularity_method(self):
        """Test hybrid recommender with popularity method"""
        recommendations = self.hybrid_rec.recommend(
            'popularity',
            genre='Action',
            min_reviews_threshold=50,
            num_recommendations=2
        )
        
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertLessEqual(len(recommendations), 2)
    
    def test_hybrid_content_method(self):
        """Test hybrid recommender with content method"""
        recommendations = self.hybrid_rec.recommend(
            'content',
            movie_title='Action Movie A',
            num_recommendations=2
        )
        
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertLessEqual(len(recommendations), 2)
    
    def test_hybrid_collaborative_method(self):
        """Test hybrid recommender with collaborative method"""
        recommendations = self.hybrid_rec.recommend(
            'collaborative',
            user_id=1,
            num_recommendations=2
        )
        
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertLessEqual(len(recommendations), 2)
    
    def test_hybrid_invalid_method(self):
        """Test hybrid recommender with invalid method"""
        with self.assertRaises(ValueError):
            self.hybrid_rec.recommend('invalid_method')
    
    def test_hybrid_missing_arguments(self):
        """Test hybrid recommender with missing arguments"""
        with self.assertRaises(ValueError):
            self.hybrid_rec.recommend('popularity', genre='Action')  # Missing required args


class TestRecommendationIntegration(unittest.TestCase):
    """Integration tests for the complete recommendation system"""
    
    def setUp(self):
        """Set up integration test data"""
        # Create a more comprehensive dataset
        np.random.seed(42)
        
        # Movies data
        movie_ids = list(range(1, 21))  # 20 movies
        titles = [f'Movie {i}' for i in movie_ids]
        genres_list = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance']
        genres = [np.random.choice(genres_list) for _ in movie_ids]
        
        self.movies_df = pd.DataFrame({
            'movieId': movie_ids,
            'title': titles,
            'genres': genres
        })
        
        # Ratings data
        user_ids = []
        movie_ids_ratings = []
        ratings = []
        timestamps = []
        
        for user_id in range(1, 11):  # 10 users
            for movie_id in np.random.choice(movie_ids, size=np.random.randint(5, 15), replace=False):
                user_ids.append(user_id)
                movie_ids_ratings.append(movie_id)
                ratings.append(np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.1, 0.2, 0.3, 0.3]))
                timestamps.append(np.random.randint(1000000, 2000000))
        
        self.ratings_df = pd.DataFrame({
            'userId': user_ids,
            'movieId': movie_ids_ratings,
            'rating': ratings,
            'timestamp': timestamps
        })
        
        # Create movies with stats
        rating_stats = self.ratings_df.groupby('movieId').agg({
            'rating': ['mean', 'count']
        }).round(2)
        rating_stats.columns = ['avg_rating', 'num_ratings']
        rating_stats = rating_stats.reset_index()
        
        self.movies_with_stats = self.movies_df.merge(rating_stats, on='movieId', how='left')
        self.movies_with_stats['avg_rating'] = self.movies_with_stats['avg_rating'].fillna(0)
        self.movies_with_stats['num_ratings'] = self.movies_with_stats['num_ratings'].fillna(0)
    
    def test_full_system_integration(self):
        """Test that all recommenders work together"""
        # Initialize all recommenders
        pop_rec = PopularityRecommender(self.movies_with_stats)
        content_rec = ContentBasedRecommender(self.movies_df)
        collab_rec = CollaborativeFilteringRecommender(self.ratings_df, self.movies_df)
        hybrid_rec = HybridRecommender(pop_rec, content_rec, collab_rec)
        
        # Test each recommender
        pop_recs = pop_rec.recommend('Action', 2, 3)
        self.assertIsInstance(pop_recs, pd.DataFrame)
        
        content_recs = content_rec.recommend('Movie 1', 3)
        self.assertIsInstance(content_recs, pd.DataFrame)
        
        collab_recs = collab_rec.recommend(1, 3)
        self.assertIsInstance(collab_recs, pd.DataFrame)
        
        # Test hybrid recommender
        hybrid_recs = hybrid_rec.get_combined_recommendations(1, 3)
        self.assertIsInstance(hybrid_recs, pd.DataFrame)


if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestDataLoader,
        TestPopularityRecommender,
        TestContentBasedRecommender,
        TestCollaborativeFilteringRecommender,
        TestHybridRecommender,
        TestRecommendationIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"TESTS SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print(f"\n🎉 All tests passed successfully!")
    else:
        print(f"\n❌ Some tests failed. Please check the output above.")
