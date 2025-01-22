from common.rest_client import RestClient

class LoginApi(RestClient):
    def post_v1_account_login(self, login: str, password: str, remember_me: bool = True):
        """
        Авторизация пользователя

        :param login: Логин пользователя
        :param password: Пароль пользователя
        :param remember_me: Флаг запоминания сессии
        :return: Response
        """
        payload = {
            "login": login,
            "password": password,
            "rememberMe": remember_me
        }
        response = self.post(
            path="/v1/account/login",
            json=payload
        )
        return response
