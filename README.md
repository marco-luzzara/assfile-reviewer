# .ass File Reviewer (review.py)
Here are listed all the current review operations:
* Capitalize first letter of each sentence
* If a line is longer than the specified maximum line length, it is split using a \N. This behaviour is recursive on the second part of the line, meaning that you could potentially have multiple \N inside the same line if it is very long.
* (**Optional**) If you provide a filename with a list of words (one for each line), the occurrences of these words are capitalized. Useful for proper nouns especially. For example, given a file with this content:

```
ann
bob
```

And this sentence: _**a**nn and **b**ob are going to the market_

The resulting sentence is: _**A**nn and **B**ob are going to the market_
* Letters following these symbols '?', '!', '.', '-' are uppercased.

The generated file has the suffix "_reviewed".

## Usage
`py review.py filename.ass --maxLineLen=45 --capitalizeNamesFilePath='names_to_capitalize.txt'`

For more info on arguments: `py review.py --help`


# .ass File Translator (translate.py)
Translates from english to italian a .ass file using [IBM Cloud APIs](https://cloud.ibm.com/services/language-translator/), the generated file has the suffix "_translated".

## Usage
`py translate.py yourfilename.ass --apiKey='secretapykey' --serviceUrl='secretServiceUrl'`

For more info on arguments: `py translate.py --help`

# GUI Version
There is the GUI version too (_gui_reviewer.py_ and _gui_translator.py_). To create the executables, you must install `pyinstaller`.

`pip install pyinstaller`

Then add `pyinstaller.exe` to the PATH, `cd` to the _install_ folder and run the script commands.

## GUI Reviewer
The GUI Reviewer needs a .ini file in the same folder called _reviewer_config.ini_, containing:

```
[root] 
defaultMaxLineLength=45
```

Where `defaultMaxLineLength` is an arbitrarily decided value specifying the maximum length of a line, before the \N is inserted. See second point [here](#ass-file-reviewer-reviewpy).

## GUI Translator
The GUI Translator needs a .ini file in the same folder called _translator_config.ini_, containing:

```
[translation_service] 
apiKey=ibm_api_key
serviceUrl=ibm_service_url
```

Where both `apiKey` and `serviceUrl` can be found on the [IBM Cloud](https://cloud.ibm.com/services/language-translator/).
