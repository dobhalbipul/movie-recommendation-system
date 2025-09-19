"""
Standalone GUI Application for MyNextMovie Recommendation System

This application provides a desktop interface using tkinter for all recommendation algorithms.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
import sys
import os
import re
from PIL import Image, ImageTk
import threading
import requests
from io import BytesIO

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import DataLoader
from recommendation_engine import (
    PopularityRecommender,
    ContentBasedRecommender,
    CollaborativeFilteringRecommender,
    HybridRecommender
)

class MovieRecommendationGUI:
    """Main GUI application for movie recommendations"""
    
    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("🎬 MyNextMovie Recommendation System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#333333')  # Lighter background for better visibility
        
        # Make window resizable and center it
        self.root.minsize(800, 600)
        
        # Initialize data and recommenders
        self.movies_df = None
        self.ratings_df = None
        self.movies_with_stats = None
        self.recommenders = {}
        
        print("GUI initialized, creating loading screen...")  # Debug print
        
        # Create loading screen
        self.create_loading_screen()
        
        # Initialize system in background
        threading.Thread(target=self.initialize_system, daemon=True).start()
    
    def create_loading_screen(self):
        """Create loading screen while system initializes"""
        print("Creating loading screen...")  # Debug print
        
        self.loading_frame = tk.Frame(self.root, bg='#333333')
        self.loading_frame.pack(fill='both', expand=True)
        
        # Netflix-style loading with better visibility
        loading_label = tk.Label(
            self.loading_frame,
            text="🎬 MyNextMovie",
            font=('Arial', 32, 'bold'),
            fg='#E50914',
            bg='#333333'
        )
        loading_label.pack(expand=True)
        
        self.progress_var = tk.StringVar()
        self.progress_var.set("Loading recommendation system...")
        
        progress_label = tk.Label(
            self.loading_frame,
            textvariable=self.progress_var,
            font=('Arial', 14),
            fg='white',
            bg='#333333'
        )
        progress_label.pack(pady=20)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.loading_frame,
            mode='indeterminate',
            length=300
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.start()
        
        print("Loading screen created!")  # Debug print
    
    def initialize_system(self):
        """Initialize the recommendation system"""
        try:
            self.progress_var.set("Loading movie and rating data...")
            self.root.update()
            
            # Load data
            data_loader = DataLoader('data/raw')
            self.movies_df, self.ratings_df = data_loader.load_data()
            
            self.progress_var.set("Preprocessing data...")
            self.root.update()
            
            self.movies_with_stats = data_loader.preprocess_data()
            
            self.progress_var.set("Initializing recommendation engines...")
            self.root.update()
            
            # Initialize recommenders
            self.recommenders['popularity'] = PopularityRecommender(self.movies_with_stats)
            self.recommenders['content'] = ContentBasedRecommender(self.movies_df)
            self.recommenders['collaborative'] = CollaborativeFilteringRecommender(self.ratings_df, self.movies_df)
            self.recommenders['hybrid'] = HybridRecommender(
                self.recommenders['popularity'],
                self.recommenders['content'],
                self.recommenders['collaborative']
            )
            
            self.progress_var.set("System ready!")
            self.root.update()
            
            # Create main interface
            self.root.after(1000, self.create_main_interface)
            
        except Exception as e:
            print(f"Error during initialization: {str(e)}")  # Debug print
            messagebox.showerror("Error", f"Failed to initialize system: {str(e)}")
            # Instead of quitting, show a simple interface
            self.create_simple_interface()
    
    def create_simple_interface(self):
        """Create a simple interface when full initialization fails"""
        try:
            self.loading_frame.destroy()
        except:
            pass
            
        # Create a simple interface
        simple_frame = tk.Frame(self.root, bg='#141414')
        simple_frame.pack(fill='both', expand=True)
        
        error_label = tk.Label(
            simple_frame,
            text="⚠️ System Initialization Failed",
            font=('Arial', 20, 'bold'),
            fg='#FF6B6B',
            bg='#141414'
        )
        error_label.pack(expand=True)
        
        info_label = tk.Label(
            simple_frame,
            text="Please check the console for error details",
            font=('Arial', 12),
            fg='white',
            bg='#141414'
        )
        info_label.pack(pady=20)
    
    def create_main_interface(self):
        """Create the main application interface"""
        print("Creating main interface...")  # Debug print
        
        # Stop and destroy loading screen properly
        try:
            self.progress_bar.stop()
        except:
            pass  # Progress bar might already be destroyed
            
        try:
            self.loading_frame.destroy()
        except:
            pass
        
        # Create main frame with visible background
        main_frame = tk.Frame(self.root, bg='#222222')  # Lighter gray for visibility
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header with better visibility
        header_frame = tk.Frame(main_frame, bg='#222222')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="🎬 MyNextMovie",
            font=('Arial', 28, 'bold'),
            fg='#E50914',
            bg='#222222'
        )
        title_label.pack(side='left')
        
        subtitle_label = tk.Label(
            header_frame,
            text="Discover your next favorite movie",
            font=('Arial', 12),
            fg='#FFFFFF',  # Bright white
            bg='#222222'
        )
        subtitle_label.pack(side='left', padx=(20, 0))
        
        # Data info with bright colors
        info_text = f"📊 {len(self.movies_df)} movies • {len(self.ratings_df)} ratings • {self.ratings_df['userId'].nunique()} users"
        info_label = tk.Label(
            header_frame,
            text=info_text,
            font=('Arial', 10),
            fg='#CCCCCC',  # Light gray
            bg='#222222'
        )
        info_label.pack(side='right')
        
        # Create notebook for tabs with better styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#222222', borderwidth=0)
        style.configure('TNotebook.Tab', background='#444444', foreground='white', padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', '#E50914')])
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        print("Creating tabs...")  # Debug print
        
        # Create tabs
        self.create_popularity_tab()
        self.create_content_tab()
        self.create_collaborative_tab()
        self.create_hybrid_tab()
        self.create_analytics_tab()
        
        print("Main interface created successfully!")  # Debug print
    
    def create_results_table(self, parent_frame, columns):
        """Create a styled table for displaying recommendation results"""
        # Create frame for table and scrollbars
        table_frame = tk.Frame(parent_frame, bg='#222222')
        table_frame.pack(fill='both', expand=True)
        
        # Configure style for the treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                       background="#2a2a2a",
                       foreground="white",
                       rowheight=25,
                       fieldbackground="#2a2a2a")
        style.configure("Custom.Treeview.Heading",
                       background="#E50914",
                       foreground="white",
                       font=('Arial', 10, 'bold'))
        style.map("Custom.Treeview", 
                 background=[('selected', '#E50914')])
        
        # Create treeview with scrollbars
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', style="Custom.Treeview")
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and tree
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        tree.pack(side="left", fill="both", expand=True)
        
        # Configure column headings and widths
        for col in columns:
            tree.heading(col, text=col)
            if col == 'Movie Title':
                tree.column(col, width=300, minwidth=200)
            elif col == 'Average Movie Rating':
                tree.column(col, width=150, minwidth=100)
            elif col == 'Number of Reviews':
                tree.column(col, width=150, minwidth=100)
            elif col == 'Similarity Score':
                tree.column(col, width=120, minwidth=100)
            elif col == 'Predicted Rating':
                tree.column(col, width=130, minwidth=100)
            else:
                tree.column(col, width=100, minwidth=80)
        
        return tree
    
    def display_recommendations_in_table(self, tree, recommendations, show_rating_col=True):
        """Display recommendations in a table format"""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        if recommendations.empty:
            # Insert a "No results" message
            tree.insert("", "end", values=("No recommendations found",))
            return
        
        # Insert recommendations
        for i, (_, row) in enumerate(recommendations.iterrows(), 1):
            values = []
            for col in tree["columns"]:
                if col == "Rank":
                    values.append(i)
                elif col == "Movie Name":
                    # Handle different column names for movie title
                    title = row.get('Movie Title') or row.get('Movie_Title') or row.get('title') or row.get('movie_name', '')
                    # Remove year from title if it's still there
                    clean_title = str(title)
                    clean_title = re.sub(r'\s*\(\d{4}\)$', '', clean_title)
                    values.append(clean_title)
                elif col == "Year":
                    # Extract year from different possible sources
                    year = row.get('year') or row.get('Year')
                    
                    # If year is available and valid, use it
                    if pd.notna(year) and str(year) != 'nan' and str(year) != '':
                        values.append(str(int(float(year))))
                    else:
                        # Try to extract from original title or any title field
                        title = (row.get('Movie Title') or row.get('Movie_Title') or 
                                row.get('title') or row.get('original_title', ''))
                        year_match = re.search(r'\((\d{4})\)', str(title))
                        if year_match:
                            values.append(year_match.group(1))
                        else:
                            values.append('')
                elif col == "Movie Title":
                    # For backward compatibility - show clean title without year
                    title = row.get('Movie Title') or row.get('Movie_Title') or row.get('title') or row.get('movie_name', '')
                    clean_title = str(title)
                    clean_title = re.sub(r'\s*\(\d{4}\)$', '', clean_title)
                    values.append(clean_title)
                elif col == "Average Rating" or col == "Average Movie Rating":
                    # Handle different column names for rating
                    rating = row.get('Average Movie Rating') or row.get('Average_Movie_Rating') or row.get('rating', 0)
                    values.append(f"{rating:.2f}" if rating and rating > 0 else "")
                elif col == "Number of Reviews":
                    # Handle different column names for review count
                    reviews = row.get('Number of Reviews') or row.get('Num Reviews') or row.get('Number_of_Reviews') or row.get('num_ratings', 0)
                    values.append(f"{reviews:,}" if reviews and reviews > 0 else "")
                else:
                    # For any other columns, just get the value
                    values.append(row.get(col, ''))
            
            tree.insert("", "end", values=values)
    
    def create_popularity_tab(self):
        """Create popularity-based recommendations tab"""
        tab_frame = tk.Frame(self.notebook, bg='#141414')
        self.notebook.add(tab_frame, text='🔥 Popular Movies')
        
        # Controls frame
        controls_frame = tk.Frame(tab_frame, bg='#141414')
        controls_frame.pack(fill='x', padx=20, pady=20)
        
        # Genre selection
        tk.Label(controls_frame, text="Genre:", font=('Arial', 12, 'bold'), fg='white', bg='#141414').grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        genres = self.get_unique_genres()
        self.genre_var = tk.StringVar(value='Action')
        genre_combo = ttk.Combobox(controls_frame, textvariable=self.genre_var, values=genres, width=20)
        genre_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Min reviews
        tk.Label(controls_frame, text="Min Reviews:", font=('Arial', 12, 'bold'), fg='white', bg='#141414').grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        self.min_reviews_var = tk.IntVar(value=50)
        min_reviews_spin = tk.Spinbox(controls_frame, from_=1, to=200, textvariable=self.min_reviews_var, width=10)
        min_reviews_spin.grid(row=0, column=3, padx=(0, 20))
        
        # Number of recommendations
        tk.Label(controls_frame, text="Recommendations:", font=('Arial', 12, 'bold'), fg='white', bg='#141414').grid(row=0, column=4, sticky='w', padx=(0, 10))
        
        self.pop_num_recs_var = tk.IntVar(value=10)
        num_recs_spin = tk.Spinbox(controls_frame, from_=1, to=20, textvariable=self.pop_num_recs_var, width=10)
        num_recs_spin.grid(row=0, column=5, padx=(0, 20))
        
        # Get recommendations button
        get_button = tk.Button(
            controls_frame,
            text="Get Popular Movies",
            command=self.get_popularity_recommendations,
            bg='#E50914',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        get_button.grid(row=0, column=6)
        
        # Results frame
        results_frame = tk.Frame(tab_frame, bg='#222222')
        results_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create results table
        columns = ('Rank', 'Movie Name', 'Year', 'Average Rating', 'Number of Reviews')
        self.pop_results_table = self.create_results_table(results_frame, columns)
    
    def create_content_tab(self):
        """Create content-based recommendations tab"""
        tab_frame = tk.Frame(self.notebook, bg='#141414')
        self.notebook.add(tab_frame, text='🎯 Similar Movies')
        
        # Controls frame
        controls_frame = tk.Frame(tab_frame, bg='#141414')
        controls_frame.pack(fill='x', padx=20, pady=20)
        
        # Movie selection
        tk.Label(controls_frame, text="Movie Title:", font=('Arial', 12, 'bold'), fg='white', bg='#141414').grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.movie_var = tk.StringVar()
        movie_entry = tk.Entry(controls_frame, textvariable=self.movie_var, width=40, font=('Arial', 10))
        movie_entry.grid(row=0, column=1, padx=(0, 20))
        movie_entry.insert(0, "Toy Story")
        
        # Number of recommendations
        tk.Label(controls_frame, text="Recommendations:", font=('Arial', 12, 'bold'), fg='white', bg='#141414').grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        self.content_num_recs_var = tk.IntVar(value=10)
        num_recs_spin = tk.Spinbox(controls_frame, from_=1, to=20, textvariable=self.content_num_recs_var, width=10)
        num_recs_spin.grid(row=0, column=3, padx=(0, 20))
        
        # Get recommendations button
        get_button = tk.Button(
            controls_frame,
            text="Find Similar Movies",
            command=self.get_content_recommendations,
            bg='#E50914',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        get_button.grid(row=0, column=4)
        
        # Popular movies quick select
        tk.Label(controls_frame, text="Quick Select:", font=('Arial', 10), fg='#CCCCCC', bg='#141414').grid(row=1, column=0, sticky='w', pady=(10, 0))
        
        popular_movies = self.get_popular_movies()[:10]
        for i, movie in enumerate(popular_movies):
            btn = tk.Button(
                controls_frame,
                text=movie[:20] + "..." if len(movie) > 20 else movie,
                command=lambda m=movie: self.movie_var.set(m),
                bg='#333333',
                fg='white',
                font=('Arial', 8),
                padx=5,
                pady=2
            )
            btn.grid(row=1 + i//5, column=1 + i%5, padx=2, pady=2, sticky='w')
        
        # Results frame
        results_frame = tk.Frame(tab_frame, bg='#222222')
        results_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create results table
        columns = ('Rank', 'Movie Name', 'Year')
        self.content_results_table = self.create_results_table(results_frame, columns)
    
    def create_collaborative_tab(self):
        """Create collaborative filtering recommendations tab"""
        tab_frame = tk.Frame(self.notebook, bg='#141414')
        self.notebook.add(tab_frame, text='👥 Personal Picks')
        
        # Controls frame
        controls_frame = tk.Frame(tab_frame, bg='#141414')
        controls_frame.pack(fill='x', padx=20, pady=20)
        
        # User ID
        tk.Label(controls_frame, text="User ID:", font=('Arial', 12, 'bold'), fg='white', bg='#141414').grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.user_id_var = tk.IntVar(value=1)
        user_id_spin = tk.Spinbox(controls_frame, from_=1, to=668, textvariable=self.user_id_var, width=10)
        user_id_spin.grid(row=0, column=1, padx=(0, 20))
        
        # Similar users (K)
        tk.Label(controls_frame, text="Similar Users (K):", font=('Arial', 12, 'bold'), fg='white', bg='#141414').grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        self.k_users_var = tk.IntVar(value=100)
        k_users_spin = tk.Spinbox(controls_frame, from_=10, to=300, textvariable=self.k_users_var, width=10)
        k_users_spin.grid(row=0, column=3, padx=(0, 20))
        
        # Number of recommendations
        tk.Label(controls_frame, text="Recommendations:", font=('Arial', 12, 'bold'), fg='white', bg='#141414').grid(row=0, column=4, sticky='w', padx=(0, 10))
        
        self.collab_num_recs_var = tk.IntVar(value=10)
        num_recs_spin = tk.Spinbox(controls_frame, from_=1, to=20, textvariable=self.collab_num_recs_var, width=10)
        num_recs_spin.grid(row=0, column=5, padx=(0, 20))
        
        # Get recommendations button
        get_button = tk.Button(
            controls_frame,
            text="Get Personal Recommendations",
            command=self.get_collaborative_recommendations,
            bg='#E50914',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        get_button.grid(row=0, column=6)
        
        # Quick user select
        tk.Label(controls_frame, text="Active Users:", font=('Arial', 10), fg='#CCCCCC', bg='#141414').grid(row=1, column=0, sticky='w', pady=(10, 0))
        
        active_users = self.get_active_users()[:20]
        for i, user_id in enumerate(active_users):
            btn = tk.Button(
                controls_frame,
                text=f"User {user_id}",
                command=lambda u=user_id: self.user_id_var.set(u),
                bg='#333333',
                fg='white',
                font=('Arial', 8),
                padx=5,
                pady=2
            )
            btn.grid(row=1 + i//10, column=1 + i%10, padx=2, pady=2, sticky='w')
        
        # Results frame
        results_frame = tk.Frame(tab_frame, bg='#222222')
        results_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create results table
        columns = ('Rank', 'Movie Name', 'Year')
        self.collab_results_table = self.create_results_table(results_frame, columns)
    
    def create_hybrid_tab(self):
        """Create hybrid recommendations tab"""
        tab_frame = tk.Frame(self.notebook, bg='#141414')
        self.notebook.add(tab_frame, text='🌟 Hybrid Picks')
        
        # Controls frame
        controls_frame = tk.Frame(tab_frame, bg='#141414')
        controls_frame.pack(fill='x', padx=20, pady=20)
        
        # User ID
        tk.Label(controls_frame, text="User ID:", font=('Arial', 12, 'bold'), fg='white', bg='#141414').grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.hybrid_user_var = tk.IntVar(value=1)
        user_id_spin = tk.Spinbox(controls_frame, from_=1, to=668, textvariable=self.hybrid_user_var, width=10)
        user_id_spin.grid(row=0, column=1, padx=(0, 20))
        
        # Number of recommendations
        tk.Label(controls_frame, text="Recommendations:", font=('Arial', 12, 'bold'), fg='white', bg='#141414').grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        self.hybrid_num_recs_var = tk.IntVar(value=10)
        num_recs_spin = tk.Spinbox(controls_frame, from_=1, to=20, textvariable=self.hybrid_num_recs_var, width=10)
        num_recs_spin.grid(row=0, column=3, padx=(0, 20))
        
        # Get recommendations button
        get_button = tk.Button(
            controls_frame,
            text="Get Hybrid Recommendations",
            command=self.get_hybrid_recommendations,
            bg='#E50914',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        get_button.grid(row=0, column=4)
        
        # Algorithm weights
        weights_frame = tk.Frame(controls_frame, bg='#141414')
        weights_frame.grid(row=1, column=0, columnspan=7, pady=(20, 0), sticky='w')
        
        tk.Label(weights_frame, text="Algorithm Weights:", font=('Arial', 12, 'bold'), fg='white', bg='#141414').pack(anchor='w')
        
        # Collaborative weight
        collab_frame = tk.Frame(weights_frame, bg='#141414')
        collab_frame.pack(fill='x', pady=5)
        
        tk.Label(collab_frame, text="Collaborative:", font=('Arial', 10), fg='#CCCCCC', bg='#141414').pack(side='left')
        
        self.collab_weight_var = tk.DoubleVar(value=0.6)
        collab_scale = tk.Scale(
            collab_frame,
            from_=0.0,
            to=1.0,
            resolution=0.1,
            variable=self.collab_weight_var,
            orient='horizontal',
            bg='#141414',
            fg='white',
            highlightbackground='#141414'
        )
        collab_scale.pack(side='left', padx=10)
        
        # Popularity weight
        pop_frame = tk.Frame(weights_frame, bg='#141414')
        pop_frame.pack(fill='x', pady=5)
        
        tk.Label(pop_frame, text="Popularity:", font=('Arial', 10), fg='#CCCCCC', bg='#141414').pack(side='left')
        
        self.pop_weight_var = tk.DoubleVar(value=0.4)
        pop_scale = tk.Scale(
            pop_frame,
            from_=0.0,
            to=1.0,
            resolution=0.1,
            variable=self.pop_weight_var,
            orient='horizontal',
            bg='#141414',
            fg='white',
            highlightbackground='#141414'
        )
        pop_scale.pack(side='left', padx=10)
        
        # Results frame
        results_frame = tk.Frame(tab_frame, bg='#222222')
        results_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create results table
        columns = ('Rank', 'Movie Name', 'Year')
        self.hybrid_results_table = self.create_results_table(results_frame, columns)
    
    def create_analytics_tab(self):
        """Create analytics dashboard tab"""
        tab_frame = tk.Frame(self.notebook, bg='#141414')
        self.notebook.add(tab_frame, text='📊 Analytics')
        
        # Controls frame
        controls_frame = tk.Frame(tab_frame, bg='#141414')
        controls_frame.pack(fill='x', padx=20, pady=20)
        
        # Show analytics button
        analytics_button = tk.Button(
            controls_frame,
            text="Show Data Analytics",
            command=self.show_analytics,
            bg='#E50914',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        analytics_button.pack()
        
        # Results frame
        results_frame = tk.Frame(tab_frame, bg='#141414')
        results_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Results text area
        self.analytics_results_text = scrolledtext.ScrolledText(
            results_frame,
            bg='#222222',
            fg='white',
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.analytics_results_text.pack(fill='both', expand=True)
    
    # Helper methods
    def get_unique_genres(self):
        """Get list of unique genres"""
        all_genres = set()
        for genres_str in self.movies_df['genres'].dropna():
            genres = genres_str.split('|')
            all_genres.update(genres)
        return sorted(list(all_genres))
    
    def get_popular_movies(self, n=50):
        """Get popular movie titles without years"""
        popular_movies = self.movies_with_stats.nlargest(n, 'num_ratings')
        # Return clean movie names without years
        clean_titles = []
        for title in popular_movies['title']:
            # Remove year from title if present
            clean_title = str(title)
            clean_title = re.sub(r'\s*\(\d{4}\)$', '', clean_title)
            clean_titles.append(clean_title)
        return clean_titles
    
    def get_active_users(self, n=50):
        """Get most active user IDs"""
        return self.ratings_df['userId'].value_counts().head(n).index.tolist()
    
    # Recommendation methods
    def get_popularity_recommendations(self):
        """Get popularity-based recommendations"""
        try:
            # Clear previous results
            for item in self.pop_results_table.get_children():
                self.pop_results_table.delete(item)
            
            recommendations = self.recommenders['popularity'].recommend(
                genre=self.genre_var.get(),
                min_reviews_threshold=self.min_reviews_var.get(),
                num_recommendations=self.pop_num_recs_var.get()
            )
            
            if recommendations.empty:
                messagebox.showinfo("No Results", "❌ No movies found matching the criteria.")
            else:
                # Only show columns that exist in the data
                self.pop_results_table['columns'] = ['Rank', 'Movie Name', 'Year', 'Average Rating', 'Number of Reviews']
                
                # Update column headings
                for col in self.pop_results_table['columns']:
                    self.pop_results_table.heading(col, text=col)
                
                # Display results in table
                self.display_recommendations_in_table(self.pop_results_table, recommendations)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get recommendations: {str(e)}")
    
    def get_content_recommendations(self):
        """Get content-based recommendations"""
        try:
            # Clear previous results
            for item in self.content_results_table.get_children():
                self.content_results_table.delete(item)
            
            movie_title = self.movie_var.get().strip()
            if not movie_title:
                messagebox.showwarning("Warning", "Please enter a movie title.")
                return
            
            recommendations = self.recommenders['content'].recommend(
                movie_title=movie_title,
                num_recommendations=self.content_num_recs_var.get()
            )
            
            if recommendations.empty:
                messagebox.showinfo("No Results", "❌ No similar movies found or movie not in database.")
            else:
                # Only show columns that exist in the data
                self.content_results_table['columns'] = ['Rank', 'Movie Name', 'Year']
                
                # Update column headings
                for col in self.content_results_table['columns']:
                    self.content_results_table.heading(col, text=col)
                
                # Display results in table
                self.display_recommendations_in_table(self.content_results_table, recommendations)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get recommendations: {str(e)}")
    
    def get_collaborative_recommendations(self):
        """Get collaborative filtering recommendations"""
        try:
            # Clear previous results
            for item in self.collab_results_table.get_children():
                self.collab_results_table.delete(item)
            
            recommendations = self.recommenders['collaborative'].recommend(
                user_id=self.user_id_var.get(),
                num_recommendations=self.collab_num_recs_var.get(),
                k_similar_users=self.k_users_var.get()
            )
            
            if recommendations.empty:
                messagebox.showinfo("No Results", "❌ No recommendations found for this user.")
            else:
                # Only show columns that exist in the data
                self.collab_results_table['columns'] = ['Rank', 'Movie Name', 'Year']
                
                # Update column headings
                for col in self.collab_results_table['columns']:
                    self.collab_results_table.heading(col, text=col)
                
                # Display results in table
                self.display_recommendations_in_table(self.collab_results_table, recommendations)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get recommendations: {str(e)}")
    
    def get_hybrid_recommendations(self):
        """Get hybrid recommendations"""
        try:
            # Clear previous results
            for item in self.hybrid_results_table.get_children():
                self.hybrid_results_table.delete(item)
            
            weights = {
                'collaborative': self.collab_weight_var.get(),
                'popularity': self.pop_weight_var.get()
            }
            
            recommendations = self.recommenders['hybrid'].get_combined_recommendations(
                user_id=self.hybrid_user_var.get(),
                num_recommendations=self.hybrid_num_recs_var.get(),
                weights=weights
            )
            
            if recommendations.empty:
                messagebox.showinfo("No Results", "❌ No hybrid recommendations found.")
            else:
                # Only show columns that exist in the data
                self.hybrid_results_table['columns'] = ['Rank', 'Movie Name', 'Year']
                
                # Update column headings
                for col in self.hybrid_results_table['columns']:
                    self.hybrid_results_table.heading(col, text=col)
                
                # Display results in table
                self.display_recommendations_in_table(self.hybrid_results_table, recommendations)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get recommendations: {str(e)}")
    
    def show_analytics(self):
        """Show data analytics"""
        try:
            self.analytics_results_text.delete(1.0, tk.END)
            
            result_text = "📊 MyNextMovie Data Analytics Dashboard\\n"
            result_text += "=" * 80 + "\\n\\n"
            
            # Basic statistics
            stats = {
                'Total Movies': len(self.movies_df),
                'Total Users': self.ratings_df['userId'].nunique(),
                'Total Ratings': len(self.ratings_df),
                'Average Rating': f"{self.ratings_df['rating'].mean():.2f}",
                'Unique Genres': len(self.get_unique_genres()),
                'Most Popular Genre': self.movies_df['genres'].str.split('|').explode().value_counts().index[0],
                'Data Sparsity': f"{((len(self.movies_df) * self.ratings_df['userId'].nunique() - len(self.ratings_df)) / (len(self.movies_df) * self.ratings_df['userId'].nunique()) * 100):.2f}%"
            }
            
            for key, value in stats.items():
                result_text += f"{key}: {value}\\n"
            
            result_text += "\\n" + "=" * 80 + "\\n\\n"
            
            # Top genres
            result_text += "🎭 Top 10 Genres:\\n"
            result_text += "-" * 30 + "\\n"
            top_genres = self.movies_df['genres'].str.split('|').explode().value_counts().head(10)
            for i, (genre, count) in enumerate(top_genres.items(), 1):
                result_text += f"{i:2d}. {genre}: {count} movies\\n"
            
            result_text += "\\n"
            
            # Top rated movies
            result_text += "⭐ Top 10 Highest Rated Movies (50+ reviews):\\n"
            result_text += "-" * 50 + "\\n"
            top_rated = self.movies_with_stats[self.movies_with_stats['num_ratings'] >= 50].nlargest(10, 'avg_rating')
            for i, (_, movie) in enumerate(top_rated.iterrows(), 1):
                result_text += f"{i:2d}. {movie['title']} ({movie['avg_rating']:.2f}⭐, {movie['num_ratings']} reviews)\\n"
            
            result_text += "\\n"
            
            # Most active users
            result_text += "👥 Top 10 Most Active Users:\\n"
            result_text += "-" * 30 + "\\n"
            top_users = self.ratings_df['userId'].value_counts().head(10)
            for i, (user_id, count) in enumerate(top_users.items(), 1):
                result_text += f"{i:2d}. User {user_id}: {count} ratings\\n"
            
            self.analytics_results_text.insert(tk.END, result_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show analytics: {str(e)}")


def main():
    """Main function to run the GUI application"""
    # Check if data files exist
    if not os.path.exists("data/raw/movies.csv") or not os.path.exists("data/raw/ratings.csv"):
        messagebox.showerror(
            "Error", 
            "Data files not found!\\n\\nPlease ensure the following files exist:\\n- data/raw/movies.csv\\n- data/raw/ratings.csv"
        )
        return
    
    # Create and run the GUI
    root = tk.Tk()
    app = MovieRecommendationGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\\nApplication closed by user.")


if __name__ == "__main__":
    main()
