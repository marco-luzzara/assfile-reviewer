from __future__ import annotations
import re
import math
import argparse
import os

dialogueRegex = re.compile(r'^(Dialogue:(?:[^,]*?,){9})(.*?)$')
capitalPunctuationRegex = re.compile(r'([?!.]\s*)(\w)')
AssFormattingRegex = re.compile(r'\{.*?\}')

class LineReviewer:
    def __init__(self, initialLine: str, maxLineLength: int):
        self._line = initialLine
        self._maxLen = maxLineLength
        self._line = self._line.replace('\\N', '')

        self._formattingMatches = []
        formattingMatch = AssFormattingRegex.search(self._line)
        while formattingMatch != None:
            startPos = formattingMatch.start(0)
            formattingMatchStr = formattingMatch.group(0)
            self._formattingMatches.append([startPos, formattingMatchStr])
            self._line = self._line.replace(formattingMatchStr, '', 1)
            formattingMatch = AssFormattingRegex.search(self._line, startPos)

    def capitalizeLine(self) -> LineReviewer:
        if len(self._line) > 0:
            self._line = self._line[0].upper() + self._line[1:]
        return self

    def upperCaseForCapitalPunctuation(self) -> LineReviewer:
        self._line = capitalPunctuationRegex.sub(lambda match: match.group(1) + match.group(2).upper(), self._line)
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


def reviewLine(line: str, maxLineLength: int) -> str:
    reviewer = LineReviewer(line, maxLineLength)
    reviewer.capitalizeLine().upperCaseForCapitalPunctuation().splitLineWhenGreaterThanMaxLen()

    return reviewer.getReviewedLine()


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s ASSPATH [--maxLineLen=0]",
        description="Fix basic grammar mistakes in a .ass file. It is possible to split dialogues on multiple lines."
    )
    parser.add_argument(
        "-mll", "--maxLineLen", 
        action="store",
        default=0,
        type=int,
        help="""Provided value is the maximum length of a dialogue displayed line. If a 
            line length is greater than this max value, then the line is splitted with a '\\N'. 
            the algorithm split optimally the entire text so that words are not truncated and 
            splitted lines' lengths are as similar as possible."""
    )
    parser.add_argument(
        'assPath',
        action="store",
        type=str,
        help="""The path of the .ass file to review.""")

    return parser


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    
    filePath = args.assPath
    fileName = os.path.splitext(os.path.basename(filePath))[0]
    maxLineLength = args.maxLineLen

    with open(filePath, 'r', encoding='utf8') as fIn, open(f'{fileName}_reviewed.ass', 'w', encoding='utf8') as fOut:
        for line in fIn:
            reviewedText = dialogueRegex.sub(lambda match: match.group(1) + reviewLine(match.group(2), maxLineLength), line)

            fOut.write(f'{reviewedText}')