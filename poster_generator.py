"""
Movie Poster Placeholder Generator

Generates dummy movie poster images for the GUI applications.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random
import hashlib

class MoviePosterGenerator:
    """Generate placeholder movie poster images"""
    
    def __init__(self, poster_dir="posters"):
        """Initialize the poster generator"""
        self.poster_dir = poster_dir
        self.poster_size = (300, 450)  # Standard movie poster ratio
        self.colors = [
            '#E50914',  # Netflix red
            '#221F1F',  # Dark gray
            '#564D4D',  # Medium gray
            '#F5F5F1',  # Light gray
            '#B20710',  # Dark red
            '#831010',  # Darker red
            '#FF6B6B',  # Light red
            '#4ECDC4',  # Teal
            '#45B7D1',  # Blue
            '#96CEB4',  # Green
            '#FFEAA7',  # Yellow
            '#DDA0DD',  # Plum
            '#98D8C8',  # Mint
            '#F7DC6F',  # Light yellow
            '#BB8FCE',  # Light purple
        ]
        
        # Create poster directory if it doesn't exist
        os.makedirs(self.poster_dir, exist_ok=True)
    
    def generate_poster(self, movie_title, movie_id=None):
        """
        Generate a placeholder poster for a movie
        
        Args:
            movie_title (str): Title of the movie
            movie_id (int): Movie ID for consistent color generation
            
        Returns:
            str: Path to the generated poster image
        """
        # Create filename from title
        safe_title = "".join(c for c in movie_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
        filename = f"{safe_title}.png"
        filepath = os.path.join(self.poster_dir, filename)
        
        # Return existing poster if it exists
        if os.path.exists(filepath):
            return filepath
        
        # Generate consistent color from movie title/ID
        if movie_id:
            color_index = movie_id % len(self.colors)
        else:
            # Use hash of title for consistent color
            title_hash = hashlib.md5(movie_title.encode()).hexdigest()
            color_index = int(title_hash[:2], 16) % len(self.colors)
        
        background_color = self.colors[color_index]
        
        # Create image
        image = Image.new('RGB', self.poster_size, background_color)
        draw = ImageDraw.Draw(image)
        
        # Try to use a nice font, fall back to default if not available
        try:
            # Try to find a good font (adjust path as needed)
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_medium = ImageFont.truetype("arial.ttf", 18)
            font_small = ImageFont.truetype("arial.ttf", 14)
        except:
            # Fall back to default font
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Add some visual elements
        self._add_background_pattern(draw, background_color)
        
        # Add title text
        self._add_title_text(draw, movie_title, font_large, font_medium)
        
        # Add some decorative elements
        self._add_decorative_elements(draw, background_color)
        
        # Save the image
        image.save(filepath, 'PNG')
        return filepath
    
    def _add_background_pattern(self, draw, bg_color):
        """Add a subtle background pattern"""
        # Convert hex color to RGB for calculations
        if bg_color.startswith('#'):
            bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
        else:
            bg_rgb = (128, 128, 128)  # Default gray
        
        # Create a slightly lighter/darker shade for pattern
        pattern_rgb = tuple(min(255, max(0, c + 20)) for c in bg_rgb)
        pattern_color = f"rgb{pattern_rgb}"
        
        # Add some geometric shapes for texture
        width, height = self.poster_size
        
        # Add diagonal lines
        for i in range(0, width + height, 50):
            draw.line([(i, 0), (i - height, height)], fill=pattern_color, width=1)
        
        # Add some circles
        for _ in range(5):
            x = random.randint(0, width)
            y = random.randint(0, height)
            r = random.randint(10, 30)
            draw.ellipse([x-r, y-r, x+r, y+r], outline=pattern_color, width=2)
    
    def _add_title_text(self, draw, title, font_large, font_medium):
        """Add the movie title to the poster"""
        width, height = self.poster_size
        
        # Split title into words for better wrapping
        words = title.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            # Estimate text width (rough approximation)
            if len(test_line) * 12 < width - 40:  # Leave some margin
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Limit to 4 lines max
        lines = lines[:4]
        
        # Calculate starting Y position to center text
        line_height = 30
        total_text_height = len(lines) * line_height
        start_y = (height - total_text_height) // 2
        
        # Draw each line
        for i, line in enumerate(lines):
            # Calculate text position for centering
            bbox = draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * line_height
            
            # Add text with shadow effect
            shadow_color = "black" if sum(int(self.colors[0][i:i+2], 16) for i in (1, 3, 5)) > 400 else "white"
            text_color = "white" if sum(int(self.colors[0][i:i+2], 16) for i in (1, 3, 5)) < 400 else "black"
            
            # Shadow
            draw.text((x+2, y+2), line, font=font_large, fill=shadow_color)
            # Main text
            draw.text((x, y), line, font=font_large, fill=text_color)
    
    def _add_decorative_elements(self, draw, bg_color):
        """Add some decorative elements to make it look more like a movie poster"""
        width, height = self.poster_size
        
        # Add border
        border_color = "white" if bg_color == '#221F1F' else "black"
        draw.rectangle([10, 10, width-10, height-10], outline=border_color, width=3)
        
        # Add "MOVIE" text at bottom
        try:
            font_small = ImageFont.truetype("arial.ttf", 12)
        except:
            font_small = ImageFont.load_default()
        
        movie_text = "★ MOVIE ★"
        bbox = draw.textbbox((0, 0), movie_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height - 40
        
        text_color = "white" if bg_color == '#221F1F' else "black"
        draw.text((x, y), movie_text, font=font_small, fill=text_color)
        
        # Add some stars
        star_color = "#FFD700"  # Gold
        for _ in range(3):
            x = random.randint(20, width-20)
            y = random.randint(20, 100)
            self._draw_star(draw, x, y, 8, star_color)
    
    def _draw_star(self, draw, cx, cy, size, color):
        """Draw a simple star shape"""
        points = []
        for i in range(10):
            angle = i * 36  # 360/10 = 36 degrees
            if i % 2 == 0:
                # Outer point
                x = cx + size * (1 if angle == 0 else 0.9 if angle == 36 else 0.3 if angle == 72 else -0.3 if angle == 108 else -0.9 if angle == 144 else -1 if angle == 180 else -0.9 if angle == 216 else -0.3 if angle == 252 else 0.3 if angle == 288 else 0.9)
                y = cy + size * (0 if angle == 0 else -0.4 if angle == 36 else -1 if angle == 72 else -1 if angle == 108 else -0.4 if angle == 144 else 0 if angle == 180 else 0.4 if angle == 216 else 1 if angle == 252 else 1 if angle == 288 else 0.4)
            else:
                # Inner point
                x = cx + size * 0.4 * (1 if angle == 18 else 0.3 if angle == 54 else -0.3 if angle == 126 else -1 if angle == 162 else -1 if angle == 198 else -0.3 if angle == 234 else 0.3 if angle == 306 else 1 if angle == 342 else 0)
                y = cy + size * 0.4 * (0 if angle == 18 else -0.9 if angle == 54 else -0.9 if angle == 126 else 0 if angle == 162 else 0 if angle == 198 else 0.9 if angle == 234 else 0.9 if angle == 306 else 0 if angle == 342 else 0)
            points.append((x, y))
        
        # Simplified star - just draw a small filled circle
        draw.ellipse([cx-size//2, cy-size//2, cx+size//2, cy+size//2], fill=color)
    
    def generate_posters_for_movies(self, movies_df, limit=50):
        """Generate posters for a list of movies"""
        generated_posters = {}
        
        for i, (_, movie) in enumerate(movies_df.head(limit).iterrows()):
            movie_title = movie['title']
            movie_id = movie['movieId'] if 'movieId' in movie else None
            
            poster_path = self.generate_poster(movie_title, movie_id)
            generated_posters[movie_title] = poster_path
            
            print(f"Generated poster {i+1}/{limit}: {movie_title}")
        
        return generated_posters


# Example usage
if __name__ == "__main__":
    import sys
    sys.path.append('src')
    from data_loader import DataLoader
    
    # Load movie data
    data_loader = DataLoader('data/raw')
    movies_df, _ = data_loader.load_data()
    
    # Generate posters for top 20 popular movies
    poster_gen = MoviePosterGenerator()
    
    # Get popular movies
    movies_with_stats = data_loader.preprocess_data()
    popular_movies = movies_with_stats.nlargest(20, 'num_ratings')
    
    print("Generating movie posters...")
    posters = poster_gen.generate_posters_for_movies(popular_movies, 20)
    
    print(f"\\nGenerated {len(posters)} movie posters in the 'posters' directory!")
    print("\\nSample posters:")
    for title, path in list(posters.items())[:5]:
        print(f"  {title}: {path}")
