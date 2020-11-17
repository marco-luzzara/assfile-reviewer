import os

from operations.lineOperations.lineExtractor import LineExtractor
from operations.lineOperations.lineReviewer import LineReviewer

class Reviewer:
    def __init__(self, filePath: str, maxLineLength: int, namesToCapitalizeFilePath: str):
        self._filePath = filePath
        self._fileName = os.path.splitext(os.path.basename(self._filePath))[0]
        self._maxLineLength = maxLineLength
        self._namesToCapitalizeSet = self._getSetOfNamesToCapitalize(namesToCapitalizeFilePath)

    def _getSetOfNamesToCapitalize(self, fileName: str) -> set[str]:
        if fileName is None:
            return []

        with open(fileName, 'r') as f:
            return {line.strip().lower() for line in f}

    def _reviewLine(self, line: str) -> str:
        reviewer = LineReviewer(line, self._maxLineLength, self._namesToCapitalizeSet)
        reviewer.capitalizeLine().capitalizeNames().upperCaseForCapitalPunctuation().splitLineWhenGreaterThanMaxLen()

        return reviewer.getReviewedLine()

    def review(self):
        with open(self._filePath, 'r', encoding='utf8') as fIn, open(f'{self._fileName}_reviewed.ass', 'w', encoding='utf8') as fOut:
            for line in fIn:
                extractor = LineExtractor(line, self._reviewLine)

                fOut.write(f'{extractor.getTransformedLine()}')