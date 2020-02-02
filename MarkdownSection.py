from enum import Enum
# Every special character is given a label to simplify looking for special characters

class MarkdownSection(Enum):
    Html = 0
    Body = 1
    Heading = 2
    BlockOfCode = 3
    Quote = 4
    Bold = 5
    Italic = 6
    ListOrdered = 7
    ListUnorderedPlus = 8
    ListUnorderedDash = 9
    ListUnorderedStar = 10
    Paragraph = 11
    Blockquotes = 12
    EmtpyLine = 13
    BlockCode = 14
    MetaData = 15

ListElements = [MarkdownSection.ListUnorderedDash, MarkdownSection.ListUnorderedPlus,
                MarkdownSection.ListUnorderedStar, MarkdownSection.ListOrdered]
ListUnorderedElements = [MarkdownSection.ListUnorderedDash, MarkdownSection.ListUnorderedPlus,
                         MarkdownSection.ListUnorderedStar]
