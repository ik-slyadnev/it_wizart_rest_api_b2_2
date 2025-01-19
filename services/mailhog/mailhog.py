from configs.rest_client import RestClient

class MailhogApi(RestClient):
    def get_api_v2_messages(self, limit: str = '2'):
        """
        Получение писем пользователей

        :param limit: Количество писем
        :return: Response
        """
        params = {
            'limit': limit
        }
        response = self.get(
            path="/api/v2/messages",
            params=params
        )
        return response
