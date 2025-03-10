from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
import json
import time
import random

def parser(url):
    products_data = []
    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.get(url=url)
    time.sleep(3)
    try:
        elem = driver.find_element(By.CSS_SELECTOR, "button[class='base-button -large -secondary "
                                                           "-shadow -full-width kCsyDn']")
        while elem:
            time.sleep(random.randint(2, 5))
            elem.click()
            products = driver.find_elements(By.CSS_SELECTOR, "div[class='dGMJLz fSNq2j Ppy5qY LXySrk']")
            for prod in products:
                name = prod.find_element(By.CSS_SELECTOR, "span[class='typography text v2 -no-margin']").text
                try:
                    price = prod.find_element(By.CSS_SELECTOR, "p[class='typography heading v5 -no-margin "
                                                            "GJ7gDd _6CwlGT']").text.replace("\xa0", "")
                except NoSuchElementException:
                    price = "Не найденo"

                link = prod.find_element(By.CSS_SELECTOR, "a[class='-dp5Dd clamp-3 buZF02']").get_attribute("href")
                products_data.append({"Наименование": name, "Цена": price, "Ссылка": link})
    except Exception as e:
        print("Ошибка:", e)
    finally:
        with open('products.json', 'w', encoding='utf-8') as json_file:
            json.dump(products_data, json_file, ensure_ascii=False, indent=4)
        driver.quit()




if __name__ == "__main__":
    url = "https://www.vseinstrumenti.ru/category/bezudarnye-akkumulyatornye-dreli-shurupoverty-16/page1/"
    parser(url)
