import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import string


options = Options()
options.add_argument("--start-maximized")


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)



def collect_all_disease_urls():
    disease_urls = set()
    
    for letter in string.ascii_lowercase:
        page = 1
        while True:
            url = f"https://www.1mg.com/all-diseases?label={letter}&page={page}"
            print(f"Visiting page {page}")
            driver.get(url)
            time.sleep(4)

            links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/diseases/']")
            if not links:
                break  

            for link in links:
                href = link.get_attribute("href")
                if href:
                    disease_urls.add(href)

            page += 1

    print(f"Total disease URLs collected: {len(disease_urls)}")
    return list(disease_urls)




def safe_text(by, value):
    try:
        return driver.find_element(by, value).text
    except:
        return None




def scrape_disease_page(url):
    driver.get(url)
    time.sleep(3)

    disease_name = safe_text(By.TAG_NAME, "h1")

    age_range = safe_text(
        By.XPATH, "//div[contains(text(),'Age')]/following-sibling::div"
    )

    gender = safe_text(
        By.XPATH, "//div[contains(text(),'Gender')]/following-sibling::div"
    )

    body_parts = safe_text(
        By.XPATH, "//div[contains(text(),'Body')]/following-sibling::div"
    )

    # Symptoms
    try:
        symptoms_list = driver.find_elements(
            By.XPATH, "//h2[contains(text(),'Symptoms')]/following-sibling::ul/li"
        )
        symptoms = ",".join([s.text for s in symptoms_list])
    except:
        symptoms = None

    # Treatment
    treatment = safe_text(
        By.XPATH, "//h2[contains(text(),'Treatment')]/following-sibling::p"
    )

    return {
        "disease_name": disease_name,
        "age_range": age_range,
        "gender": gender,
        "body_parts": body_parts,
        "symptoms": symptoms,
        "treatment": treatment
    }




all_urls = collect_all_disease_urls()

data = []

for idx, disease_url in enumerate(all_urls, start=1):
    print(f"[{idx}/{len(all_urls)}] Scraping...")
    record = scrape_disease_page(disease_url)
    record["url"] = disease_url
    data.append(record)






df = pd.DataFrame(data)
df.to_csv("final_disease_data.csv", index=False)
print("CSV file saved successfully!")
print(df)



