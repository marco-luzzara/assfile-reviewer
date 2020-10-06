# .ass File Reviewer (review.py)
Here are listed all the current reviewing operations:
* Capitalize first letter of the sentence
* split dialogues on multiple lines specifying the desired maximum length (separator is \N)
* providing a filename with a list of words (one for each line), the occurrences of these words are capitalized. Useful features for proper nouns.
* Uppercase letters that follow these symbols '?', '!', '.', '-'.
the file generated will have the suffix "_reviewed".

## Usage
`py review.py filename.ass --maxLineLen=45 --capitalizeNamesFilePath='names_to_capitalize.txt'`

For more info on arguments: `py review.py --help`


# .ass File Translator (translate.py)
Translates from english to italian a .ass file using IBM Watson API, the file generated will have the suffix "_translated".

## Usage
`py translate.py yourfilename.ass --apiKey='secretapykey' --serviceUrl='secretServiceUrl'`

For more info on arguments: `py translate.py --help`


 
* `--capitalizeNamesFilePath`
  The file path where a list of words is stored, separated by newlines. The
  occurences of these words inside the dialogues are capitalized.
 

