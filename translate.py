from __future__ import annotations
import argparse
import os
from lineOperations.lineExtractor import LineExtractor
from lineOperations.lineTranslator import LineTranslator

if __name__ == "__main__":
    def init_argparse() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            usage="%(prog)s ASSPATH ",
            description="Translated from english to italian the .ass file specified"
        )
        parser.add_argument(
            'assPath',
            action="store",
            type=str,
            help="""The path of the .ass file to translate.""")
        parser.add_argument(
            '--apiKey',
            action="store",
            required=True,
            type=str,
            help="""Api key for IBM Watson APIs.""")
        parser.add_argument(
            '--serviceUrl',
            action="store",
            required=True,
            type=str,
            help="""Service url for IBM Watson APIs.""")

        return parser


    parser = init_argparse()
    args = parser.parse_args()
    filePath = args.assPath
    fileName = os.path.splitext(os.path.basename(filePath))[0]
    apiKey = args.apiKey
    serviceUrl = args.serviceUrl

    translator = LineTranslator(apiKey, serviceUrl)
    def translateLine(line: str) -> str:
        return translator.getTranslatedLine(line)

    with open(filePath, 'r', encoding='utf8') as fIn, open(f'{fileName}_translated.ass', 'w', encoding='utf8') as fOut:
        for line in fIn:
            extractor = LineExtractor(line, translateLine)

            fOut.write(f'{extractor.getTransformedLine()}')