import os

from operations.lineOperations.lineExtractor import LineExtractor
from operations.lineOperations.lineTranslator import LineTranslator

class Translator:
    def __init__(self, filePath: str, apiKey: str, serviceUrl: str):
        self._filePath = filePath
        self._fileName = os.path.splitext(os.path.basename(self._filePath))[0]
        self._translator = LineTranslator(apiKey, serviceUrl)

    def _translateLine(self, line: str) -> str:
        return self._translator.getTranslatedLine(line)

    def translate(self):
        with open(self._filePath, 'r', encoding='utf8') as fIn, open(f'{self._fileName}_translated.ass', 'w', encoding='utf8') as fOut:
            for line in fIn:
                extractor = LineExtractor(line, self._translateLine)

                fOut.write(f'{extractor.getTransformedLine()}')