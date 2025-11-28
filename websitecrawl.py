from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def crawl_google_maps_from_url(search_url):
    # Launch Chrome with specific options and scrape place names from a Google Maps search URL
    # Configure Chrome options for headless and efficient performance
    options = Options()
    options.add_argument("--headless=chrome")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    # Disable image loading to speed up page load
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    # Launch the Chrome WebDriver with the configured options
    driver = webdriver.Chrome(options=options)

    try:
        # Record start time to measure crawling duration
        start_time = time.time()

        driver.get(search_url)
        # Wait for the presence of place elements using CSS selector
        elements = WebDriverWait(driver, 1.5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.hfpxzc"))
        )

        place_elements = elements

        # Extract place names from the top search results
        places = []
        for elem in place_elements[:5]:
            try:
                name = elem.get_attribute("aria-label")
                if name:
                    places.append(name)
                else:
                    pass
            except Exception as e:
                pass

        # Calculate elapsed time and report crawling success
        elapsed = time.time() - start_time
        return places

    except Exception as e:
        # Handle exceptions during crawling and report errors
        elapsed = time.time() - start_time
        return []

    finally:
        # Ensure the WebDriver is properly closed
        driver.quit()

if __name__ == "__main__":
    url = input("Enter Google Maps search URL: ").strip()
    places = crawl_google_maps_from_url(url)
    print("Top places found:")
    for place in places:
        print("-", place)
