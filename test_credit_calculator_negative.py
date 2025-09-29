import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# --- Константы ---
STEP_DELAY = 3.5   # увеличил задержку для наглядности
AMOUNT = "1000000"
INCOME = "300000"
PAYMENT = "50000"

@pytest.mark.usefixtures("open_calculator_page")
class TestCreditCalculatorNegative:

    def fill_common_fields(self, browser, wait):
        """Заполняет сумму, доход и платежи"""
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

        return browser.find_elements(By.XPATH, "//select[contains(@class,'border-green-300')]")

    def check_reject_message(self, browser, wait):
        """Проверяет, что появилось сообщение 'Отказано'"""
        reject_msg = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Отказано банками')]"))
        )

        # Скроллим к блоку результата
        browser.execute_script("arguments[0].scrollIntoView(true);", reject_msg)
        time.sleep(2)  # ждём чтобы увидеть блок

        assert "Отказано" in reject_msg.text, f"Сообщение об отказе не найдено! Было найдено: {reject_msg.text}"
        print(f"✅ Найдено сообщение об отказе: {reject_msg.text}")

    def test_with_overdue(self, open_calculator_page):
        """Негативный сценарий: наличие просрочек"""
        browser = open_calculator_page
        wait = WebDriverWait(browser, 20)
        time.sleep(STEP_DELAY)

        selects = self.fill_common_fields(browser, wait)

        overdue_select = Select(selects[0])
        overdue_select.select_by_value("30+")  # выбираем "Более 30 дней"
        time.sleep(STEP_DELAY)

        arrest_select = Select(selects[1])
        arrest_select.select_by_value("none")
        time.sleep(STEP_DELAY)

        calc_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Рассчитать')]")))
        wait.until(lambda driver: calc_btn.is_enabled())
        calc_btn.click()
        time.sleep(STEP_DELAY)

        self.check_reject_message(browser, wait)

    def test_with_arrest(self, open_calculator_page):
        """Негативный сценарий: наличие арестов"""
        browser = open_calculator_page
        wait = WebDriverWait(browser, 20)
        time.sleep(STEP_DELAY)

        selects = self.fill_common_fields(browser, wait)

        overdue_select = Select(selects[0])
        overdue_select.select_by_value("0")  # просрочек нет
        time.sleep(STEP_DELAY)

        arrest_select = Select(selects[1])
        arrest_select.select_by_value("account-arrest")  # есть аресты счетов
        time.sleep(STEP_DELAY)

        calc_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Рассчитать')]")))
        wait.until(lambda driver: calc_btn.is_enabled())
        calc_btn.click()
        time.sleep(STEP_DELAY)

        self.check_reject_message(browser, wait)
