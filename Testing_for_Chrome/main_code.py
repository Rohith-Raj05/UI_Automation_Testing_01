
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager 
from webdriver_manager.firefox import GeckoDriverManager 
import os
import time
from datetime import datetime
import logging



def get_webdriver(browser):
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser == 'firefox':
        # options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    else:
        raise ValueError("Unsupported browser!")
    return driver


logging.basicConfig(level=logging.INFO)


def take_full_page_screenshot(driver, file_path, width):
    # Get the height of the entire page
    web_page_height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight,"
        "document.body.offsetHeight, document.documentElement.offsetHeight,"
        "document.body.clientHeight, document.documentElement.clientHeight);"
    )
    driver.set_window_size(width, web_page_height)  # getting the max height for the website

    # Take a full-page screenshot
    driver.save_screenshot(file_path)


def take_screenshot(url, browser, width, height, idx):
    driver = None
    try:
        driver = get_webdriver(browser)
        driver.get(url)
        logging.info(f"Loading {url} on {browser}")

        time.sleep(5)  # Wait for the page to load fully

        folder_type = "Desktop" if width >= 1366 else "Mobile"
        folder_name = f"Testing_for_chrome/URL{idx}_screenshots/{browser.capitalize()}/{folder_type}/{width}x{height}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        screenshot_path = os.path.join(folder_name, f"{timestamp}.png")
        take_full_page_screenshot(driver, screenshot_path, width)
        logging.info(f"Screenshot saved to {screenshot_path}")
    except Exception as e:
        logging.error(f"Error taking screenshot for {url} on {browser}: {e}")
    finally:
        if driver:
            driver.quit()


def main():
    urls = [
        'https://www.getcalley.com/',
        'https://www.getcalley.com/calley-lifetime-offer/',
        'https://www.getcalley.com/see-a-demo/',
        'https://www.getcalley.com/calley-teams-features/',
        'https://www.getcalley.com/calley-pro-features/'
    ]

    resolutions = [
        (1920, 1080),
        (1366, 768),
        (1536, 864),
        (360, 640),
        (414, 896),
        (375, 667)
    ]

    type_of_browser ="chrome" # to indicate on which type of browser we are working on 
    
    for idx, url in enumerate(urls, start=1):  #it will start the index from 1 which helps in saving screenshots
        for width, height in resolutions:
            take_screenshot(url, type_of_browser , width, height, idx) 


if __name__ == "__main__":
    main()

# thank you and i will be making the seperate video for the firefox browser

