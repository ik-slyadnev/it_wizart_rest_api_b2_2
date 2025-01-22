class LoginHelper:
    def __init__(self, dm_api_facade):
        self.dm_api_facade = dm_api_facade

    def login(self, login: str, password: str):
        response = self.dm_api_facade.login_api.post_v1_account_login(
            login=login,
            password=password
        )
        return response
