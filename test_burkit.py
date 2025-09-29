import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# фикстура для браузера
@pytest.fixture
def browser():
    service = Service("C:\\drivers\\chromedriver.exe")  # путь к chromedriver
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()  # закрываем браузер после теста

def test_open_burkit(browser):
    # открываем сайт
    browser.get("https://online.burkit.kz/")

    # проверяем, что заголовок страницы не пустой
    assert browser.title != ""

    # (пример проверки элемента — по желанию можно убрать)
    assert browser.find_element(By.TAG_NAME, "body")
