import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

STEP_DELAY = 2  # задержка между шагами (в секундах)

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()  # закрываем браузер после теста

def test_send_application(browser):
    browser.get("https://online.burkit.kz/")
    wait = WebDriverWait(browser, 20)

    # Поле ИИН
    iin_input = wait.until(EC.presence_of_element_located((By.ID, "iin")))
    iin_input.send_keys("123456789012")
    time.sleep(STEP_DELAY)

    # Поле телефон
    phone_input = wait.until(EC.presence_of_element_located((By.ID, "phone")))
    phone_input.send_keys("+7474552739")
    time.sleep(STEP_DELAY)

    # Выбор города
    city_select = Select(wait.until(EC.presence_of_element_located((By.ID, "city"))))
    city_select.select_by_visible_text("Алматы - Айтеке би 123/1")
    time.sleep(STEP_DELAY)

    # Выбор типа кредита
    loan_type = Select(wait.until(EC.presence_of_element_located((By.ID, "loanType"))))
    loan_type.select_by_value("express")
    time.sleep(STEP_DELAY)

    # Чек-бокс согласия
    consent_label = wait.until(EC.presence_of_element_located((By.XPATH, "//label[@for='consent']")))
    consent_label.click()
    time.sleep(STEP_DELAY)

    # Кнопка "Подать заявку"
    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Подать заявку')]")))
    submit_btn.click()
    time.sleep(STEP_DELAY)
