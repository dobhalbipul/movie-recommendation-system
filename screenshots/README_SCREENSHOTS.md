# 📸 How to Capture Screenshots for Documentation

## Manual Screenshot Instructions

### 1. Homepage Screenshot
1. Open your browser and navigate to `http://localhost:8501`
2. Wait for the application to fully load
3. Take a full-page screenshot showing:
   - The header "🎬 My CinemaAI Movies"
   - The welcome section with feature descriptions
   - The sidebar with recommendation settings
   - The sample popular movies at the bottom

**Recommended filename:** `webapp_homepage.png`

### 2. Recommendations Screenshot
1. In the sidebar, select "Popularity-Based" recommendations
2. Choose a genre (e.g., "Action")
3. Set minimum reviews to 50
4. Set number of recommendations to 10
5. Click "🎬 Get Recommendations"
6. Wait for the recommendations to load
7. Take a screenshot showing:
   - The filled recommendation cards with movie posters, ratings, and genres
   - The Netflix-style dark theme
   - The grid layout of movie cards

**Recommended filename:** `webapp_recommendations.png`

### 3. Analytics Dashboard Screenshot
1. After generating recommendations, click on the "📊 Analytics Dashboard 📊" tab
2. Take a screenshot showing:
   - The metrics cards at the top
   - The rating distribution chart
   - The year trends chart
   - The professional dark theme

**Recommended filename:** `webapp_analytics.png`

### 4. Algorithm Comparison Screenshot
1. Try different recommendation types:
   - Content-Based (select a movie like "Toy Story")
   - Collaborative Filtering (use User ID: 1)
   - Hybrid (combine parameters)
2. Take screenshots of each to show the variety of results

**Recommended filenames:** 
- `webapp_content_based.png`
- `webapp_collaborative.png`
- `webapp_hybrid.png`

## Browser Tips

### For Best Quality Screenshots:
- Use Chrome or Firefox in full-screen mode
- Set browser zoom to 100%
- Use a resolution of at least 1920x1080
- Ensure the sidebar is fully visible
- Wait for all animations and loading to complete

### Full-Page Screenshots:
- **Chrome**: Use DevTools (F12) → More tools → Full page screenshot
- **Firefox**: Right-click → Take Screenshot → Save full page
- **Edge**: DevTools (F12) → Device Emulation → Capture screenshot

## Screenshot Specifications

### Required Screenshots:
1. **Homepage** (webapp_homepage.png) - Main interface without recommendations
2. **Recommendations** (webapp_recommendations.png) - Movie cards with data
3. **Analytics** (webapp_analytics.png) - Dashboard with charts

### Optional Screenshots:
4. **Different Algorithms** - Show variety of recommendation types
5. **Mobile View** - Responsive design demonstration
6. **Loading States** - Show the professional loading animations

## Adding Screenshots to README

Once you have the screenshots, update the README.md file:

```markdown
## 🖼️ Screenshots

### 🏠 Homepage
![Homepage](screenshots/webapp_homepage.png)

### 🎬 Movie Recommendations
![Recommendations](screenshots/webapp_recommendations.png)

### 📊 Analytics Dashboard
![Analytics](screenshots/webapp_analytics.png)
```

## File Organization

```
screenshots/
├── webapp_homepage.png          # Main interface
├── webapp_recommendations.png   # Movie recommendations
├── webapp_analytics.png         # Analytics dashboard
├── webapp_content_based.png     # Content-based recommendations
├── webapp_collaborative.png     # Collaborative filtering
├── webapp_hybrid.png           # Hybrid recommendations
└── capture_screenshot.py       # Automated capture script
```

## Quality Checklist

Before finalizing screenshots, ensure:
- [ ] Text is crisp and readable
- [ ] Netflix-style dark theme is visible
- [ ] Movie cards show complete information (stars, reviews, genres)
- [ ] Sidebar controls are clearly visible
- [ ] No loading spinners or incomplete data
- [ ] Professional appearance that represents the project well
- [ ] File sizes are reasonable (< 2MB each)

## Automation Alternative

If you have Selenium and ChromeDriver installed:
```bash
cd screenshots
python capture_screenshot.py
```

This will automatically capture screenshots of the running application.
