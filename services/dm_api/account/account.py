from configs.rest_client import RestClient
from configs.configuration import Configuration

class AccountApi(RestClient):
    def post_v1_account(self, login: str, email: str, password: str):
        """
        Регистрация нового аккаунта.

        :param login: Логин пользователя
        :param email: Email пользователя
        :param password: Пароль пользователя
        :return: Response
        """
        payload = {
            "login": login,
            "email": email,
            "password": password
        }
        response = self.post(
            path="/v1/account",
            json=payload
        )
        return response

    def put_v1_account_token(self, token: str):
        """
        Активация аккаунта по токену.

        :param token: Токен активации
        :return: Response
        """
        response = self.put(
            path=f"/v1/account/{token}"
        )
        return response

    def put_v1_account_email(self, login: str, new_email: str, password: str):
        """
        Смена email пользователя.

        :param login: Логин пользователя
        :param password: Пароль пользователя
        :param new_email: Новый email пользователя
        :return: Response
        """
        payload = {
            "login": login,
            "email": new_email,
            "password": password
        }
        response = self.put(
            path="/v1/account/email",
            json=payload
        )
        return response
