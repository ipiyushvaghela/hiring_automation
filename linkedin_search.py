from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

# linkedin_email = "kivab31262@apifan.com"
# linkedin_password = "kivab31262@apifan.com"

# linkedin_email = "domovag725@kwalah.com"
# linkedin_password = "domovag725@kwalah.com"

# linkedin_email = "atsundeep@gmail.com"
# linkedin_password = "Ugc2023$$"

def linkedin_post(email, password, job_post, form_link):
    
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors') # Ignore SSL certificate errors
    chrome_driver_path = 'chromedriver.exe'

    chrome_service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

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
        time.sleep(2)
        driver.get(f"https://www.linkedin.com/search/results/people/?geoUrn=%5B102713980%5D&keywords={job_post}&origin=SWITCH_SEARCH_VERTICAL")
        

      
        driver.quit()
        
    except Exception as e:
        print("Failed to login to LinkedIn.")
        print(e)
        

# linkedin_post("domovag725@kwalah.com", "Domvag@@1234", content)