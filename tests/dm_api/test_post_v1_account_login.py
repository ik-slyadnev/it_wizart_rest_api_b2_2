

class TestPostV1AccountLogin:
    def test_post_v1_account_login(self, account_helper, login_helper):
        # Регистрация и активация пользователя через хелпер
        user_data = account_helper.register_new_user()

        # Авторизация пользователя через login_helper
        response = login_helper.login(
            login=user_data['login'],
            password=user_data['password']
        )
        assert response.status_code == 200, "Не удалось авторизоваться"
