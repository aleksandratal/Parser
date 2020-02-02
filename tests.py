from MarkdownSection import MarkdownSection
from Stack import Stack
from Parser import Parser
import re

import unittest

class TestStack(unittest.TestCase):

    def test_empty_len(self):
        testStack = Stack()
        self.assertEqual(testStack.size(), 0)
    
    # Proper length and append
    def test_append(self):
        testStack = Stack()
        testStack.append('a')
        testStack.append(6754)
        testStack.append([7, 5, 6, 'a'])
        self.assertEqual(testStack.size(), 3)

    # Raises error when poping from empty stack
    def test_empty_pop(self):
        testStack = Stack()
        testStack.append('a')
        testStack.pop()
        self.assertEqual(testStack.size(), 0)
        with self.assertRaises(Exception):
            testStack.pop()

    # Is the last added element on top        
    def test_last_on_top(self):
        testStack = Stack()
        testStack.append('a')
        testStack.append(4)
        testStack.append(54)
        testStack.append('b')
        self.assertEqual(testStack.peek(), 'b')

    def test_peek_empty(self):
        testStack = Stack()
        self.assertEqual(testStack.peek(), None)

    # Check how much is an element "nested"
    def test_level(self):
        testStack = Stack()
        testStack.append('a')
        testStack.append(4)
        testStack.append('a')
        testStack.append('b')
        testStack.append(6)
        testStack.append(75)
        testStack.append('a')
        self.assertEqual(testStack.check_level('a'), 3)

class TestParserMethods(unittest.TestCase):

    # too short metadata file
    def test_file_len(self):
        example = "text ** bold ** text2"
        parser = Parser()
        with self.assertRaises(Exception):
            result = parser.parse(example)

    # checks bold
    def test_bold(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

text ** bold ** text2
"""
        result = parser.parse(example)
        result2 = result.split('\n')
        my_result = "text <strong> bold </strong> text2"
        
        self.assertEqual(my_result, result2[8])

    # checks italic
    def test_italic(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

text _ bold _ text2
"""
        result = parser.parse(example)
        result2 = result.split('\n')
        my_result = "text <em> bold </em> text2"
        
        self.assertEqual(my_result, result2[8])

    # checks bold and italic
    def test_bolditalic(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

text *** bold *** text2
"""
        result = parser.parse(example)
        result2 = result.split('\n')
        my_result = "text <strong><em> bold </em></strong> text2"
        
        self.assertEqual(my_result, result2[8])

    # checks italic after bold
    def test_bolditalic_onebyone(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

text ** bold ** *text2*
"""
        result = parser.parse(example)
        result2 = result.split('\n')
        my_result = "text <strong> bold </strong> <em>text2</em>"
        
        self.assertEqual(my_result, result2[8])
    
    # checks code
    def test_code(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

```
text text text text
```
"""
        result = parser.parse(example)
        self.assertTrue("<div class='CodeBlock'>" in result)
        self.assertTrue("</div>" in result)

    # checks blockquotes
    def test_blockquotes(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

> text text text text
"""
        result = parser.parse(example)
        self.assertTrue("<blockquote class='QuotesBlock'>" in result)
        self.assertTrue("</blockquote>" in result)

    # checks url
    def test_url(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

text [url name](https:address)
"""
        result = parser.parse(example)
        self.assertTrue("<a href=" in result)
        self.assertTrue("</a>" in result)

    # checks unknown
    def test_unknown(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

text * special sign # should not be here
"""
        result = parser.parse(example)
        self.assertTrue("text * special sign # should not be here" in result)

    # ensures no paragraph is created if file is empty
    def test_empty(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---


"""
        result = parser.parse(example)
        self.assertTrue("<p>" not in result)

    # creates paragraph
    def test_paragraph(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

Import a HTML file and watch it magically convert to Markdown. 

Import a HTML file and watch it magically convert to Markdown.

Import a HTML file and watch it magically convert to Markdown.
"""
        result = parser.parse(example)
        self.assertTrue("<p>" in result)

    # lists
    def test_lists(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

+ 6 and drop images (requires your Dropbox account be linked)
+ 7 and drop images
"""
        result = parser.parse(example)
        self.assertTrue(result.count("<li>") == 2)
        self.assertTrue(result.count("</li>") == 2)
        self.assertTrue("<ul>" in result)
        self.assertTrue("</ul>" in result)

    # nested lists
    def test_nested_list(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

+ 1 and drop images (requires your Dropbox account be linked)
    + 2 and drop images
        + 3 drop images
    + image
"""
        result = parser.parse(example)
        self.assertTrue(result.count("<li>") == 4)
        self.assertTrue(result.count("</li>") == 4)
        self.assertTrue(result.count("<ul>") == 3)
        self.assertTrue(result.count("</ul>") == 3)

    # not enough spaces
    def test_spaces_inlists(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

+ 1 and drop images (requires your Dropbox account be linked)
  + 2 and drop images

"""
        result = parser.parse(example)
        print(result)
        self.assertTrue(result.count("<li>") == 2)
        self.assertTrue(result.count("</li>") == 2)
        self.assertTrue(result.count("<ul>") == 1)
        self.assertTrue(result.count("</ul>") == 1)

    # bold within list
    def test_bold_in_list(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

+ 6 and drop images (requires your Dropbox account be linked)
+ 7 and **drop images**
"""
        result = parser.parse(example)
        self.assertTrue("<strong>" in result)
        self.assertTrue("</strong>" in result)
        self.assertTrue("<ul>" in result)
        self.assertTrue("</ul>" in result)

    # checks if all tags are closed
    def test_tag_closing(self):
        f = open("sample.md", "r")
        example = "".join(f.readlines())
        f.close()

        open_tag = example.count('<p>')
        close_tag = example.count('</p>')
        self.assertEqual(open_tag, close_tag)
        open_tag = example.count('<ul>')
        close_tag = example.count('</ul>')
        self.assertEqual(open_tag, close_tag)
        open_tag = example.count('<ol>')
        close_tag = example.count('</ol>')
        self.assertEqual(open_tag, close_tag)
        open_tag = example.count('<html>')
        close_tag = example.count('</html>')
        self.assertEqual(open_tag, close_tag)
        open_tag = example.count('<body>')
        close_tag = example.count('</body>')
        self.assertEqual(open_tag, close_tag)
        self.assertEqual(open_tag, close_tag)
        open_tag = example.count('<blockquote>')
        close_tag = example.count('</blockquote>')
        self.assertEqual(open_tag, close_tag)
        open_tag = example.count('<div>')
        close_tag = example.count('</div>')
        self.assertEqual(open_tag, close_tag)

    # html code in block of code not converted
    def test_escapeHTML(self):
        parser = Parser()
        example = """---
title: Turkish Cheese Pide
date: 2019-04-12
tags: Bread, Savoury
theme: style
---

```
<p><em> text text text </em></p>
```
"""
        result = parser.parse(example)
        my_result = '&lt;p&gt;&lt;em&gt; text text text &lt;/em&gt;&lt;/p&gt;<br>'
        
        self.assertTrue(my_result in result)

if __name__ == '__main__':
    unittest.main()


