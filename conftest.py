import pytest
from common.logger import setup_logging
from configs.configuration import Configuration
from services.dm_api.dm_api_facade import DMApiAccount
from services.mailhog.mailhog_facade import MailHogAPI
from helpers.account_helper import AccountHelper

# Инициализация логгера при старте тестов
setup_logging()

@pytest.fixture
def config_data():
    """
    Конфигурация для API endpoints
    """
    return {
        'host': 'http://5.63.153.31:5051',
        'mailhog_host': 'http://5.63.153.31:5025'
    }

@pytest.fixture
def main_config(config_data):
    """
    disable_log:
        False - логирование запросов и ответов включено
        True - логирование запросов и ответов выключено
        По умолчанию установлено в True
    """
    return Configuration(
        host=config_data['host'],
        headers={
            'Content-Type': 'application/json'
        },
        disable_log=False
    )

@pytest.fixture
def mailhog_config(config_data):
    return Configuration(
        host=config_data['mailhog_host'],
        disable_log=True  # логи отключены для mailhog
    )

# Фикстуры для фасадов
@pytest.fixture
def dm_api_facade(main_config):
    """
    Фасад для работы с DM API
    """
    return DMApiAccount(configuration=main_config)

@pytest.fixture
def mailhog_facade(mailhog_config):
    """
    Фасад для работы с Mailhog
    """
    return MailHogAPI(configuration=mailhog_config)

# Фикстуры хелперов
@pytest.fixture
def account_helper(dm_api_facade, mailhog_facade):
    """
    Хелпер для работы с аккаунтом, использует фасады
    """
    return AccountHelper(dm_api_facade, mailhog_facade)