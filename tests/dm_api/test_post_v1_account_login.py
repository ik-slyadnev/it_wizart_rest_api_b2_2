

class TestPostV1AccountLogin:
    def test_post_v1_account_login(self, account_helper, dm_api_facade):
        # Регистрация и активация пользователя через хелпер
        user_data = account_helper.register_new_user()

        # Авторизация пользователя
        response = dm_api_facade.login_api.post_v1_account_login(
            login=user_data['login'],
            password=user_data['password'],
            remember_me=True
        )
        assert response.status_code == 200, "Не удалось авторизоваться"
