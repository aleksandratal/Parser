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

Every markdown file needs to contain metada in first 6 lines encolsed between "---" signs. It specifies 4 features of a file: title, date, tags, theme (style or dark).

## Required libraries 
* html
* re
* webbrowser
* unittest
* enum

## Logic

