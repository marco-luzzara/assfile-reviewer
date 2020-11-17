from __future__ import annotations
import argparse

from operations.reviewer import Reviewer

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


    parser = init_argparse()
    args = parser.parse_args()
    
    filePath = args.assPath
    maxLineLength = args.maxLineLen
    namesToCapitalizeFilePath = args.capitalizeNamesFilePath

    reviewer = Reviewer(filePath, maxLineLength, namesToCapitalizeFilePath)
    reviewer.review()