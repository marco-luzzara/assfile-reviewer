from __future__ import annotations
import re

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
        self._AssFormattingRegex = re.compile(r'\{.*?\}')

    def getTranslatedLine(self, line: str) -> str:
        translation = self._language_translator.translate(text=line, source='en', target='it').get_result()
        rawTranslatedLine = translation['translations'][0]['translation']
        translatedLine = self._AssFormattingRegex.sub(lambda match: match.group(0).replace(' ', ''), rawTranslatedLine)

        return translatedLine