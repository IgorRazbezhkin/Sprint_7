import requests
import urls
import data
import allure


class TestOrderAcceptance:

    @allure.title("Успешное принятие заказа курьером.")
    @allure.description("Тест для проверки успешного принятие заказа курьером с id курьера и заказа.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_accept_order_success(self, created_courier_with_id, create_order_and_get_id):
        with allure.step("Получить id созданного курьера и заказа."):
            courier = created_courier_with_id
            order = create_order_and_get_id

        with allure.step("Сформировать URL для принятия заказа."):
            url = urls.endpoints['order_accept'].format(order['order_id'])

        with allure.step("Подготовить параметры запроса с id курьера"):
            params = {"courierId": courier["id"]}

        with allure.step("Отправить запрос на принятие заказа."):
            response = requests.put(url, params=params)

        with allure.step("Проверить код и статус ответа."):
            assert response.status_code == 200
            assert response.json() == {"ok": True}

    @allure.title("Получение ошибки при принятии заказа без id курьера")
    @allure.description("Тест для проверки получения ошибки при принятии заказа без id курьера.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_accept_order_without_courier_id_received_an_error(self, created_courier_with_id, create_order_and_get_id):
        with allure.step("Получить id созданного заказа."):
            order = create_order_and_get_id

        with allure.step("Сформировать URL для принятия заказа без id курьера."):
            url = urls.endpoints['order_accept'].format(order['order_id'])

        with allure.step("Отправить запрос на принятие заказа без id курьера."):
            response = requests.put(url)

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response.status_code == 400
            assert response.json()['message'] == data.error_massages['not_enough_data_to_search']

    @allure.title("Получение ошибки при принятии заказа с несуществующим id курьера.")
    @allure.description("Тест для проверки получения ошибки при принятии заказа с несуществующим id курьера.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_accept_order_with_nonexistent_courier_id_received_an_error(self, created_courier_with_id, create_order_and_get_id):
        with allure.step("Получить id созданного заказа."):
            order = create_order_and_get_id

        with allure.step("Сформировать URL для принятия заказа с несуществующим id курьера."):
            url = urls.endpoints['order_accept'].format(order['order_id'])

        with allure.step("Отправить запрос на принятие заказа с несуществующим id курьера."):
            response = requests.put(url, params={"courierId": data.non_existent_number})

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response.status_code == 404
            assert response.json()['message'] == data.error_massages['no_courier_with_such_id']

    @allure.title("Получение ошибки при принятии заказа без id заказа.")
    @allure.description("Тест для проверки получения ошибки при принятии заказа без id заказа.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_accept_order_without_order_id_received_an_error(self, created_courier_with_id, create_order_and_get_id):
        with allure.step("Получить id созданного курьера."):
            courier = created_courier_with_id

        with allure.step("Сформировать URL для принятия заказа без id заказа."):
            url = f"{urls.base_url}/orders/accept"

        with allure.step("Отправить запрос на принятие заказа без id заказа."):
            response = requests.put(url, params={"courierId": courier["id"]})

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response.status_code == 404
            assert response.json()['message'] == data.error_massages['non_existent_id']

    @allure.title("Получение ошибки при принятии заказа с несуществующим id заказа.")
    @allure.description("Тест для проверки получения ошибки при принятии заказа с несуществующим id заказа.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_accept_order_with_invalid_order_id_received_an_error(self, created_courier_with_id, create_order_and_get_id):
        with allure.step("Получить id созданного курьера."):
            courier = created_courier_with_id

        with allure.step("Сформировать URL для принятия заказа с несуществующим id заказа."):
            url = urls.endpoints['order_accept'].format(data.non_existent_number)

        with allure.step("Отправить запрос на принятие заказа с несуществующим id заказа."):
            response = requests.put(url, params={"courierId": courier["id"]})

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response.status_code == 404
            assert response.json()['message'] == data.error_massages['no_order_with_such_id']