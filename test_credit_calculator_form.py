import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# --- Константы ---
STEP_DELAY = 1.5
AMOUNT = "1000000"          # Желаемая сумма кредита
INCOME = "300000"           # Доход
PAYMENT = "50000"           # Ежемесячные платежи
OVERDUE_VALUE = "0"         # Просрочки: "0" = Отсутствуют
ARREST_VALUE = "none"       # Ограничения/аресты: "none" = Нет арестов

@pytest.mark.usefixtures("open_calculator_page")
def test_credit_calculator_form(open_calculator_page):
    browser = open_calculator_page
    wait = WebDriverWait(browser, 20)
    time.sleep(STEP_DELAY)

    # --- Поля суммы / дохода / платежей ---
    amount_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Например: 1 000 000 тенге']"))
    )
    amount_input.clear()
    amount_input.send_keys(AMOUNT)
    time.sleep(STEP_DELAY)

    inputs = browser.find_elements(By.XPATH, "//input[contains(@placeholder,'тенге')]")
    assert len(inputs) >= 3, f"Ожидали минимум 3 input с 'тенге', нашли {len(inputs)}"

    income_input = inputs[1]
    income_input.clear()
    income_input.send_keys(INCOME)
    time.sleep(STEP_DELAY)

    payment_input = inputs[2]
    payment_input.clear()
    payment_input.send_keys(PAYMENT)
    time.sleep(STEP_DELAY)

    # --- Селекты: просрочки и ограничения/аресты ---
    selects = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//select[contains(@class,'border-green-300')]"))
    )
    assert len(selects) >= 2, "Не найдено двух селектов с классом 'border-green-300'"

    overdue_select = Select(selects[0])
    overdue_select.select_by_value(OVERDUE_VALUE)
    time.sleep(STEP_DELAY)

    arrest_select = Select(selects[1])
    arrest_select.select_by_value(ARREST_VALUE)
    time.sleep(STEP_DELAY)

    # --- Кнопка "Рассчитать" ---
    calc_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Рассчитать')]"))
    )

    # Ждём, пока кнопка станет активной (disabled исчезнет)
    wait.until(lambda driver: calc_btn.is_enabled())

    calc_btn.click()
    time.sleep(STEP_DELAY)

    # --- Проверка результата ---
    result_block = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//div[contains(@class,'result') or contains(text(),'Ежемесячный платеж')]"
        ))
    )
    assert result_block.is_displayed(), "Блок с результатами калькулятора не появился!"

    print("✅ Тест успешно прошёл: форма заполнена, кнопка 'Рассчитать' нажата, результат появился.")
