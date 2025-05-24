import requests
import urls
import data
import allure


class TestCourierDeletion:

    @allure.title("Успешное удаление курьера по существующему ID.")
    @allure.description("Тест для проверки успешного удаления курьера по существующему ID.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_delete_courier_success(self, created_courier_with_id):
        with allure.step("Получить ID созданного курьера курьера"):
            courier_id = created_courier_with_id['id']

        with allure.step("Сформировать URL для удаления курьера по ID"):
            response = requests.delete(urls.endpoints['delete_courier'].replace("{id}", str(courier_id)))

        with allure.step("Отправить запрос на удаление курьера"):
            response.raise_for_status()

        with allure.step("Проверить код и статус ответа."):
            assert response.status_code == 200
            assert response.json() == {"ok": True}

    @allure.title("Получение ошибки при удалении курьера без указания ID.")
    @allure.description("Тест для проверки получения ошибки при попытке удалить курьера без указания ID.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_delete_without_id_returns_error_received_an_error(self):
        with allure.step("Сформировать URL без {id} для удаления курьера"):
            url_without_id = urls.endpoints['delete_courier'].replace("/{id}", "")

        with allure.step("Отправить запрос на удаление курьера без ID"):
            response = requests.delete(url_without_id)

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response.status_code == 404
            json_resp = response.json()
            assert "message" in json_resp
            assert json_resp["message"] == data.error_massages['non_existent_id']

    @allure.title("Получение ошибки при удалении курьера с несуществующим ID.")
    @allure.description("Тест для проверки получения ошибки при попытке удалить курьера с несуществующим ID.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_delete_with_nonexistent_id_returns_error_received_an_error(self):
        with allure.step("Сформировать URL для удаления курьера с несуществующим ID"):
            delete_url = urls.endpoints['delete_courier'].replace("{id}", data.non_existent_number)

        with allure.step("Отправить запрос на удаление курьера с несуществующим ID"):
            response = requests.delete(delete_url)

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response.status_code == 404
            json_resp = response.json()
            assert "message" in json_resp
            assert json_resp["message"] == data.error_massages['without_id']