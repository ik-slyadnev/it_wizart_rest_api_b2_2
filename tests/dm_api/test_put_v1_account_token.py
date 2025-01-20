import json
from faker import Faker

fake = Faker()


class TestPutV1AccountToken:
    def test_put_v1_account_token(self, dm_api_facade, mailhog_facade):
        """
        Тест проверяет активацию аккаунта по токену

        Шаги:
        1. Регистрация нового пользователя
        2. Получение письма с токеном активации
        3. Активация аккаунта с помощью токена
        """
        # Регистрация пользователя
        user_data = {
            'login': fake.user_name(),
            'email': fake.email(),
            'password': fake.password()
        }
        response = dm_api_facade.account_api.post_v1_account(**user_data)
        assert response.status_code == 201, "Регистрация пользователя не прошла"

        messages = mailhog_facade.mailhog_api.get_api_v2_messages(limit='1')
        assert messages['total'] > 0, "Письма не были получены"

        token = None
        for item in messages['items']:
            message_data = json.loads(item['Content']['Body'])
            user_login = message_data['Login']
            if user_login == user_data['login']:
                token = message_data['ConfirmationLinkUrl'].split('/')[-1]
                break

        assert token is not None, f"Токен для пользователя {user_data['login']} не был получен"

        response = dm_api_facade.account_api.put_v1_account_token(token)
        assert response.status_code == 200, "Не удалось активировать аккаунт"
