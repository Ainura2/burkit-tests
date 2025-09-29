import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException

# --- Константы ---
STEP_DELAY = 2
AMOUNT = "1000000"          # Желаемая сумма кредита
INCOME = "300000"           # Доход
PAYMENT = "50000"           # Ежемесячные платежи
OVERDUE_VALUE = "0"         # Просрочки: "0" = Отсутствуют
ARREST_VALUE = "none"       # Ограничения/аресты: "none" = Нет арестов

@pytest.mark.usefixtures("open_calculator_page")
def test_credit_reservation_process(open_calculator_page):
    browser = open_calculator_page
    wait = WebDriverWait(browser, 30)
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
    wait.until(lambda driver: calc_btn.is_enabled())  # ждём активность кнопки
    calc_btn.click()
    time.sleep(STEP_DELAY)

    # --- Ждём исчезновения лоудера (если он есть) ---
    try:
        wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'loader')]")))
        print("⏳ Лоудер исчез")
    except TimeoutException:
        print("⚠️ Лоудер не найден или не исчез, идём дальше")

    # --- Проверка текста об одобрении ---
    success_block = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//*[contains(text(),'Ваша заявка предодобрена') or contains(text(),'Поздравляем')]"
        ))
    )
    assert success_block.is_displayed(), "Сообщение об одобрении не отображается!"
    print("✅ Найден блок с текстом предодобрения")

    # --- Кнопка 'Поставить бронь на кредит без переплаты' ---
    reserve_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Поставить бронь')]"))
    )
    assert reserve_btn.is_displayed(), "Кнопка 'Поставить бронь' не отображается!"
    print("✅ Найдена кнопка 'Поставить бронь'")

    # --- Пауза для просмотра кнопки ---
    print("⏸ Ждём 4 секунд, чтобы увидеть кнопку перед кликом...")
    time.sleep(4)

    reserve_btn.click()
    print("👉 Кликнули по кнопке 'Поставить бронь на кредит без переплаты'")

    # --- Пауза после клика, чтобы увидеть результат ---
    time.sleep(5)

    # --- Проверка результата после клика ---
    try:
        alert = wait.until(EC.alert_is_present())
        print(f"🔔 Появился alert с текстом: {alert.text}")
        alert.accept()
        print("✅ Alert успешно закрыт")
    except TimeoutException:
        print("⚠️ Alert не появился")
    except UnexpectedAlertPresentException:
        print("⚠️ Alert появился внезапно, но тест его поймал")
