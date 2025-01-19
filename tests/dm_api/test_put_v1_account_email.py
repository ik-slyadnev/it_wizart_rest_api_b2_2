from faker import Faker

fake = Faker()

class TestPutV1AccountEmail:
    def test_put_v1_account_email(self, account_helper, dm_api_facade):
        # Регистрация и активация пользователя через хелпер
        user_data = account_helper.register_new_user()

        # Смена email
        new_email = fake.email()
        response = dm_api_facade.account_api.put_v1_account_email(
            login=user_data['login'],
            new_email=new_email,
            password=user_data['password']
        )
        assert response.status_code == 200
