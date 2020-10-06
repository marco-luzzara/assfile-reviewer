from __future__ import annotations
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class LineTranslator:
    def __init__(self, apiKey: str, serviceUrl: str):
        self._authenticator = IAMAuthenticator(apiKey)
        self._language_translator = LanguageTranslatorV3(
            version='2018-05-01',
            authenticator=self._authenticator
        )
        self._language_translator.set_service_url(serviceUrl)

    def getTranslatedLine(self, line: str) -> str:
        translation = self._language_translator.translate(text=line, source='en', target='it').get_result()
        return translation['translations'][0]['translation']