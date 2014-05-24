__author__ = 'jkonieczny'

class ActionUrl:
    """
    Klasa akcji: url i związany z tym tekst
    """
    def __init__(self, url, text):
        self.url = url
        self.text = text
    def html(self):
        return "<a href=\"%s\">%s</a>" %(self.url, self.text)

class ActionBack:
    def html(self):
        return "<a href=\"javascript:history.back()\">Wróć</a>"

class Message:
    """
    Klasa wiadomości
    """
    def __init__(self, head, message, actions=[]):
        self.head = head
        self.message = message
        self.actions = actions