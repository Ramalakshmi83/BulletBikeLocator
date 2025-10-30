from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

print("🏍️ Starting Bullet Bike Showroom Locator...")

# Step 1: Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Step 2: Open Google Maps
driver.get("https://www.google.com/maps")
time.sleep(3)

# Step 3: Search for Bullet Bike Showrooms
search_box = driver.find_element(By.ID, "searchboxinput")
search_box.send_keys("Bullet Bike Showroom near me")
search_button = driver.find_element(By.ID, "searchbox-searchbutton")
search_button.click()
time.sleep(5)

# Step 4: Scrape showroom details
names, ratings, addresses = [], [], []

showrooms = driver.find_elements(By.CLASS_NAME, "Nv2PK")

for s in showrooms:
    try:
        name = s.find_element(By.CLASS_NAME, "qBF1Pd-fontHeadlineSmall").text
        rating = s.find_element(By.CLASS_NAME, "MW4etd").text if s.find_elements(By.CLASS_NAME, "MW4etd") else "No rating"
        address = s.find_element(By.CLASS_NAME, "W4Efsd").text if s.find_elements(By.CLASS_NAME, "W4Efsd") else "No address"
        names.append(name)
        ratings.append(rating)
        addresses.append(address)
    except:
        continue

# Step 5: Save data to CSV
df = pd.DataFrame({
    "Showroom Name": names,
    "Rating": ratings,
    "Address": addresses
})
df.to_csv("showrooms.csv", index=False)
print(" Data saved to showrooms.csv successfully!")

driver.quit()
