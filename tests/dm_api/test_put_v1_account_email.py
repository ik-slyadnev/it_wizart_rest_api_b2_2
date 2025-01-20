import json

class TestPutV1AccountEmail:
    def test_put_v1_account_email(self, account_helper, dm_api_facade, mailhog_facade):
        """
        Тест на смену email пользователя

        Шаги:
        1. Регистрация и активация пользователя
        2. Логин в систему
        3. Смена email
        4. Проверка невозможности входа до подтверждения
        5. Получение и активация токена подтверждения
        6. Проверка возможности входа после подтверждения
        """

        user = account_helper.register_new_user()
        response = dm_api_facade.login_api.post_v1_account_login(
            login=user['login'],
            password=user['password']
        )
        assert response.status_code == 200

        new_email = f"new_{user['login']}@example.com"
        response = dm_api_facade.account_api.put_v1_account_email(
            login=user['login'],
            password=user['password'],
            new_email=new_email
        )
        assert response.status_code == 200


        response = dm_api_facade.login_api.post_v1_account_login(
            login=user['login'],
            password=user['password']
        )
        assert response.status_code == 403


        messages = mailhog_facade.mailhog_api.get_api_v2_messages(limit=1)
        email_change_token = None
        for item in messages['items']:
            message_data = json.loads(item['Content']['Body'])
            if message_data.get('Login') == user['login']:
                email_change_token = message_data['ConfirmationLinkUrl'].split('/')[-1]
                break

        assert email_change_token is not None, "Токен для смены email не найден"

        response = dm_api_facade.account_api.put_v1_account_token(token=email_change_token)
        assert response.status_code == 200

        response = dm_api_facade.login_api.post_v1_account_login(
            login=user['login'],
            password=user['password']
        )
        assert response.status_code == 200
