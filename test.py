from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional: Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_info(driver):
    """Extract unique links, names, and profile links from the current page."""
    items = driver.find_elements(By.XPATH, "//div[starts-with(@data-item-index, '')]")
    results = []

    for item in items:
        try:
            # Extract link
            link_elements = item.find_elements(By.XPATH, ".//a[contains(@href, '/items/')]")
            if link_elements:
                link = link_elements[0].get_attribute("href")
            else:
                continue  # Skip this item if no link is found

            # Extract name
            name_element = item.find_element(By.XPATH, ".//p[contains(@class, 'chakra-text css-1wydx3c')]")
            if name_element:
                name = name_element.text.strip()
            else:
                continue  # Skip this item if no name is found

            if link and name:
                profile_url = "No profile URL"
                # Click the profile button to get the profile link
                profile_button_xpath = "//button[contains(@class, 'chakra-button css-u6jdce')]"
                try:
                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.XPATH, profile_button_xpath))
                    )
                    profile_button = driver.find_element(By.XPATH, profile_button_xpath)
                    driver.execute_script("arguments[0].scrollIntoView(true);", profile_button)
                    driver.execute_script("arguments[0].click();", profile_button)
                    print("Profile button clicked.")

                    # Wait for the URL to change
                    WebDriverWait(driver, 20).until(
                        EC.url_changes(link)
                    )
                    profile_url = driver.current_url
                    print(f"Profile URL: {profile_url}")

                except Exception as e:
                    print(f"Error while clicking the profile button or extracting URL: {e}")

                # Go back to the main page
                try:
                    driver.get("https://godid.io/marketplace")
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[starts-with(@data-item-index, '')]")))
                    print("Navigated back to the main page.")
                except Exception as e:
                    print(f"Error while navigating back to the main page: {e}")

                results.append((link, name, profile_url))

        except Exception as e:
            print(f"Error while processing item: {e}")

    return results

def write_to_file(entries, filename):
    """Write collected entries to a file."""
    with open(filename, 'a') as file:
        for entry in entries:
            entry_str = f"Link: {entry[0]}, Name: {entry[1]}, Profile URL: {entry[2]}"
            file.write(entry_str + '\n')

try:
    # Navigate to the starting URL
    driver.get("https://godid.io/marketplace")
    print("Navigated to the link.")

    # Wait for the page to load completely
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@data-item-index='0']")))
    print("Page loaded.")

    # Initialize variables
    all_links_and_names = []
    target_count = 1500
    output_file = "output.txt"

    while len(all_links_and_names) < target_count:
        # Get links, names, and profiles from the current page
        new_links_and_names = get_info(driver)
        all_links_and_names.extend(new_links_and_names)
        write_to_file(new_links_and_names, output_file)
        print(f"Collected {len(all_links_and_names)} entries so far.")

        if len(all_links_and_names) >= target_count:
            break

        # Scroll down to load more items
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Adjust sleep time if needed for more robust loading

    # Output the collected links and names
    print(f"Collected {len(all_links_and_names)} entries:")
    for count, (link, name, profile_url) in enumerate(all_links_and_names, start=1):
        print(f"{count}. Link: {link}, Name: {name}, Profile URL: {profile_url}")

finally:
    # Close the browser
    driver.quit()
