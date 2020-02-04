import html # escape special signs in hTML
from MarkdownSection import MarkdownSection, ListElements, ListUnorderedElements
import re
from Stack import Stack
import sys
import webbrowser   # open the html page automatically


class Parser(object):
    def __init__(self):
        self._stack = Stack() # Stack where the information on open HTML tags is stored
        self._html = ['<!DOCTYPE html>', '<html>', '<body>']  # output list, stores HTML code
        self._stack.append(MarkdownSection.Html)
        self._stack.append(MarkdownSection.Body)
        # list of all functions which handle the appriopriate text type
        self._nonBlockHandlers = [self.handleHeading, self.handleBoldItalid, self.handleBold,
                                  self.handleItalic, self.handleurl, self.handleUnknown]
        self._handlers = [self.handleEmpty, self.handleCode, self.handleBlockquotes,
                          self.handleList] + self._nonBlockHandlers

        self.MetaData = {} # stores metadata of the md file, 
                           #i.e. title, date: 2019-04-12, tags, theme (style or dark)

    def parse(self, text: str):
        """main function - splits given text by enters"""
        lines = text.split('\n')
        if len(lines) < 6:
            raise Exception('No meta data or too short')
        metadata = lines[:6]  # retrieves metadata (by calling appriopriate function)
        rest = lines[7:]
        self.handleMetaData(metadata)
        list(map(lambda x: self.parseNewLine(x), rest)) # parses every line of text 
        while self._stack.size():    # closes all open tags at the end of the file
            self.closeHtmlTag(self._stack.pop())

        return '\n'.join(self._html) # returns a string with HTML code

    def closeHtmlTag(self, tagType: MarkdownSection): 
        """closes last tag from the stack
        tag types are defined within Markdown class"""
        if tagType in ListUnorderedElements:          
            self._html.append("</ul>")
            return
        if tagType == MarkdownSection.ListOrdered:
            self._html.append("</ol>")
        if tagType == MarkdownSection.Html:
            self._html.append("</html>")
        if tagType == MarkdownSection.Body:
            self._html.append("</body>")
        if tagType == MarkdownSection.Paragraph:
            self._html.append("</p>")
        if tagType == MarkdownSection.BlockOfCode:
            self._html.append("</div>")
        if tagType == MarkdownSection.Blockquotes:
            self._html.append("</blockquote>")

    def handleNewList(self, currentListType: MarkdownSection, spacesCount: int, text: str):
        """function to handle nested lists
        it checks the level of nesting
        and parses the text additionally (checks for bold or italic text etc)"""

        nestLevel = self._stack.check_level(currentListType)
        if not spacesCount:
            spacesCount = ''
        currentLevel = int(len(spacesCount) / 4) + 1

        if currentLevel < nestLevel:
            while currentLevel < nestLevel:
                currentElement = self._stack.pop()
                if currentElement == currentListType:
                    nestLevel -= 1
                self.closeHtmlTag(currentElement)
        elif currentLevel - 1 == nestLevel:
            self._stack.append(currentListType)
            if currentListType == MarkdownSection.ListOrdered:
                self._html.append("<ol>")
            else:
                self._html.append("<ul>")

        return f"<li>{self.parseText(text)}</li>"

    def closeList(self): 
        """closes list HTML tags checking first the list type"""
        for listType in ListUnorderedElements:
            level = self._stack.check_level(listType)
            while level:
                currentElement = self._stack.pop()
                if currentElement == listType:
                    level -= 1
                self.closeHtmlTag(currentElement)

    def handleList(self, line: str): 
        """function for parsing lists (both ordered and unordered)"""
        regex = re.search(r"^( *)([+\-*]|\d\.) (.*)$", line) # regex to match +, -, * or digit.
        if regex and regex.group(2):
            if regex.group(2) == "+" or regex.group(2) == "-" or regex.group(2) == "*":
                return self.handleNewList(MarkdownSection.ListUnorderedPlus,
                                          regex.group(1), regex.group(3))
            else:
                return self.handleNewList(MarkdownSection.ListOrdered,
                                          regex.group(1), regex.group(3))     
            return None
        self.closeList()

    def handleHeading(self, line: str): 
        """function for parsing heads"""
        regex = re.search(r"^(#+) (.*)$", line) # regex to match #### head (any number of #'s)
        if regex:
            headingType = len(regex.group(1))
            headingValue = regex.group(2)
            return f"<h{headingType}>{headingValue}</h{headingType}>"

    def handleBold(self, line: str): 
        """function for parsing bold text"""
        regex = re.search(r"^(.*)(\*\*|\_\_)([^*_]+)(\*\*|\_\_)(.*)$", line) 
        if regex: # regex to match ** ** or __ __
            textBefore = regex.group(1)
            textBold = regex.group(3)
            textAfter = regex.group(5)
            return f"{self.parseText(textBefore)}<strong>{self.parseText(textBold)}</strong>{self.parseText(textAfter)}"

    def handleUnknown(self, line: str) -> str: 
        """function for parsing normal text 
        or text with symbols not defined as special characters"""
        return line                            

    def handleItalic(self, line: str):
        """function for parsing italic text""" 
        regex = re.search(r"^(.*)([\*\_])([^*_]+)([\*\_])(.*)$", line)
        if regex: # regex to match * * or _ _
            textBefore = regex.group(1)
            textItalic = regex.group(3)
            textAfter = regex.group(5)
            return f"{self.parseText(textBefore)}<em>{self.parseText(textItalic)}</em>{self.parseText(textAfter)}"

    def handleBoldItalid(self, line: str): 
        """function for parsing bold and italic text"""
        regex = re.search(
            r"^(.*)(\*\*\*|\_\_\_)([^*_]+)(\*\*\*|\_\_\_)(.*)$", line)
        if regex: # regex to match *** *** or ___ ___
            textBefore = regex.group(1)
            textBoldandItalic = regex.group(3)
            textAfter = regex.group(5)
            return f"{textBefore}<strong><em>{textBoldandItalic}</em></strong>{textAfter}"

    def handleurl(self, line:str): 
        """function for parsing links"""
        regex = re.search(r"^(.*)\[(.*)\]\((https:.*)\)(.*)$", line)
        if regex:
            txtBefore = regex.group(1)
            urlText = regex.group(2)
            urlHtml = regex.group(3)
            txtAfter = regex.group(4)
            return f"{txtBefore}<a href='{urlHtml}'>{urlText}</a>{txtAfter}"

    def handleCode(self, line: str): 
        """function for parsing block of code starting with ```"""
        regex = re.search(r"^(```).*$", line)
        if regex and self._stack.peek() != MarkdownSection.BlockOfCode:
            self._stack.append(MarkdownSection.BlockOfCode)
            return f"<div class='CodeBlock'>"
        elif regex and self._stack.peek() == MarkdownSection.BlockOfCode:
            self._stack.pop()
            return f"</div>"
        elif self._stack.peek() == MarkdownSection.BlockOfCode:
            line = html.escape(line)
            return f"{line}<br>"

    def handleBlockquotes(self, line: str): 
        """function for parsing blockquote starting with >"""
        regex = re.search(r"^(>)(.*)$", line)
        if regex and self._stack.peek() != MarkdownSection.Blockquotes:
            self._stack.append(MarkdownSection.Blockquotes)
            txt = regex.group(2)
            return f"<blockquote class='QuotesBlock'>{txt}"

    def handleMetaData(self, lines: list): 
        """retrieving metadata and saving to dictionary
        metadata attributes are then used to define a style of the file"""
        if len(lines) < 6:
            raise Exception('No meta data or wrong format')

        data = lines[1:-1]                 
        for line in data:                  
            lineSplit = line.split(": ")
            key = lineSplit[0]
            value = lineSplit[1].strip()
            self.MetaData[key] = value
        self._html.append("<head>")
        self._html.append(
            f'<meta name="keywords" content="{self.MetaData["tags"]}">')
        self._html.append(f"<title>{self.MetaData['title']}</title>")
        self._html.append(
            f'<link rel="stylesheet" href="{self.MetaData["theme"]}.css">')
        self._html.append("</head>")

    def handleEmpty(self, line: str): 
        """empty lines indicates opening or starting a new paragraph
        empty line == line with spaces, tabs etc"""
        regex = re.search(r"^\s*$", line)
        if line == '' or regex:
            self.closeList()
            if self._stack.peek() == MarkdownSection.EmtpyLine:
                return
            if self._stack.peek() == MarkdownSection.BlockOfCode:
                self._html.append(f"{line}<br>")
                return
            if self._stack.peek() == MarkdownSection.Blockquotes:
                self.closeHtmlTag(self._stack.pop())
            if self._stack.peek() == MarkdownSection.Paragraph:
                self.closeHtmlTag(MarkdownSection.Paragraph)
                self._stack.pop()
            self._stack.append(MarkdownSection.EmtpyLine)
        elif self._stack.peek() == MarkdownSection.EmtpyLine:
            self._stack.pop()
            self._stack.append(MarkdownSection.Paragraph)
            self._html.append("<p>")

    def parseNewLine(self, line: str): 
        """parse every line by checking every regex"""
        for handler in self._handlers:
            res = handler(line)
            if res:
                self._html.append(res)
                return

    def parseText(self, line: str):
        """non block handlers for nested special characters"""
        for handler in self._nonBlockHandlers:
            res = handler(line)
            if res:
                return res
        return ''

"""Main program, calling a parser with sample.md example, writing it to index.html file"""

filename = sys.argv[1]
f = open(filename, "r")
example = "".join(f.readlines())
f.close()

parser = Parser()
result = parser.parse(example)

f = open("index.html", "w")
f.write(result)
f.close()

url = 'index.html'
webbrowser.open(url, new=2)  # open in new tab
