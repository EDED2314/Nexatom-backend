from bs4 import BeautifulSoup
import aiohttp
from  scrapers.github.gitsoup import GitSoup

class GithubInfo():
    def __init__(self, username:str):
        self.username = username
    
    async def  getpfp(self, user_session: aiohttp.ClientSession):
        async with user_session as session:
            async with session.get(url=self.url) as response:
                html = await response.text()
                soup = GitSoup(html)
                
                
                