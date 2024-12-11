from gigachat import GigaChat

from . import GigaChatEntryPoint


class GigaMaxEntryPoint(GigaChatEntryPoint):
    def __init__(self, client_id: str, client_secret: str, obligatory_warmup: bool = False) -> None:
        super().__init__(client_id, client_secret)
        self._model = GigaChat(
            credentials=self._creds,
            base_url="https://gigachat.devices.sberbank.ru/api/v1/",
            scope="GIGACHAT_API_CORP",
            model="GigaChat-Max",
            verify_ssl_certs=False,
            profanity_check=False,
        )
        self._warmed_up: bool = False
        if obligatory_warmup:
            self.warmup()