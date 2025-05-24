import requests
import data
import urls
import allure


class TestGetOrderByTrack:

    @allure.title("Получение заказа по существующему треку")
    @allure.description("Тест для проверки успешного получение заказа по существующему треку.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_get_order_by_valid_track_success(self, create_order_and_get_id):
        with allure.step("Получить track и id созданного заказа."):
            track = create_order_and_get_id['track']
            order_id = create_order_and_get_id['order_id']

        with allure.step("Сформировать URL для получения заказа по треку."):
            url = urls.endpoints['track_order']

        with allure.step("Отправить запрос с существующим треком."):
            response = requests.get(url, params={"t": track})

        with allure.step("Проверить код ответа."):
            assert response.status_code == 200

        with allure.step("Обработка ответа."):
            response_json = response.json()

        with allure.step("Проверить наличия ключа 'orders' в ответе."):
            assert 'order' in response_json

        with allure.step("Проверить, что track и id в ответе совпадает с ожидаемым."):
            order = response_json['order']
            assert order['track'] == track
            assert order['id'] == order_id

    @allure.title("Получение ошибки при попытке получить заказ без трека заказа")
    @allure.description("Тест для проверки получения ошибки при отправке запроса без трека заказа.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_get_order_without_track_received_an_error(self):
        with allure.step("Сформировать URL для получения заказа без трека."):
            url = urls.endpoints['track_order']

        with allure.step("Отправить запрос без трека заказа."):
            response = requests.get(url)

        with allure.step("Обработка ответа."):
            response_json = response.json()

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response.status_code == 400
            assert response_json['message'] == data.error_massages['not_enough_data_to_search']

    @allure.title("Получение ошибки при попытке получить заказ по несуществующему треку")
    @allure.description("Тест для проверки получения ошибки при отправке запроса с несуществующим треком заказа.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_get_order_with_nonexistent_track_received_an_error(self):
        with allure.step("Сформировать URL для получения заказа с несуществующим треком."):
            url = urls.endpoints['track_order']

        with allure.step("Отправить запрос с несуществующим треком заказа."):
            response = requests.get(url, params={"t": data.non_existent_number})

        with allure.step("Обработка ответа."):
            response_json = response.json()

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response.status_code == 404
            assert response_json['message'] == data.error_massages['order_not_found']