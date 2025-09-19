"""
Main Application for MyNextMovie Recommendation System

This is the main entry point for the movie recommendation system.
It provides a command-line interface to interact with different recommendation algorithms.
"""

import os
import sys
import pandas as pd
from typing import Optional

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import DataLoader
from recommendation_engine import (
    PopularityRecommender, 
    ContentBasedRecommender, 
    CollaborativeFilteringRecommender, 
    HybridRecommender
)

class MovieRecommendationSystem:
    """Main class for the Movie Recommendation System"""
    
    def __init__(self, data_folder_path: str = "data/raw"):
        """
        Initialize the recommendation system
        
        Args:
            data_folder_path (str): Path to the folder containing CSV files
        """
        self.data_folder_path = data_folder_path
        self.data_loader = None
        self.movies_df = None
        self.ratings_df = None
        self.movies_with_stats = None
        self.recommenders = {}
        self.hybrid_recommender = None
        
        # Initialize the system
        self._initialize_system()
    
    def _initialize_system(self) -> None:
        """Initialize all components of the recommendation system"""
        print("🎬 Initializing MyNextMovie Recommendation System...")
        
        try:
            # Load data
            print("📊 Loading movie and rating data...")
            self.data_loader = DataLoader(self.data_folder_path)
            self.movies_df, self.ratings_df = self.data_loader.load_data()
            
            # Preprocess data
            print("🔄 Preprocessing data...")
            self.movies_with_stats = self.data_loader.preprocess_data()
            
            # Validate data
            print("✅ Validating data...")
            self.data_loader.validate_data()
            
            # Initialize recommenders
            print("🤖 Initializing recommendation engines...")
            self._initialize_recommenders()
            
            print("🎉 System initialized successfully!")
            print(f"📈 Loaded {len(self.movies_df)} movies and {len(self.ratings_df)} ratings")
            
        except Exception as e:
            print(f"❌ Error initializing system: {str(e)}")
            sys.exit(1)
    
    def _initialize_recommenders(self) -> None:
        """Initialize all recommendation engines"""
        # Popularity-based recommender
        self.recommenders['popularity'] = PopularityRecommender(self.movies_with_stats)
        
        # Content-based recommender
        self.recommenders['content'] = ContentBasedRecommender(self.movies_df)
        
        # Collaborative filtering recommender
        self.recommenders['collaborative'] = CollaborativeFilteringRecommender(
            self.ratings_df, self.movies_df
        )
        
        # Hybrid recommender
        self.hybrid_recommender = HybridRecommender(
            self.recommenders['popularity'],
            self.recommenders['content'],
            self.recommenders['collaborative']
        )
    
    def get_popularity_recommendations(self, genre: str, min_reviews: int, num_recs: int) -> pd.DataFrame:
        """
        Get popularity-based recommendations
        
        Args:
            genre (str): Movie genre to filter by
            min_reviews (int): Minimum number of reviews required
            num_recs (int): Number of recommendations
            
        Returns:
            pd.DataFrame: Recommended movies
        """
        print(f"\n🔥 Getting popular {genre} movies with at least {min_reviews} reviews...")
        
        recommendations = self.recommenders['popularity'].recommend(
            genre=genre,
            min_reviews_threshold=min_reviews,
            num_recommendations=num_recs
        )
        
        return recommendations
    
    def get_content_recommendations(self, movie_title: str, num_recs: int) -> pd.DataFrame:
        """
        Get content-based recommendations
        
        Args:
            movie_title (str): Movie title to find similar movies for
            num_recs (int): Number of recommendations
            
        Returns:
            pd.DataFrame: Recommended movies
        """
        print(f"\n🎯 Finding movies similar to '{movie_title}'...")
        
        recommendations = self.recommenders['content'].recommend(
            movie_title=movie_title,
            num_recommendations=num_recs
        )
        
        return recommendations
    
    def get_collaborative_recommendations(self, user_id: int, num_recs: int, k_users: int = 100) -> pd.DataFrame:
        """
        Get collaborative filtering recommendations
        
        Args:
            user_id (int): User ID to get recommendations for
            num_recs (int): Number of recommendations
            k_users (int): Number of similar users to consider
            
        Returns:
            pd.DataFrame: Recommended movies
        """
        print(f"\n👥 Getting personalized recommendations for User {user_id}...")
        
        recommendations = self.recommenders['collaborative'].recommend(
            user_id=user_id,
            num_recommendations=num_recs,
            k_similar_users=k_users
        )
        
        return recommendations
    
    def get_hybrid_recommendations(self, user_id: int, num_recs: int) -> pd.DataFrame:
        """
        Get hybrid recommendations combining multiple methods
        
        Args:
            user_id (int): User ID to get recommendations for
            num_recs (int): Number of recommendations
            
        Returns:
            pd.DataFrame: Recommended movies
        """
        print(f"\n🌟 Getting hybrid recommendations for User {user_id}...")
        
        recommendations = self.hybrid_recommender.get_combined_recommendations(
            user_id=user_id,
            num_recommendations=num_recs
        )
        
        return recommendations
    
    def print_recommendations(self, recommendations: pd.DataFrame, title: str) -> None:
        """
        Print recommendations in a formatted way
        
        Args:
            recommendations (pd.DataFrame): Recommendations to print
            title (str): Title for the recommendations
        """
        print(f"\n{title}")
        print("=" * len(title))
        
        if recommendations.empty:
            print("No recommendations found.")
            return
        
        for _, row in recommendations.iterrows():
            if len(recommendations.columns) == 2:  # Simple format (S.No., Movie Title)
                print(f"{row['S.No.']}. {row['Movie Title']}")
            else:  # Detailed format (with ratings and reviews)
                print(f"{row['S.No.']}. {row['Movie Title']}")
                print(f"   Rating: {row['Average Movie Rating']:.2f} | Reviews: {row['Num Reviews']}")
    
    def get_data_summary(self) -> None:
        """Print a summary of the loaded data"""
        summary = self.data_loader.get_data_summary()
        
        print("\n📊 Data Summary")
        print("=" * 50)
        for key, value in summary.items():
            print(f"{key}: {value}")
    
    def interactive_mode(self) -> None:
        """Run the system in interactive mode"""
        print("\n🎬 Welcome to MyNextMovie Recommendation System!")
        print("Choose your recommendation method:")
        
        while True:
            print("\n" + "="*50)
            print("RECOMMENDATION OPTIONS:")
            print("1. 🔥 Popular Movies by Genre")
            print("2. 🎯 Similar Movies (Content-based)")
            print("3. 👥 Personalized Recommendations (Collaborative)")
            print("4. 🌟 Hybrid Recommendations")
            print("5. 📊 Data Summary")
            print("6. 🚪 Exit")
            print("="*50)
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            try:
                if choice == '1':
                    self._handle_popularity_recommendations()
                elif choice == '2':
                    self._handle_content_recommendations()
                elif choice == '3':
                    self._handle_collaborative_recommendations()
                elif choice == '4':
                    self._handle_hybrid_recommendations()
                elif choice == '5':
                    self.get_data_summary()
                elif choice == '6':
                    print("\n👋 Thank you for using MyNextMovie! Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please enter a number between 1-6.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Thank you for using MyNextMovie! Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {str(e)}")
                print("Please try again.")
    
    def _handle_popularity_recommendations(self) -> None:
        """Handle popularity-based recommendations input"""
        genre = input("Enter genre (e.g., Action, Comedy, Drama): ").strip()
        if not genre:
            print("❌ Genre cannot be empty.")
            return
        
        try:
            min_reviews = int(input("Enter minimum number of reviews (e.g., 20): ").strip())
            num_recs = int(input("Enter number of recommendations (e.g., 10): ").strip())
            
            recommendations = self.get_popularity_recommendations(genre, min_reviews, num_recs)
            self.print_recommendations(recommendations, f"🔥 Popular {genre} Movies")
            
        except ValueError:
            print("❌ Please enter valid numbers for reviews and recommendations.")
    
    def _handle_content_recommendations(self) -> None:
        """Handle content-based recommendations input"""
        movie_title = input("Enter movie title: ").strip()
        if not movie_title:
            print("❌ Movie title cannot be empty.")
            return
        
        try:
            num_recs = int(input("Enter number of recommendations (e.g., 10): ").strip())
            
            recommendations = self.get_content_recommendations(movie_title, num_recs)
            self.print_recommendations(recommendations, f"🎯 Movies Similar to '{movie_title}'")
            
        except ValueError:
            print("❌ Please enter a valid number for recommendations.")
    
    def _handle_collaborative_recommendations(self) -> None:
        """Handle collaborative filtering recommendations input"""
        try:
            user_id = int(input("Enter user ID (e.g., 1): ").strip())
            num_recs = int(input("Enter number of recommendations (e.g., 10): ").strip())
            
            recommendations = self.get_collaborative_recommendations(user_id, num_recs)
            self.print_recommendations(recommendations, f"👥 Personalized Recommendations for User {user_id}")
            
        except ValueError:
            print("❌ Please enter valid numbers for user ID and recommendations.")
    
    def _handle_hybrid_recommendations(self) -> None:
        """Handle hybrid recommendations input"""
        try:
            user_id = int(input("Enter user ID (e.g., 1): ").strip())
            num_recs = int(input("Enter number of recommendations (e.g., 10): ").strip())
            
            recommendations = self.get_hybrid_recommendations(user_id, num_recs)
            self.print_recommendations(recommendations, f"🌟 Hybrid Recommendations for User {user_id}")
            
        except ValueError:
            print("❌ Please enter valid numbers for user ID and recommendations.")


def main():
    """Main function to run the application"""
    # Check if running from correct directory
    if not os.path.exists("data"):
        print("❌ Error: 'data' folder not found.")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    try:
        # Initialize the recommendation system
        rec_system = MovieRecommendationSystem()
        
        # Check if command line arguments are provided
        if len(sys.argv) > 1:
            # Command line mode
            if sys.argv[1].lower() == 'demo':
                run_demo(rec_system)
            else:
                print("Usage: python main.py [demo]")
                print("  demo: Run demonstration with sample recommendations")
        else:
            # Interactive mode
            rec_system.interactive_mode()
            
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)


def run_demo(rec_system: MovieRecommendationSystem):
    """Run a demonstration of all recommendation methods"""
    print("\n🎬 MyNextMovie Recommendation System - DEMO MODE")
    print("="*60)
    
    # Demo 1: Popularity-based recommendations
    print("\n📍 DEMO 1: Popular Action Movies")
    recs = rec_system.get_popularity_recommendations("Action", 50, 5)
    rec_system.print_recommendations(recs, "🔥 Top 5 Popular Action Movies")
    
    # Demo 2: Content-based recommendations
    print("\n📍 DEMO 2: Movies Similar to Toy Story")
    recs = rec_system.get_content_recommendations("Toy Story", 5)
    rec_system.print_recommendations(recs, "🎯 Movies Similar to Toy Story")
    
    # Demo 3: Collaborative filtering recommendations
    print("\n📍 DEMO 3: Personalized Recommendations for User 1")
    recs = rec_system.get_collaborative_recommendations(1, 5)
    rec_system.print_recommendations(recs, "👥 Personalized Recommendations for User 1")
    
    # Demo 4: Data summary
    print("\n📍 DEMO 4: Data Summary")
    rec_system.get_data_summary()
    
    print("\n🎉 Demo completed! Run without 'demo' argument for interactive mode.")


if __name__ == "__main__":
    main()
