import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def open_calculator_page(browser):
    """Фикстура: сначала подаем заявку, потом открываем калькулятор"""
    browser.get("https://online.burkit.kz/")

    wait = WebDriverWait(browser, 20)

    # Поле ИИН
    iin_input = wait.until(EC.presence_of_element_located((By.ID, "iin")))
    iin_input.send_keys("123456789012")

    # Поле телефон
    phone_input = wait.until(EC.presence_of_element_located((By.ID, "phone")))
    phone_input.send_keys("+7474552739")

    # Выбор города
    from selenium.webdriver.support.ui import Select
    city_select = Select(wait.until(EC.presence_of_element_located((By.ID, "city"))))
    city_select.select_by_visible_text("Алматы - Айтеке би 123/1")

    # Тип кредита
    loan_type = Select(wait.until(EC.presence_of_element_located((By.ID, "loanType"))))
    loan_type.select_by_value("express")

    # Чек-бокс согласия
    consent_label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[@for='consent']")))
    consent_label.click()

    # Кнопка "Подать заявку"
    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Подать заявку')]")))
    submit_btn.click()

    # Ждём, когда загрузится страница калькулятора
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'тенге')]")))

    return browser
