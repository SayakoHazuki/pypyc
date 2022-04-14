import re
import requests

from html2text import html2text

from .logger import logger
from .exceptions import CredentialsError
from .types import Message, Circular


class Pypyc():
    def __init__(self):
        self.baseUrl = "https://www2.pyc.edu.hk/pycnet"
        self.headers = {
            "credentials": "include",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0)"
                + "Gecko/20100101 Firefox/100.0",
            "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                + "image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "mode": "cors"
        }
        self.session = requests.Session()
        self.logger = logger()

    def get(self, url: str, _headers: dict = {}) -> requests.Response:
        headers = self.headers
        headers["method"] = "GET"
        for header in _headers:
            headers[header] = _headers[header]
        response = self.session.get(url, headers=headers)
        return response

    def post(self, url: str,
             _headers: dict = {}, body: dict = {}) -> requests.Response:
        headers = self.headers
        headers["method"] = "POST"
        for header in _headers:
            headers[header] = _headers[header]

        response = self.session.post(url, headers=_headers, data=body)
        return response

    def login(self, username, password, nostore: bool = False) -> str | None:
        self.post(
            url=f'{self.baseUrl}/',
            _headers={
                "credentials": "omit",
                "Content-Type": "application/x-www-form-urlencoded",
                "Sec-Fetch-User": "?1",
            },
            body={
                'username': username,
                'password': password,
                'loginSubmit': 'Login'
            }
        )

        if not self.validateCreds():
            self.session.cookies.clear()
            raise CredentialsError("Invalid username/password")

        if not nostore:
            self.username = username
            self.password = password

        index_html = self.get(f'{self.baseUrl}/formmail/index.php#').text
        index_md = html2text(index_html)
        welcome_string = index_md.splitlines()[2].split(" || ")[0]
        userMatch = re.fullmatch(
            r'Welcome S([1-6][A-E])\(([0-9]{2})\) ([A-Z ]*)\((pyc[0-9]{5})\)',
            welcome_string
        )
        if userMatch is not None:
            sClass = userMatch.group(1)
            sClassNum = userMatch.group(2)
            sFullName = userMatch.group(3)
            sStudCode = userMatch.group(4)
            self.logger.info('Logged in as {}({}) {} [{}]'.format(
                sClass, sClassNum, sFullName, sStudCode
            ))

    def logout(self):
        self.session.cookies.clear()
        self.logger.info('Logged out')

    def updateCreds(self) -> str:
        self.session.cookies.clear()

        if self.username is None or self.password is None:
            raise CredentialsError("No stored username/password")

        new_token = self.login(self.username, self.password)
        return new_token

    def validateCreds(self) -> bool:
        return 'access_token' in self.session.cookies.get_dict()

    def getMessages(self, pageNumber: int = 1) -> list[Message]:
        index_html = self.get(
            "{}/formmail/index.php?page={}&key=&key2=&sort=".format(
                self.baseUrl, pageNumber
            )
        ).text
        message_html_pattern = re.compile(
            r'<input type="?checkbox"? name="dels\[\]" '
            + r'value="([0-9]+),([0-9A-Za-z]+),([^,]+),([0-9]+),[0-9]+,">',
            re.I
        )
        message_props = re.findall(message_html_pattern, index_html)
        index_md = html2text(index_html)
        messages_md = index_md.split(
            "sort=date&key=&key2=)\n\n"
        )[1].split(
            "\n\nSelect/Deselect all"
        )[0]
        message_pattern = re.compile(
            r'\[(.*)\]\((view\.php\?page=[0-9]+&id=[0-9]+)\)'
            + r'[\n\s]?(!\[\]\(images\/common\.gif\))?\n+(.*)\n+'
            + r'([A-Za-z]+ [0-9]+, [0-9]+)',
            re.M
        )
        messages = re.findall(message_pattern, messages_md)
        messages_list = []

        for i, message in enumerate(messages):
            props = ()
            if i < len(message_props):
                props = message_props[i]

            messages_list.append(
                Message(
                    self,
                    *message,
                    *props
                )
            )
        return messages_list

    def getCirculars(self) -> list[Circular]:
        circulars_html = self.session.get(
            f'{self.baseUrl}/circulars/student.php'
        ).text
        circulars_md = html2text(circulars_html).split('---|---|---')[1]

        circulars_list = []
        for line in circulars_md.splitlines():
            line_is_circular = re.fullmatch(
                r'(.*)\|\s*(\[.*\])\s*\(view.php\?id=([0-9]*)\)\|\s*', line)

            if not line_is_circular:
                continue

            regex_res = re.search(
                r'^(.*)\|\s*\[(.*)\]\s*\(view.php\?id=([0-9]*)\)\|\s*$', line)
            (date, title, _id) = regex_res.groups()
            circulars_list.append(Circular(self, date, title, _id))
        return circulars_list
