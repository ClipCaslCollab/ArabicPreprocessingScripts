class Document:

    def __init__(self, uid, text, score):
        self._uid = uid
        self._text = text
        self._score = score

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = val

    @property
    def score(self):
        return self._score

    @property
    def unique_id(self):
        return self._uid

    @property
    def polarity(self):
        if self.score == "1" or self.score == "2":
            return "negative"
        elif self.score == "4" or self.score == "5":
            return "positive"
        return "neutral"


