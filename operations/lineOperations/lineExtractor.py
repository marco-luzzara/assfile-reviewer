from __future__ import annotations
import re

class LineExtractor:
    def __init__(self, line: str, func: [[str], str]):
        self._dialogueRegex = re.compile(r'^(Dialogue:(?:[^,]*?,){9})(.*?)$')
        self._opFunc = func
        self.line = line.replace('\\N', ' ')

    def getTransformedLine(self) -> str:
        return self._dialogueRegex.sub(lambda match: match.group(1) + self._opFunc(match.group(2)), self.line)