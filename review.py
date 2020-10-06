from __future__ import annotations
import argparse
import os
from lineOperations.lineExtractor import LineExtractor
from lineOperations.lineReviewer import LineReviewer

if __name__ == "__main__":
    def init_argparse() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            usage="%(prog)s ASSPATH [--maxLineLen=0] [--capitalizeNamesFilePath=path]",
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
            "--capitalizeNamesFilePath", 
            action="store",
            default=None,
            type=str,
            help="""The file path where a list of words is stored, separated by newlines. The
                occurences of these words inside the dialogues are capitalized."""
        )
        parser.add_argument(
            'assPath',
            action="store",
            type=str,
            help="""The path of the .ass file to review.""")

        return parser


    def getListOfNamesToCapitalize(fileName: str) -> list(str):
        if fileName is None:
            return []

        with open(fileName, 'r') as f:
            return [line.strip() for line in f]


    parser = init_argparse()
    args = parser.parse_args()
    
    filePath = args.assPath
    fileName = os.path.splitext(os.path.basename(filePath))[0]
    maxLineLength = args.maxLineLen
    namesToCapitalizeFilePath = args.capitalizeNamesFilePath
    namesToCapitalizeList = getListOfNamesToCapitalize(namesToCapitalizeFilePath)


    def reviewLine(line: str) -> str:
        reviewer = LineReviewer(line, maxLineLength, namesToCapitalizeList)
        reviewer.capitalizeLine().capitalizeNames().upperCaseForCapitalPunctuation().splitLineWhenGreaterThanMaxLen()

        return reviewer.getReviewedLine()


    with open(filePath, 'r', encoding='utf8') as fIn, open(f'{fileName}_reviewed.ass', 'w', encoding='utf8') as fOut:
        for line in fIn:
            extractor = LineExtractor(line, reviewLine)

            fOut.write(f'{extractor.getTransformedLine()}')