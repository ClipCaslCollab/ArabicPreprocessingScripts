class Document:

    def __init__(self, text, score, author=None, review=None, book=None, uid=None):
        self._text = text
        self._score = score
        self._author = author
        self._review = review
        self._book = book
        self._uid = uid

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
    def author(self):
        return self._author

    @property
    def review(self):
        return self._review

    @property
    def book(self):
        return self._book

    @property
    def unique_id(self):
        try:
            if self._uid:
                return self._uid
        except AttributeError:
            pass
        return '_'.join([self.score, self.book, self.review, self.author])

    @property
    def polarity(self):
        if self.score == "1" or self.score == "2":
            return "negative"
        elif self.score == "4" or self.score == "5":
            return "positive"
        return "neutral"


