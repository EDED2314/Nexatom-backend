from bs4 import BeautifulSoup
import aiohttp

class GitSoup(BeautifulSoup):
    def __init__(self, html, praser="html.parser", **kwargs):
        super().__init__(html, praser, **kwargs)
        self.html = html
        self.praser = "html.praser"