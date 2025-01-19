

class TestPostV1Account:
    def test_post_v1_account(self, account_helper):
        """
        Тест проверяет успешную регистрацию нового пользователя
        """
        user_data = account_helper.register_new_user()

        assert isinstance(user_data, dict)
