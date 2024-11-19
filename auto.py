from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
import random
import time

# Function to get a random free proxy
def get_free_proxy():
    print("Fetching a free proxy...")
    response = requests.get("https://free-proxy-list.net/")
    if response.status_code == 200:
        proxies = [
            line.split()[0] + ":" + line.split()[1]
            for line in response.text.split("\n")
            if len(line.split()) > 1 and "elite proxy" in line.lower() and "yes" in line.lower()
        ]
        if proxies:
            proxy = random.choice(proxies)
            print(f"Using proxy: {proxy}")
            return proxy
    print("No proxies available. Running without a proxy.")
    return None

# Function to simulate human-like pauses
def human_pause(min_wait, max_wait):
    wait_time = random.uniform(min_wait, max_wait)
    print(f"Please wait {round(wait_time, 2)} seconds...")
    time.sleep(wait_time)

# Prompt user for the link and the number of visitors
URL = input("Enter the URL to visit: ").strip()
while not URL.startswith("http"):
    print("Please enter a valid URL (e.g., https://example.com).")
    URL = input("Enter the URL to visit: ").strip()

try:
    VISIT_COUNT = int(input("Enter the number of visitors: ").strip())
    if VISIT_COUNT <= 0:
        raise ValueError
except ValueError:
    print("Invalid input. Setting the number of visitors to 10 by default.")
    VISIT_COUNT = 10

# Configuration
WAIT_MIN = 5  # Minimum wait time in seconds
WAIT_MAX = 10  # Maximum wait time in seconds

# Path to your WebDriver (update with the path to your chromedriver)
CHROMEDRIVER_PATH = "chromedriver"

# Main visiting loop
for i in range(VISIT_COUNT):
    proxy_address = get_free_proxy()  # Fetch a new proxy for each visit

    # Setup WebDriver with options
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    if proxy_address:
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = proxy_address
        proxy.ssl_proxy = proxy_address
        proxy.add_to_capabilities(webdriver.DesiredCapabilities.CHROME)
        options.add_argument(f"--proxy-server={proxy_address}")

    driver_service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=driver_service, options=options)

    try:
        user_id = f"User_{str(i + 1).zfill(2)}"  # Generate a user ID
        print(f"{user_id} visiting the site: {URL}")
        
        # Open the URL
        driver.get(URL)
        
        # Simulate human behavior
        human_pause(WAIT_MIN, WAIT_MAX)
        
        # Scroll down and back up
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        human_pause(2, 4)
        driver.execute_script("window.scrollTo(0, 0);")
        
        print(f"{user_id} completed the visit.\n")

    except Exception as e:
        print(f"An error occurred during visit {i + 1}: {e}")

    finally:
        driver.quit()

print("All visits completed successfully!")
