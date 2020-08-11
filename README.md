# .ass File Reviewer
Fix basic grammar mistakes in a .ass file. It is possible to split dialogues on multiple lines. 
As for now, fixed mistakes are letter that should be capitalized after fullstops or ellipsis.

## Usage
`py reviewer.py ASSPATH [--maxLineLen=0]`

## Arguments
* `ASSPATH`
  The path of the .ass file to review.

* `-mll`, `--maxLineLen`
  Provided value is the maximum length of a dialogue displayed line. If a 
  line length is greater than this max value, then the line is splitted with a '\\N'. 
  the algorithm split optimally the entire text so that words are not truncated and 
  splitted lines' lengths are as similar as possible. Default value is 0, which means "do not split".
 

