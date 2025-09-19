#!/usr/bin/env python3
"""
Setup script for Movie Recommendation System
This script creates the necessary directory structure and provides setup instructions.
"""

import os
import sys

def create_directories():
    """Create necessary directories for the project."""
    directories = [
        'data',
        'data/raw',
        'data/processed',
        'screenshots'
    ]
    
    for dir_path in directories:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"✅ Created directory: {dir_path}")
        else:
            print(f"📁 Directory already exists: {dir_path}")

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'scikit-learn',
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is NOT installed")
    
    if missing_packages:
        print(f"\n🔧 Install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_data_files():
    """Check if data files are present."""
    data_files = [
        'data/raw/movies.csv',
        'data/raw/ratings.csv'
    ]
    
    missing_files = []
    
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"✅ Data file found: {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ Data file missing: {file_path}")
    
    if missing_files:
        print(f"\n📥 Download data files from:")
        print(f"https://www.kaggle.com/code/ayushimishra2809/movie-recommendationsystem/data?select=ratings.csv")
        print(f"\nRequired files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    return True

def main():
    """Main setup function."""
    print("🎬 Movie Recommendation System - Setup")
    print("=" * 50)
    
    # Create directories
    print("\n📁 Creating directory structure...")
    create_directories()
    
    # Check dependencies
    print("\n🔍 Checking Python dependencies...")
    deps_ok = check_dependencies()
    
    # Check data files
    print("\n📊 Checking data files...")
    data_ok = check_data_files()
    
    # Final status
    print("\n" + "=" * 50)
    if deps_ok and data_ok:
        print("🎉 Setup complete! You can now run:")
        print("   streamlit run streamlit_app.py")
    else:
        print("⚠️  Setup incomplete. Please address the issues above.")
        
        if not deps_ok:
            print("\n1. Install missing Python packages:")
            print("   pip install -r requirements.txt")
        
        if not data_ok:
            print("\n2. Download data files from Kaggle:")
            print("   https://www.kaggle.com/code/ayushimishra2809/movie-recommendationsystem/data?select=ratings.csv")
            print("   Place movies.csv and ratings.csv in data/raw/ directory")

if __name__ == "__main__":
    main()
