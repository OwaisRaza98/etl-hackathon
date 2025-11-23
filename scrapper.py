import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# -------------------------
# Setup Chrome Driver
# -------------------------
driver_path = r"E:\chromedriver-win64\chromedriver.exe"
options = Options()
options.headless = False
service = Service(driver_path)

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

# -------------------------
# All Main Categories (5)
# -------------------------
main_categories = [
    "https://www.banggood.com/Wholesale-Sports-and-Outdoors-ca-6001.html?bid=210702&from=nav",
    "https://www.banggood.com/Wholesale-Tools,Industrial-and-Scientific-ca-3001.html?bid=210703&from=nav",
    "https://www.banggood.com/Wholesale-Phones-and-Accessories-ca-1001.html?bid=210706&from=nav"
]

all_products = []

# -------------------------
# Loop through each main category
# -------------------------
for main_url in main_categories:
    print(f"\nProcessing Main Category: {main_url}")
    driver.get(main_url)
    time.sleep(5)

    # Collect subcategory links
    subcategory_links = []
    subcategories = driver.find_elements(By.CSS_SELECTOR, ".nav a.exclick")

    for sub in subcategories:
        link = sub.get_attribute("href")
        if link and link.startswith("http"):
            subcategory_links.append(link)

    print(f"Found {len(subcategory_links)} subcategories.")

    # -------------------------
    # Scrape Each Subcategory
    # -------------------------
    for url in subcategory_links:
        print(f"  Scraping Subcategory: {url}")
        driver.get(url)
        time.sleep(3)

        # Infinite scroll to load all products
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Extract products
        products = driver.find_elements(By.CSS_SELECTOR, ".p-wrap")

        for item in products:
            try:
                title = item.find_element(By.CSS_SELECTOR, "a.title").get_attribute("title")
            except:
                title = None

            try:
                price = item.find_element(By.CSS_SELECTOR, ".price").text
            except:
                price = None

            try:
                rating = item.find_element(By.CSS_SELECTOR, ".reivew-box .review-text").text
            except:
                rating = None

            try:
                reviews = item.find_element(By.CSS_SELECTOR, ".prd-sold-review a.review").text
            except:
                reviews = None

            try:
                link = item.find_element(By.CSS_SELECTOR, "a.title").get_attribute("href")
            except:
                link = None

            all_products.append({
                "main_category": main_url,
                "subcategory": url,
                "title": title,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "url": link
            })

# close driver
driver.quit()

# -------------------------
# DONE
# -------------------------
print(f"\nTotal Products Scraped: {len(all_products)}")
for p in all_products:
    print(p)

df = pd.DataFrame(all_products)
df.to_csv("banggood_products_data.csv", index=False, encoding="utf-8-sig")
print("CSV SAVED")