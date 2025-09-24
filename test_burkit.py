import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    # путь к chromedriver.exe
    driver = webdriver.Chrome(executable_path="C:\\drivers\\chromedriver.exe")
    yield driver
    driver.quit()

def test_open_burkit(browser):
    browser.get("https://burkit.kz/ru/")
    
    # Проверим, что заголовок страницы содержит слово "Burkit"
    assert "Burkit" in browser.title

    # Дополнительно: проверим, что есть кнопка "Войти"
    login_button = browser.find_element(By.LINK_TEXT, "Войти")
    assert login_button.is_displayed()
