from html2text import html2text

from pypyc.exceptions import PropertyException


class Message:

    def __init__(
        self,
        session,
        title: str = "",
        relative_url: str = "view.php",
        ico: str = None,
        author: str = "",
        date: str = "Jan 1, 2020",
        messageId: str = None,
        attachmentId: str = None,
        authorId: str = None,
        messageId2: str = None,
        sp_param: str = '0'
    ):

        self.session = session
        self.title = title
        self.url = f'{self.session.baseUrl}/formmail/{relative_url}'
        self.icon = None if ico == "" else ico
        self.author = author
        self.date = date
        self.messageId = messageId
        self.attachmentId = attachmentId
        self.authorId = authorId
        self.messageId2 = messageId2
        self.sp_param = sp_param

    @property
    def hasAttachments(self):
        if (self.icon is None and self.attachmentId != 0):
            self.session.logger.warn(PropertyException(
                'Message has attachmentId {} while icon is {}'.format(
                    self.attachmentId, None
                )
            ))
        return (self.icon is not None and self.attachmentId != 0)

    def delete(self):
        response = self.session.post(
            self.session.baseUrl
            + '/formmail/index.php?page=1key=&key2=&sort=',
            {},
            {
                "dels[]":
                    f'{self.messageId},{self.attachmentId},'
                    + f'{self.authorId},{self.messageId2},{self.sp_param},',
                "page": 1,
                "submit": "Delete checked"
            }
        )
        if response.status_code == 200:
            return
        else:
            self.session.logger.error(
                f'POST Request failed with status code {response.status_code}'
            )
            return

    def getText(self) -> str:
        message_html = self.session.get(self.url).text

        message_md = html2text(message_html)
        message_md = message_md.split('\n\nMessage :\n\n')[1]
        message_md = message_md.split('\n\nCopyright (C)')[0]

        return message_md
