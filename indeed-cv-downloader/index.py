# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/Library/Application Support/Google/Chrome"


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# ✅ Connect to already running Chrome session
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # Attach to open Chrome

# ✅ Use WebDriver Service
driver = webdriver.Chrome(service=Service("/opt/homebrew/bin/chromedriver"), options=options)

print("hello")

# ✅ Open Indeed Candidate Page
driver.get("https://employers.indeed.com/candidates/view?id=e4a2b7665167&l=BXOj&listQuery=aWQlM0Q2MmRmOTQ2NmVjOTAlMjZzdGF0dXNOYW1lJTNETmV3JTI2c2VsZWN0ZWRKb2JzJTNEYVhKcE9pOHZZWEJwY3k1cGJtUmxaV1F1WTI5dEwwVnRjR3h2ZVdWeVNtOWlMek16TkdZME5tVmtMV1ZtT1RrdE5HUTVNQzA0T0dZeExXTmhaV1ZtTjJNMU1qY3hPQSUyNTNEJTI1M0Q=&lName=nextPreviousCandidateList")
time.sleep(2)  # Wait for page to load

# ✅ Initialize WebDriverWait (waits up to 10 sec)
wait = WebDriverWait(driver, 2)

download_folder = os.path.expanduser("~/Downloads")



def wait_for_download(resume_name):
    file_path = os.path.join(download_folder, resume_name)
    timeout = 20  # Wait up to 20 seconds
    while timeout > 0:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"✅ Successfully downloaded: {resume_name}")
            return True
        time.sleep(1)
        timeout -= 1
    print(f"❌ Failed to download: {resume_name}")
    return False

while True:
    try:
        # ✅ Find the "Download Resume" Button (Wait until it's clickable)
        download_button = wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@data-testid, "download-resume-inline")]')))
        
        # ✅ Ensure the href is a valid blob URL before clicking
        resume_href = download_button.get_attribute("href")
        resume_name = download_button.get_attribute("download")

        if not resume_href.startswith("blob:"):
            print("⚠ Resume link is not valid yet, retrying...")
            time.sleep(2)
            continue  # Retry if href is not set properly

        print(f"✅ Downloading: {resume_name}")

        # ✅ Click the "Download Resume" button
        driver.execute_script("arguments[0].click();", download_button)

        # ✅ Wait for the download to complete
        if not wait_for_download(resume_name):
            print("⚠ Retrying download due to slow response...")
            time.sleep(2)
            continue  # Retry downloading

        # ✅ Click "Next Candidate" Button (Wait until clickable)
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "nextPreBlock-next")))
        next_button.click()
        print("➡ Moving to the Next Candidate...")

        # ✅ Wait for the next candidate to load
        time.sleep(2)

    except Exception as e:
        print("❌ No more candidates or error:", e)
        break  # Exit loop if no more candidates

# ✅ Close browser when done
print("🎉 All CVs Downloaded Successfully!")

# ✅ Keep browser open for manual checks
time.sleep(100000)
