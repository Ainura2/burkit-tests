import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_form_elements(browser):
    browser.get("https://burkit.kz/ru/")
    time.sleep(3)  # ждём загрузку страницы

    # Поле "Имя"
    name_input = browser.find_element(By.NAME, "name")
    assert name_input.is_displayed()
    print("Поле 'Имя' найдено ✅")
    time.sleep(2)

    # Поле "Телефон"
    phone_input = browser.find_element(By.NAME, "phone")
    assert phone_input.is_displayed()
    print("Поле 'Телефон' найдено ✅")
    time.sleep(2)

    # Поле "ИИН"
    iin_input = browser.find_element(By.NAME, "iin")
    assert iin_input.is_displayed()
    print("Поле 'ИИН' найдено ✅")
    time.sleep(2)

    # Селект "Город"
    city_select = Select(browser.find_element(By.NAME, "city_id"))
    assert city_select is not None
    print("Поле 'Город' найдено ✅")
    time.sleep(2)

    # Чекбокс "Согласие"
    agree_checkbox = browser.find_element(By.ID, "agree")
    assert agree_checkbox.is_displayed()
    print("Чекбокс 'Согласие' найден ✅")
    time.sleep(2)

    # Кнопка "Получить кредит"
    submit_button = browser.find_element(By.CSS_SELECTOR, "button.submit-button")
    assert submit_button.is_displayed()
    print("Кнопка 'Получить кредит' найдена ✅")
    time.sleep(2)
