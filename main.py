#!/usr/bin/env python3
"""
MyNextMovie Recommendation System - Main Entry Point

This script demonstrates the complete recommendation system functionality.
"""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import DataLoader
from recommendation_engine import (
    PopularityRecommender,
    ContentBasedRecommender, 
    CollaborativeFilteringRecommender,
    HybridRecommender
)


def main():
    """Main function to demonstrate the recommendation system"""
    print("=== MyNextMovie Recommendation System ===")
    
    # Initialize data loader
    print("\n1. Loading data...")
    data_loader = DataLoader('data/raw')
    movies_df, ratings_df = data_loader.load_data()
    
    # Preprocess data
    print("\n2. Preprocessing data...")
    movies_with_stats = data_loader.preprocess_data()
    
    # Initialize recommenders
    print("\n3. Initializing recommendation engines...")
    pop_recommender = PopularityRecommender(movies_with_stats)
    content_recommender = ContentBasedRecommender(movies_df)
    collab_recommender = CollaborativeFilteringRecommender(ratings_df, movies_df)
    hybrid_recommender = HybridRecommender(pop_recommender, content_recommender, collab_recommender)
    
    print("\n4. Testing recommendation systems...")
    
    # Test Popularity-based recommendations
    print("\n--- Popularity-Based Recommendations ---")
    pop_recs = pop_recommender.recommend('Action', 3.5, 5)
    print(f"Top Action movies (min rating 3.5):")
    print(pop_recs)
    
    # Test Content-based recommendations
    print("\n--- Content-Based Recommendations ---")
    content_recs = content_recommender.recommend('Toy Story', 5)
    print(f"Movies similar to 'Toy Story':")
    print(content_recs)
    
    # Test Collaborative filtering recommendations
    print("\n--- Collaborative Filtering Recommendations ---")
    collab_recs = collab_recommender.recommend(1, 5)
    print(f"Recommendations for User 1:")
    print(collab_recs)
    
    print("\n=== System test completed successfully! ===")


if __name__ == "__main__":
    main()
