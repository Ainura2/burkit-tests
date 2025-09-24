import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def browser():
    # Открываем Chrome
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_application_form(browser):
    browser.get("https://burkit.kz/ru/")

    # Имя
    name_input = browser.find_element(By.NAME, "name")
    name_input.send_keys("Тест")
    time.sleep(1)  # задержка после ввода

    # Телефон (вводим только цифры, маска сама подставит +7)
    phone_input = browser.find_element(By.NAME, "phone")
    phone_input.send_keys("77474552739")
    time.sleep(1)

    # ИИН (12 цифр)
    iin_input = browser.find_element(By.NAME, "iin")
    iin_input.send_keys("010101123456")
    time.sleep(1)

    # Город
    city_select = Select(browser.find_element(By.NAME, "city_id"))
    city_select.select_by_visible_text("Алматы, Айтеке Би 123/1")
    time.sleep(1)

    # Согласие (на всякий случай)
    agree_checkbox = browser.find_element(By.ID, "agree")
    if not agree_checkbox.is_selected():
        agree_checkbox.click()
    time.sleep(1)

    # Ждём пока кнопка станет кликабельной
    submit_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "submit-button"))
    )

    time.sleep(2)  # задержка перед нажатием кнопки
    submit_button.click()

    time.sleep(3)  # задержка после отправки формы, чтобы увидеть результат
