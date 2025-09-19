@echo off
echo Starting Netflix-Style Movie Recommendation Web App...
echo.
echo Open your browser and go to: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

REM Activate virtual environment and run streamlit
call ".venv\Scripts\activate"
streamlit run streamlit_app.py
