from __future__ import annotations
import re
import math

class LineReviewer:
    def __init__(self, initialLine: str, maxLineLength: int, namesToCapitalize: set[str]):
        self._maxLen = maxLineLength
        self._line = initialLine
        self._capitalizeLineRegex = re.compile(r'(^\s*)([A-zÀ-ú])')
        self._capitalPunctuationRegex = re.compile(r'([?!.-]\s*)(\w)')
        self._AssFormattingRegex = re.compile(r'\{.*?\}')
        self._capitalizeNameRegex = re.compile(r'\w+', re.IGNORECASE)

        self._formattingMatches = []
        formattingMatch = self._AssFormattingRegex.search(self._line)
        while formattingMatch != None:
            startPos = formattingMatch.start(0)
            formattingMatchStr = formattingMatch.group(0)
            self._formattingMatches.append([startPos, formattingMatchStr])
            self._line = self._line.replace(formattingMatchStr, '', 1)
            formattingMatch = self._AssFormattingRegex.search(self._line, startPos)

        self._namesToCapitalize = namesToCapitalize

    def capitalizeLine(self) -> LineReviewer:
        self._line = self._capitalizeLineRegex.sub(lambda match: match.group(1) + match.group(2).upper(), self._line)
        return self

    def upperCaseForCapitalPunctuation(self) -> LineReviewer:
        self._line = self._capitalPunctuationRegex.sub(lambda match: match.group(1) + match.group(2).upper(), self._line)
        return self

    def __findNearestWhiteSpace(self, line: str, pointer: int) -> int:
        def __findFirstWhiteSpace(halfLine: str) -> int:
            for (i, c) in enumerate(halfLine):
                if c == ' ':
                    return i
            
            return math.inf

        firstHalfWhiteSpace = __findFirstWhiteSpace(line[:pointer + 1][::-1])
        secondHalfWhiteSpace = __findFirstWhiteSpace(line[pointer:])

        minWithSign = (firstHalfWhiteSpace, -1) if firstHalfWhiteSpace < secondHalfWhiteSpace else (secondHalfWhiteSpace, 1)

        return pointer if minWithSign[0] == math.inf else pointer + minWithSign[0] * minWithSign[1]

    def splitLineWhenGreaterThanMaxLen(self) -> LineReviewer:
        if self._maxLen == 0:
            return self

        lineChunks = []
        residualLine = self._line
        nLines = math.ceil(len(self._line) / self._maxLen)

        while nLines > 0:
            nlIndex = None

            if nLines > 1:
                nextChunkLen = round(len(residualLine) / nLines)
                nlIndex = self.__findNearestWhiteSpace(residualLine, nextChunkLen)

            lineChunks.append(residualLine[:nlIndex]) 
            residualLine = residualLine[nlIndex:]
            nLines -= 1

        self._line = '\\N'.join(lineChunks)
        return self

    def capitalizeNames(self) -> LineReviewer:
        self._line = self._capitalizeNameRegex.sub(lambda match: match.group(0).capitalize() if match.group(0).lower() in self._namesToCapitalize else match.group(0), self._line)
        return self

    def getReviewedLine(self) -> str:
        lastIndex = 0
        newLineIndex = self._line.find('\\N', lastIndex)

        while newLineIndex != -1:
            for m in self._formattingMatches:
                if m[0] >= newLineIndex:
                    m[0] = m[0] + 2

            lastIndex = newLineIndex + 2
            newLineIndex = self._line.find('\\N', lastIndex)

        offset = 0
        for m in self._formattingMatches:
            curIndex = m[0] + offset
            self._line = self._line[:curIndex] + m[1] + self._line[curIndex:]
            offset = offset + len(m[1])

        return self._line