import re

from html2text import html2text


class Circular:
    def __init__(self, session, date: str, title: str, _id: str) -> None:
        self.session = session
        self.title = title
        self.date = date
        self.id = _id

    @property
    def url(self):
        page_html = self.session.get(
            url=f'{self.session.baseUrl}/circulars/view.php?id={self.id}'
        )

        page_text = ''.join(
            html2text(page_html.text).splitlines())
        url = re.sub(
            r'[\s\S]*\[Download\]\(', '', page_text, re.M)
        url = re.sub(r'\)[\s\S]*', '', url, re.M)

        return url

    def getBinaryContent(self):
        r = self.session.get(self.url)
        return r.content
