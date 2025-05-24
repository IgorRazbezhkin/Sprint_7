import pytest
import requests
import urls
import allure


@allure.title("Успешное создание заказа")
@allure.description("Тест для проверки создания заказа с разными комбинациями цветов.")
@allure.link(urls.api_documentation, name='API документация')

@pytest.mark.parametrize("colors", [
    (["BLACK"]),
    (["GREY"]),
    (["BLACK", "GREY"]),
    ([])
])
class TestOrderCreation:

    def test_create_order_with_various_colors_success(self, colors):
        with allure.step("Собрать тело запроса."):
            order_body = {
                "firstName": "Павел",
                "lastName": "Смородинов",
                "address": "Чернышевского д.82, кв. 6",
                "metroStation": "4",
                "phone": "+8 987 654 32 10",
                "rentTime": 5,
                "deliveryDate": "2020-06-06",
                "comment": "",
                "color": colors if len(colors) > 0 else None
            }
        if not order_body["color"]:
            del order_body["color"]

        with allure.step("Отправить запрос на создание заказа"):
            response = requests.post(urls.endpoints['create_order'], json=order_body)

        with allure.step("Проверить код и статус ответа."):
            assert response.status_code == 201, f"Некорректный статус: {response.status_code}, тело: {response.text}"

        with allure.step("Проверить наличие номера трека в ответе запроса"):
            response_json = response.json()
            assert 'track' in response_json and isinstance(response_json['track'], int), \
                f"В ответе отсутствует track или он не число: {response_json}"