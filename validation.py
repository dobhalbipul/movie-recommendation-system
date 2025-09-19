"""
Final Validation Script for MyNextMovie Recommendation System

This script validates all components of the recommendation system including GUI interfaces.
"""

import sys
import os
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🎬 {title}")
    print("="*60)

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (NOT FOUND)")
        return False

def check_directory_structure():
    """Validate the complete project structure"""
    print_header("PROJECT STRUCTURE VALIDATION")
    
    structure = {
        "Main Files": {
            "main.py": "Command Line Interface",
            "gui_app.py": "Desktop GUI Application", 
            "poster_generator.py": "Movie Poster Generator",
            "requirements.txt": "Dependencies List",
            "README.md": "Project Documentation",
            "USAGE_GUIDE.md": "Complete Usage Guide"
        },
        "Data Directory": {
            "data/raw/movies.csv": "Movies Dataset",
            "data/raw/ratings.csv": "Ratings Dataset"
        },
        "Source Code": {
            "src/data_loader.py": "Data Loading Module",
            "src/recommendation_engine.py": "ML Algorithms Module"
        },
        "Notebooks": {
            "notebooks/movie_recommendation_system.ipynb": "Analysis Notebook",
            "notebooks/interactive_gui.ipynb": "Interactive GUI Notebook"
        },
        "Tests": {
            "tests/test_recommenders.py": "Unit Tests"
        },
        "Documentation": {
            "docs/my-next-movie.pdf": "Requirements Document"
        }
    }
    
    all_files_exist = True
    
    for category, files in structure.items():
        print(f"\n📁 {category}:")
        for filepath, description in files.items():
            exists = check_file_exists(filepath, description)
            if not exists:
                all_files_exist = False
    
    return all_files_exist

def test_core_functionality():
    """Test the core recommendation functionality"""
    print_header("CORE FUNCTIONALITY TEST")
    
    try:
        # Add src to path
        sys.path.append('src')
        
        print("🔄 Testing data loading...")
        from data_loader import DataLoader
        data_loader = DataLoader('data/raw')
        movies_df, ratings_df = data_loader.load_data()
        print(f"✅ Data loaded: {len(movies_df)} movies, {len(ratings_df)} ratings")
        
        print("🔄 Testing data preprocessing...")
        movies_with_stats = data_loader.preprocess_data()
        print(f"✅ Data preprocessed: {len(movies_with_stats)} movies with statistics")
        
        print("🔄 Testing recommendation engines...")
        from recommendation_engine import (
            PopularityRecommender,
            ContentBasedRecommender, 
            CollaborativeFilteringRecommender,
            HybridRecommender
        )
        
        # Test popularity recommender
        pop_rec = PopularityRecommender(movies_with_stats)
        pop_recs = pop_rec.recommend('Action', 50, 3)
        print(f"✅ Popularity recommender: {len(pop_recs)} recommendations")
        
        # Test content-based recommender
        content_rec = ContentBasedRecommender(movies_df)
        content_recs = content_rec.recommend('Toy Story', 3)
        print(f"✅ Content-based recommender: {len(content_recs)} recommendations")
        
        # Test collaborative filtering
        collab_rec = CollaborativeFilteringRecommender(ratings_df, movies_df)
        collab_recs = collab_rec.recommend(1, 3)
        print(f"✅ Collaborative filtering: {len(collab_recs)} recommendations")
        
        # Test hybrid recommender
        hybrid_rec = HybridRecommender(pop_rec, content_rec, collab_rec)
        hybrid_recs = hybrid_rec.get_combined_recommendations(1, 3)
        print(f"✅ Hybrid recommender: {len(hybrid_recs)} recommendations")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {str(e)}")
        return False

def test_gui_components():
    """Test GUI components"""
    print_header("GUI COMPONENTS TEST")
    
    # Check ipywidgets availability
    try:
        import ipywidgets
        print("✅ ipywidgets installed - Jupyter GUI ready")
        ipywidgets_available = True
    except ImportError:
        print("❌ ipywidgets not available - Jupyter GUI unavailable")
        ipywidgets_available = False
    
    # Check tkinter availability
    try:
        import tkinter
        print("✅ tkinter available - Desktop GUI ready")
        tkinter_available = True
    except ImportError:
        print("❌ tkinter not available - Desktop GUI unavailable")
        tkinter_available = False
    
    # Check PIL for poster generation
    try:
        from PIL import Image, ImageDraw, ImageFont
        print("✅ Pillow (PIL) available - Poster generation ready")
        pil_available = True
    except ImportError:
        print("❌ Pillow (PIL) not available - Poster generation unavailable")
        pil_available = False
    
    # Test poster generation
    if pil_available:
        try:
            from poster_generator import MoviePosterGenerator
            poster_gen = MoviePosterGenerator("test_posters")
            test_poster = poster_gen.generate_poster("Test Movie", 1)
            print(f"✅ Poster generation test successful: {test_poster}")
            
            # Clean up test
            import shutil
            if os.path.exists("test_posters"):
                shutil.rmtree("test_posters")
                
        except Exception as e:
            print(f"❌ Poster generation test failed: {str(e)}")
    
    return ipywidgets_available and tkinter_available and pil_available

def check_generated_posters():
    """Check if movie posters were generated"""
    print_header("MOVIE POSTERS CHECK")
    
    poster_dir = "posters"
    if os.path.exists(poster_dir):
        poster_files = [f for f in os.listdir(poster_dir) if f.endswith('.png')]
        print(f"✅ Poster directory exists with {len(poster_files)} posters")
        
        if poster_files:
            print("Sample posters:")
            for poster in poster_files[:5]:
                print(f"  📸 {poster}")
        
        return len(poster_files) > 0
    else:
        print(f"❌ Poster directory not found: {poster_dir}")
        return False

def run_comprehensive_validation():
    """Run all validation tests"""
    print_header("MYNEXTMOVIE COMPREHENSIVE VALIDATION")
    print("This script validates the complete movie recommendation system")
    
    # Track overall success
    all_tests_passed = True
    
    # Test 1: Directory structure
    structure_ok = check_directory_structure()
    all_tests_passed = all_tests_passed and structure_ok
    
    # Test 2: Core functionality
    core_ok = test_core_functionality() 
    all_tests_passed = all_tests_passed and core_ok
    
    # Test 3: GUI components
    gui_ok = test_gui_components()
    all_tests_passed = all_tests_passed and gui_ok
    
    # Test 4: Generated posters
    posters_ok = check_generated_posters()
    
    # Final summary
    print_header("VALIDATION SUMMARY")
    
    print(f"📁 Project Structure: {'✅ PASS' if structure_ok else '❌ FAIL'}")
    print(f"🤖 Core Algorithms: {'✅ PASS' if core_ok else '❌ FAIL'}")
    print(f"🖼️ GUI Components: {'✅ PASS' if gui_ok else '❌ FAIL'}")
    print(f"🎨 Movie Posters: {'✅ PASS' if posters_ok else '⚠️ OPTIONAL'}")
    
    if all_tests_passed:
        print("\n🎉 ALL CORE TESTS PASSED!")
        print("✅ MyNextMovie Recommendation System is fully functional!")
    else:
        print("\n⚠️ Some tests failed - check the details above")
    
    print("\n📋 AVAILABLE INTERFACES:")
    print("1. 🖥️ Command Line: python main.py")
    print("2. 📓 Jupyter Notebook: notebooks/interactive_gui.ipynb")
    print("3. 🖼️ Desktop GUI: python gui_app.py (requires virtual env activation)")
    
    print("\n📚 DOCUMENTATION:")
    print("• README.md - Project overview and setup")
    print("• USAGE_GUIDE.md - Comprehensive usage instructions")
    print("• notebooks/ - Interactive analysis and GUI")
    
    print("\n🧪 TESTING:")
    print("• python tests/test_recommenders.py - Unit tests")
    print("• python main.py demo - Quick algorithm demo")
    print("• python validation.py - This comprehensive validation")

if __name__ == "__main__":
    run_comprehensive_validation()
