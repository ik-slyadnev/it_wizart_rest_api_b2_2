

class TestPutV1AccountToken:
    def test_put_v1_account_token(self, account_helper):
        # Регистрация пользователя через хелпер, который автоматически активирует токен
        user_data = account_helper.register_new_user()
        assert isinstance(user_data, dict)
