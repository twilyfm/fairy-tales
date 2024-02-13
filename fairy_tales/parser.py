import random
import time

from parser_tools import extract_info
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option(
    "prefs",
    {
        # block image loading
        "profile.managed_default_content_settings.images": 2,
    },
)

driver = webdriver.Chrome(options=options)
url = "https://nukadeti.ru/skazki"

driver.get(url)
driver.implicitly_wait(4)

tails = driver.find_elements(By.CLASS_NAME, "title")
iteration = 0

while len(tails) % 20 == 0:
    print(f"iteration {iteration} -- {len(tails)} fairy tales")

    df = extract_info(tails[-20:], driver)

    if iteration == 0:
        df.to_csv("data/fairy_tales.csv", index=False)
    else:
        df.to_csv("data/fairy_tales.csv", mode="a", index=False, header=False)

    iteration += 1

    show_more_button = driver.find_element(By.CLASS_NAME, "show-more.blue-bt")
    show_more_button.click()
    time.sleep(random.choice([1, 2, 3, 4]))

    tails = driver.find_elements(By.CLASS_NAME, "title")
    time.sleep(random.choice([1, 2, 3, 4]))

driver.close()
driver.quit()
