from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time


def scrape_resume(profile_urls):
    
    # download_dir = f"D:\git repos\hackathon\scrapped_resume"

    # Set Chrome options
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {
    #     "download.default_directory": download_dir,  # Set the directory to save downloads
    #     "download.prompt_for_download": False,       # Disable download prompt
    #     "plugins.always_open_pdf_externally": True   # Ensure PDFs are downloaded, not opened in the browser
    # }
    # chrome_options.add_experimental_option("prefs", prefs)
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors') # Ignore SSL certificate errors
    chrome_driver_path = 'chromedriver.exe'

    chrome_service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    email = "sakaneh518@heweek.com"
    password = "linkedintesting@2415"

    linkedin_email = email
    linkedin_password = password    
    try:
        # Open LinkedIn login page
        driver.get("https://www.linkedin.com/login")

        # Wait for the email input field to be present
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        # Enter your LinkedIn email
        email_input.send_keys(linkedin_email)

        # Locate and fill in the password
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(linkedin_password)

        # Click the "Sign in" button
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Sign in']"))
        )
        sign_in_button.click()

        # Wait for the login to complete
        WebDriverWait(driver, 600).until(EC.url_to_be("https://www.linkedin.com/feed/"))
        
        time.sleep(3)
        print("hiii")
        try:
            for i in profile_urls:
                driver.get(i)
                time.sleep(2)
                more_button = driver.find_elements(By.XPATH,"//button[@aria-label='More actions']")
                more_button[-1].click()
                save_pdf = driver.find_elements(By.XPATH,"//div[@aria-label='Save to PDF']")
                save_pdf[-1].click()
                time.sleep(5)
                
        except Exception as e:
            print("error:",e)
        
    except Exception as e:
        print("error:",e)
    finally:
        driver.quit()
        
profile_urls = ["https://in.linkedin.com/in/praveen-m-29737418","https://in.linkedin.com/in/shivakumar-g-98004031"]

# scrape_resume(profile_urls)