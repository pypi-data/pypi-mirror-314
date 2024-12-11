from html.parser import HTMLParser
from typing import List, Optional

class LinkExtractor(HTMLParser):
    link: Optional[str]
    def handle_starttag(self, tag: str, attr: List[str]): ...
