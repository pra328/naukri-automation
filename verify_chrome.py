from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
opts = webdriver.ChromeOptions()
opts.binary_location = chrome
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--window-size=1920,1080")
opts.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
print("OK")
driver.quit()
