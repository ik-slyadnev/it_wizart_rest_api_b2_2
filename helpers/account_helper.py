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
        # Генерация данных пользователя, если они не предоставлены
        user_data = {
            'login': login or fake.user_name(),
            'email': email or fake.email(),
            'password': password or fake.password()
        }

        # Регистрация пользователя
        response = self.dm_api_facade.account_api.post_v1_account(**user_data)
        assert response.status_code == 201

        # Получение и активация токена
        response = self.mailhog_facade.mailhog_api.get_api_v2_messages(limit=str(1))
        assert response.status_code == 200

        messages = response.json()
        token = None
        for item in messages['items']:
            message_data = json.loads(item['Content']['Body'])
            user_login = message_data['Login']
            if user_login == user_data['login']:
                token = message_data['ConfirmationLinkUrl'].split('/')[-1]
                break

        assert token is not None, f"Токен для пользователя {user_data['login']} не был получен"

        # Активация аккаунта
        response = self.dm_api_facade.account_api.put_v1_account_token(token)
        assert response.status_code == 200

        return user_data
