import data
from helpers import generate_login, generate_password, create_courier
import urls
import allure


class TestCourierCreation:

    @allure.title("Успешное создание курьера.")
    @allure.description("Тест для проверки успешного создания нового курьера.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_create_courier_success(self, courier_data):
        with allure.step("Отправить запрос на создание курьера."):
            response = create_courier(courier_data)

        with allure.step("Проверить код и статус ответа."):
            assert response.status_code == 201
            assert response.json() == {"ok": True}

    @allure.title("Получение ошибки при создании двух курьеров с одним логином")
    @allure.description("Тест для проверки получения ошибки при создании двух курьеров с одинаковым логином.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_create_duplicate_courier_error_in_response_received_an_error(self, courier_data):
        with allure.step("Отправить запрос на создание первого курьера."):
            response1 = create_courier(courier_data)

        with allure.step("Проверить код и статус ответа."):
            assert response1.status_code == 201
            assert response1.json() == {"ok": True}

        with allure.step("Отправить запрос на создание второго курьера с тем же логином."):
            response2 = create_courier(courier_data)

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response2.status_code == 409
            assert response2.json()["message"] == data.error_massages['login_is_in_use']

    @allure.title("Получение ошибки при создание курьера с пропущенными полем password.")
    @allure.description("Тест для проверки возникновения ошибки при попытке создать курьера без обязательного поля с паролем.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_create_courier_missing_fields_error_in_response_received_an_error(self):
        with allure.step("Собрать тело запроса без пароля."):
            data_missing_password = {
                "login": generate_login(),
                "firstName": data.courier_first_name
            }

        with allure.step("Отправить запрос на создание курьера без пароля."):
            response = create_courier(data_missing_password)

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response.status_code == 400
            assert response.json()["message"] == data.error_massages['missing_data']

    @allure.title("Получение ошибки при создание курьера с пропущенными полем login.")
    @allure.description("Тест для проверки возникновения ошибки при попытке создать курьера без обязательного поля с логином.")
    @allure.link(urls.api_documentation, name='API документация')

    def test_create_courier_missing_login_error_in_response_received_an_error(self):
        with allure.step("Собрать тело запроса без логина."):
            data_missing_login = {
                "password": generate_password(),
                "firstName": data.courier_first_name
            }

        with allure.step("Отправить запрос на создание курьера без логина."):
            response = create_courier(data_missing_login)

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response.status_code == 400
            assert response.json()["message"] == data.error_massages['missing_data']