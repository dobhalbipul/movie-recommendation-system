"""
Screenshot capture script for the movie recommendation system web UI.
This script can be used to programmatically capture screenshots of the application.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def capture_webapp_screenshot():
    """
    Capture screenshot of the running Streamlit application.
    Requires Chrome/Chromium browser and selenium webdriver.
    """
    
    # Setup Chrome options for headless mode (optional)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Remove this line to see the browser
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        # Initialize the Chrome driver
        print("Initializing browser...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to the Streamlit app
        print("Navigating to application...")
        driver.get("http://localhost:8501")
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Give extra time for Streamlit to fully render
        time.sleep(5)
        
        # Take screenshot
        print("Capturing screenshot...")
        screenshot_path = "screenshots/webapp_homepage.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")
        
        # Optionally, interact with the app to capture more screenshots
        try:
            # Try to click the recommendation button if visible
            rec_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Get Recommendations')]")
            if rec_button.is_displayed():
                rec_button.click()
                time.sleep(5)  # Wait for recommendations to load
                
                # Take another screenshot with recommendations
                recommendations_path = "screenshots/webapp_with_recommendations.png"
                driver.save_screenshot(recommendations_path)
                print(f"Recommendations screenshot saved to: {recommendations_path}")
                
        except Exception as e:
            print(f"Could not capture recommendations screenshot: {e}")
        
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        print("Make sure:")
        print("1. Chrome browser is installed")
        print("2. ChromeDriver is installed and in PATH")
        print("3. Streamlit app is running on http://localhost:8501")
        print("4. Install selenium: pip install selenium")
        
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    print("Movie Recommendation System - Screenshot Capture")
    print("=" * 50)
    capture_webapp_screenshot()
