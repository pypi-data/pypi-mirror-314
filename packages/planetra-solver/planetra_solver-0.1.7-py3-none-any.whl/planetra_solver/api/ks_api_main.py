import os

import requests
import dotenv
from dotenv import load_dotenv

from planetra_solver.config import LOGIN, PASSWORD, URL_PREFIX, DOMAIN_NAME, PROJECT_UUID


dotenv_path = os.path.join("", "../../.env")
load_dotenv()

a_token = ''


class KsAPI:
    """Класс для взаимодействия с API платформы knowledge space"""

    def __init__(
            self,
            to_log_in: bool = False
    ):
        # Получаем токен аутентификации если нужно
        if not self._check_token() or to_log_in:
            data_with_token = self.request(
                '/auth/login',
                {"login": LOGIN, "password": PASSWORD}
            )
            token = data_with_token["token"]
            self._save_token(token)

    def request(
            self,
            endpoint: str,
            params: dict | None = None,
            method: str = 'POST'
    ) -> dict:
        """
        Сделать определенный запрос к АПИ
        :param endpoint: конечная точка АПИ (копируется просто из swagger документации)
        :param params: параметры которые будут переданы в качестве JSON
        :param method: метод запроса к API (GET, POST)
        :return: JSON с данными, которые вернет сервер
        """
        headers = self._get_headers() if endpoint != '/auth/login' else {}
        json_data = params if params is not None else {}

        response = requests.request(
            method=method,
            url=f'https://{URL_PREFIX}.{DOMAIN_NAME}/api{endpoint}',
            json=json_data,
            headers=headers
        )

        return response.json()

    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": 'Bearer ' + self._get_auth_token(),
            "X-Project-UUID": PROJECT_UUID
        }

    def _check_token(self) -> bool:
        """Проверка наличия токена для авторизации"""
        token_from_env = self._get_auth_token()
        return True if token_from_env != '' else False

    @staticmethod
    def _get_auth_token() -> str:
        return os.environ.get('KS_SYSTEM_TOKEN')

    @staticmethod
    def _save_token(token) -> None:
        os.environ["KS_SYSTEM_TOKEN"] = token
        dotenv.set_key(dotenv_path,
                       "KS_SYSTEM_TOKEN",
                       token)
