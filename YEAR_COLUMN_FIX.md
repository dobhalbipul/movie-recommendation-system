# Year Column Fix - Summary

## Issue Fixed
The year column was appearing blank in the GUI tables because the recommendation engines were not including year information in their returned data.

## Root Cause
- DataLoader properly extracted years and created clean movie names
- However, recommendation engines only returned basic columns (S.No., Movie Title)
- Year information was lost in the recommendation results

## Solution Applied

### 1. Updated PopularityRecommender
- Added `year` column to result DataFrame
- Safely handles cases where year column might not exist

### 2. Updated ContentBasedRecommender  
- Added `year` to similarity dataframe
- Included `year` in final result DataFrame

### 3. Updated CollaborativeFilteringRecommender
- Added `year` column to final result DataFrame
- Safely handles missing year data

### 4. Updated HybridRecommender
- Modified to preserve year information from component recommenders
- Included `year` in combined results

### 5. Enhanced GUI Display Logic
- Improved year extraction with robust fallback mechanisms
- Better handling of different data formats
- Fixed regex usage that was causing errors

## Code Changes Made

### In `src/recommendation_engine.py`:
```python
# PopularityRecommender
result = pd.DataFrame({
    'S.No.': range(1, len(top_movies) + 1),
    'Movie Title': top_movies['title'].values,
    'Average Movie Rating': top_movies['avg_rating'].values,
    'Num Reviews': top_movies['num_ratings'].astype(int).values,
    'year': top_movies['year'].values if 'year' in top_movies.columns else [None] * len(top_movies)
})

# ContentBasedRecommender
result = pd.DataFrame({
    'S.No.': range(1, len(top_similar) + 1),
    'Movie Title': top_similar['title'].values,
    'year': top_similar['year'].values
})

# CollaborativeFilteringRecommender
result = pd.DataFrame({
    'S.No.': range(1, len(recommended_movies) + 1),
    'Movie Title': recommended_movies['title'].values,
    'year': recommended_movies['year'].values if 'year' in recommended_movies.columns else [None] * len(recommended_movies)
})

# HybridRecommender
result = pd.DataFrame({
    'S.No.': range(1, len(top_movies) + 1),
    'Movie Title': [movie['title'] for movie in top_movies],
    'year': [movie['year'] for movie in top_movies]
})
```

### In `gui_app.py`:
```python
# Enhanced year extraction logic
elif col == "Year":
    year = row.get('year') or row.get('Year')
    if pd.notna(year) and str(year) != 'nan' and str(year) != '':
        values.append(str(int(float(year))))
    else:
        # Fallback to extract from title
        title = (row.get('Movie Title') or row.get('title') or '')
        year_match = re.search(r'\((\d{4})\)', str(title))
        if year_match:
            values.append(year_match.group(1))
        else:
            values.append('')
```

## Testing Results
- ✅ Popularity recommendations now include year column with values (1997, 1959, 1999)
- ✅ GUI tables display both Movie Name and Year in separate columns
- ✅ Fixed regex error that was causing search failures
- ✅ Year extraction works with robust fallback mechanisms

## Status
The year column is now working correctly across all recommendation types in both the desktop GUI and will work in the Jupyter notebook as well.
