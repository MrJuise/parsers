from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
import json
import time
import random
import os


def load_existing_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return {}


def extract_text(element, xpath):
    try:
        return element.find_element(By.XPATH, xpath).text
    except NoSuchElementException:
        return None


def parser(url):
    all_courier_data = load_existing_data('data_courier.json')
    unique_numbers = {item.get('number') for item in all_courier_data.values() if 'number' in item}
    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)

    try:
        driver.get(url=url)
        time.sleep(3)

        driver.find_element(By.NAME, "authLogin").send_keys("xxx")
        driver.find_element(By.NAME, "password").send_keys("xxx")
        driver.find_element(By.CSS_SELECTOR, "button[elmabutton='primary']").click()
        time.sleep(random.randint(7, 15))

        driver.find_element(By.CSS_SELECTOR, "a[href='hiring']").click()
        time.sleep(random.randint(7, 15))
        driver.find_element(By.CSS_SELECTOR, "a[href='/hiring/custom_task']").click()
        time.sleep(random.randint(7, 20))

        driver.find_element(By.XPATH, "//button[@class='search-control search-control_more btn btn-default"
                                      " btn-style-icon elma-icons']").click()
        time.sleep(random.randint(1, 3))
        driver.find_element(By.XPATH, "//span[text()='курьер']").click()
        time.sleep(random.randint(20, 45))

        while True:
            all_courier = driver.find_elements(By.XPATH, "//div[@class='md tile-item ng-star-inserted']")
            for courier in all_courier:
                city = extract_text(courier, ".//a[@class='last-item ng-star-inserted']")
                name = extract_text(courier,
                                    ".//span[text()='Имя']/following-sibling::app-appview-list-field/elma-type-string/span")
                surname = extract_text(courier,
                                       ".//span[text()='Фамилия']/following-sibling::app-appview-list-field/elma-type-string/span")
                number = extract_text(courier, ".//div[@class='ng-star-inserted']//a")

                if number:
                    number = number.strip()

                    if number not in unique_numbers:
                        unique_numbers.add(number)
                        record_id = len(all_courier_data) + 1
                        courier_data = {
                            "city": city,
                            "number": number,
                            "name": name,
                            "surname": surname
                        }
                        all_courier_data[record_id] = courier_data

            try:
                with open('data_courier.json', 'w', encoding='utf-8') as json_file:
                    json.dump(all_courier_data, json_file, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Ошибка при записи в файл: {e}")

            time.sleep(30)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    url = "https:/example.com/_login"
    parser(url)
