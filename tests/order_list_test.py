import requests
import urls
import allure


@allure.title("Получение списка заказов")
@allure.description("Тест для проверки получения списка заказов.")
@allure.link(urls.api_documentation, name='API документация')

class TestOrders:

    def test_get_orders_list_returns_list_success(self):
        with allure.step("Отправить запрос на получение списка заказов"):
            response = requests.get(urls.endpoints['create_order'])

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, f"Некорректный статус: {response.status_code}, тело: {response.text}"

        with allure.step("Обработка ответа"):
            json_body = response.json()

        with allure.step("Проверка наличия ключа 'orders' в ответе"):
            assert "orders" in json_body, "В ответе отсутствует ключ 'orders'"

        with allure.step("Проверка, что 'orders' является не пустым списком"):
            orders = json_body["orders"]
            assert isinstance(orders, list), "'orders' не является списком"
            assert len(orders) > 0, "Список 'orders' пустой"