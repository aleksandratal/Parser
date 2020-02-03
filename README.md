# Parser

Python implementation of a Markdown. It converts markdown files into HTML. Main executive procedure can be found within the Parser.py file. Stack.py contains implementation of a stack data structure (used by parser) and MarkdownSection.py enumerates special characters which can be used in markdown files, i.e.:
- Heading
- BlockOfCode
- Bold
- Italic
- ListOrdered
- ListUnorderedPlus
- ListUnorderedDash
- ListUnorderedStar
- Paragraph
- Blockquotes
- EmtpyLine
- MetaData

Every markdown file needs to contain metada in first 6 lines encolsed between "---" signs. It specifies 4 features of a file: title, date, tags, theme (style or dark). Files: style.css and dark.css defines the styles of file and the tests.py file contains all tests of the program.

## Required libraries 
* html
* re
* webbrowser
* unittest
* enum

## Logic

Parser iterates through the markdown file, line by line, and convert every line to HTML code. It looks for special signs (like #, * etc) and if one is found it is added to a stack and the following lines are converted appropriatly to the sign on stack (if needed another signs are added to the stack as well e.g. for nested list). The sign is taken from the stack when a closing sign is found or an empty line is occured.
