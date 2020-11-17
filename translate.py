from __future__ import annotations
import argparse

from operations.translator import Translator

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
    apiKey = args.apiKey
    serviceUrl = args.serviceUrl

    translator = Translator(filePath, apiKey, serviceUrl)
    translator.translate()