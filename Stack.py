from MarkdownSection import MarkdownSection
# Class stack is a class which defines a stack data structure.
# It has all standard features like: pop, append, peek, size.
# But also (due to the nature of a parser) a method "check_level" was added.
# It checks the neteing level of a list (so count how many times an element is on stack so a list was opend)

class Stack:
    def __init__(self):
        self._items = []

    def pop(self):
        if not len(self._items):
            raise Exception('Empty stack')

        return self._items.pop()

    def append(self, element: MarkdownSection):
        self._items.append(element)

    def peek(self):
        if not len(self._items):
            return None

        return self._items[-1]

    def size(self):
        return len(self._items)

    def check_level(self, element: MarkdownSection):
        return self._items.count(element)
