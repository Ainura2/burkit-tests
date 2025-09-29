import pytest
import requests

BASE_URL = "https://online.burkit.kz/bitrix.php"  # твой реальный endpoint
def test_dummy():
    assert 1 == 1
@pytest.fixture
def test_payload():
    return {
        "name": "Тестовый пользователь",
        "phone": "+77001234567",
        "iin": "123456789012",
        "language": "Русский",
        "overdue": 0,
        "arrest": False,
        "cityId": 1,
        "city_id": 1,
        "loanType": "Потребительский",
        "requiredAmount": 500000,
        "income": 200000,
        "maxAmount": 1000000,
        "monthlyPayment": 50000,
        "appointmentDate": "2025-09-25",
        "appointmentTime": "10:00",
        "utm_source": "test",
        "utm_medium": "test",
        "utm_campaign": "test",
        "utm_content": "test",
        "utm_term": "test",
    }

def test_application_send_success(test_payload):
    headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.post(BASE_URL, json=test_payload, headers=headers)

    # Проверяем что сервер ответил 200
    assert response.status_code == 200

    # Проверяем JSON
    data = response.json()
    assert "success" in data

    if data["success"]:
        print("✅ Заявка успешно отправлена:", data)
    else:
        pytest.fail(f"❌ Ошибка при отправке: {data}")
