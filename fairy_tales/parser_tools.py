import random
import re
import time

import numpy as np
import pandas as pd
import requests
from selenium.webdriver.common.by import By
from tqdm import tqdm


def extract_info(tails, driver):
    # save the original tab id
    prime_tab = driver.current_window_handle

    names = []
    authors = []
    descriptions = []
    time_reads = []
    tail_texts = []
    tags_all = []

    for tail in tqdm(tails):
        tail.click()
        driver.implicitly_wait(5)

        # go to new tab
        for window_handle in driver.window_handles:
            if window_handle != prime_tab:
                driver.switch_to.window(window_handle)
                break

        driver.implicitly_wait(5)
        curr_url = driver.current_url
        time.sleep(1)
        request_page = requests.get(curr_url)
        time.sleep(2)

        if request_page.status_code != 404:
            name = driver.find_element(By.CLASS_NAME, "hdr")
            author = np.nan

            if len(name.text.split("\n")) == 2:
                author = name.text.split("\n")[1]
                name = name.text.split("\n")[0]
            else:
                name = name.text

            description = driver.find_elements(By.CLASS_NAME, "cont.si-text")

            if len(description) == 0:
                # close the tab
                driver.close()

                # switch back to the old tab
                driver.switch_to.window(prime_tab)
                continue

            description = description[0]
            time_read = driver.find_element(By.CLASS_NAME, "rtime")

            tail_text = driver.find_elements(
                By.CLASS_NAME, "tale-text.si-text"
            )
            tail_text = "\n".join([x.text for x in tail_text if x != ""])
            tail_text = (
                "\n".join(
                    [
                        x
                        for x in tail_text.split("\n")
                        if x
                        not in ["Следущая глава", "Предыдущая глава", "\n", ""]
                    ]
                )
                + "\n\n"
            )
            tail_text_full = tail_text

            next_page = driver.find_elements(
                By.CLASS_NAME, "next.b-link.r-arrow"
            )

            while len(next_page) != 0:
                next_page = [
                    x for x in next_page if x.text == "Следущая глава"
                ][0]

                next_page.click()
                time.sleep(random.choice([1, 2]))

                tail_text = driver.find_elements(
                    By.CLASS_NAME, "tale-text.si-text"
                )
                tail_text = "\n".join([x.text for x in tail_text if x != ""])
                tail_text = (
                    "\n".join(
                        [
                            x
                            for x in tail_text.split("\n")
                            if x
                            not in [
                                "Следущая глава",
                                "Предыдущая глава",
                                "\n",
                                "",
                            ]
                        ]
                    )
                    + "\n\n"
                )

                tail_text_full += tail_text
                next_page = driver.find_elements(
                    By.CLASS_NAME, "next.b-link.r-arrow"
                )
                next_page = [
                    x for x in next_page if x.text == "Следущая глава"
                ]

            tags = driver.find_element(By.CLASS_NAME, "tale-cats")

            names.append(name)
            authors.append(author)
            descriptions.append(description.text)
            time_reads.append(time_read.text)
            tail_texts.append(tail_text_full)
            tags_all.append(
                re.sub(r"(\w)([А-Я])", r"\1; \2", tags.text.split("\n")[1])
            )

        # close the tab
        driver.close()

        # switch back to the old tab
        driver.switch_to.window(prime_tab)

    df = pd.DataFrame(
        {
            "name": names,
            "author": authors,
            "description": descriptions,
            "time_read": time_reads,
            "tail_text": tail_texts,
            "tags": tags_all,
        }
    )

    return df
