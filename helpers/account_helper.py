import json
from faker import Faker

fake = Faker()

class AccountHelper:
    def __init__(self, dm_api_facade, mailhog_facade):
        self.dm_api_facade = dm_api_facade
        self.mailhog_facade = mailhog_facade

    def register_new_user(self, login: str = None, email: str = None, password: str = None):
        """
        Регистрация нового пользователя с активацией аккаунта через email

        :param login: Логин пользователя (если не указан, генерируется автоматически)
        :param email: Email пользователя (если не указан, генерируется автоматически)
        :param password: Пароль пользователя (если не указан, генерируется автоматически)
        :return: dict с данными пользователя (login, email, password)
        """
        user_data = {
            'login': login or fake.user_name(),
            'email': email or fake.email(),
            'password': password or fake.password()
        }

        self.register_account(**user_data)
        token = self.get_registration_token(user_data['login'])
        self.activate_account(token)

        return user_data

    def register_account(self, login: str, email: str, password: str):
        """
        Регистрация аккаунта пользователя
        """
        response = self.dm_api_facade.account_api.post_v1_account(
            login=login,
            email=email,
            password=password
        )
        assert response.status_code == 201, f"Не удалось зарегистрировать пользователя {login}"

    def get_registration_token(self, login: str) -> str:
        """
        Получение токена активации из почты
        """
        messages = self.mailhog_facade.mailhog_api.get_api_v2_messages(limit=1)
        token = None
        for item in messages['items']:
            message_data = json.loads(item['Content']['Body'])
            user_login = message_data['Login']
            if user_login == login:
                token = message_data['ConfirmationLinkUrl'].split('/')[-1]
                break

        assert token is not None, f"Токен для пользователя {login} не был получен"
        return token

    def activate_account(self, token: str):
        """
        Активация аккаунта по токену
        """
        response = self.dm_api_facade.account_api.put_v1_account_token(token)
        assert response.status_code == 200, f"Не удалось активировать аккаунт"
