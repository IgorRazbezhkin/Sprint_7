import requests
import random
from helpers import login_courier
import data
import urls
import allure


class TestCourierLogin:

    @allure.title("Успешная авторизация курьера.")
    @allure.description("Тест для проверки успешной авторизации созданного курьера.")
    @allure.link(urls.api_documentation, name="API документация")

    def test_courier_can_authorize_success(self, created_courier_with_id):
        with allure.step("Получить логин и пароль созданного курьера."):
            login = created_courier_with_id['login']
            password = created_courier_with_id['password']

        with allure.step("Отправить запрос на авторизацию курьера."):
            response = login_courier(login, password)

        with allure.step("Проверить код и тело ответа."):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Получение ошибки при авторизации без поля login и password.")
    @allure.description("Тест для проверки получения ошибки при попытке авторизации без одного из обязательных полей login и password.")
    @allure.link(urls.api_documentation, name="API документация")

    def test_authorization_requires_all_fields_received_an_error(self, created_courier_with_id):
        with allure.step("Получить логин и пароль созданного курьера."):
            login = created_courier_with_id['login']
            password = created_courier_with_id['password']

        with allure.step("Отправить запрос на авторизацию без логина."):
            response_no_login = requests.post(
                urls.endpoints['login_courier'],
                json={"login": "", "password": password}
            )
        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response_no_login.status_code == 400
            assert response_no_login.json()["message"] == data.error_massages['missing_login_or_password']

        with allure.step("Отправить запрос на авторизацию без пароля."):
            response_no_password = requests.post(
                urls.endpoints['login_courier'],
                json={"login": login, "password": ""}
            )
        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response_no_password.status_code == 400
            assert response_no_password.json()["message"] == data.error_massages['missing_login_or_password']

    @allure.title("Получение ошибки при авторизации c неправильным полем login и password.")
    @allure.description("Тест для проверки получения ошибки при попытке авторизации с неправильными полями login и password.")
    @allure.link(urls.api_documentation, name="API документация")

    def test_wrong_login_or_password_returns_error_received_an_error(self, created_courier_with_id):
        with allure.step("Получить логин и пароль созданного курьера."):
            login = created_courier_with_id['login']
            password = created_courier_with_id['password']

        with allure.step("Отправить запрос на авторизацию с неправильным логином."):
            response_wrong_login = requests.post(
                urls.endpoints['login_courier'],
                json={"login": "wrong_login", "password": password}
            )
        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response_wrong_login.status_code == 404
            assert response_wrong_login.json()["message"] == data.error_massages['account_not_found']

        with allure.step("Отправить запрос на авторизацию с неправильным паролем."):
            response_wrong_password = requests.post(
                urls.endpoints['login_courier'],
                json={"login": login, "password": "wrong_password"}
            )
        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response_wrong_password.status_code == 404
            assert response_wrong_password.json()["message"] == data.error_massages['account_not_found']

    @allure.title("Получение ошибки при авторизации несуществующим курьером.")
    @allure.description("Тест для проверки получения ошибки при попытке авторизоваться несуществующим курьером.")
    @allure.link(urls.api_documentation, name="API документация")

    def test_login_with_nonexistent_user_returns_error_received_an_error(self, created_courier_with_id):
        with allure.step("Получить пароль созданного курьера."):
            password = created_courier_with_id['password']

        with allure.step("Создать рандомный логин."):
            random_login = f"nonexistent_{random.randint(2, 10)}"

        with allure.step("Отправить запрос на авторизацию с несуществующим логином."):
            response = requests.post(
                urls.endpoints['login_courier'],
                json={"login": random_login, "password": password}
            )

        with allure.step("Проверить код и сообщение об ошибке ответа."):
            assert response.status_code == 404
            assert response.json()["message"] == data.error_massages['account_not_found']