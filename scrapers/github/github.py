from bs4 import BeautifulSoup
import aiohttp
from  scrapers.github.gitsoup import GitSoup
import json
import base64




class GithubInfo():
    def __init__(self, username:str):
        self.username = username
        self.rootUrl = "https://api.github.com/users"
        self.langsUrl = f"https://github-readme-stats.vercel.app/api/top-langs?username={username}&show_icons=true&theme=dark&locale=en&langs_count=10&layout=compact"
        
    async def getUserInfo(self):
        async with aiohttp.ClientSession() as session:
            repsonse = await session.get(url=f"{self.rootUrl}/{self.username}")
            return await repsonse.json()
            
                
    
    async def  getpfp(self, user_session: aiohttp.ClientSession):
        async with user_session as session:
            userInfo = await self.getUserInfo()
            async with session.get(url=userInfo["avatar_url"]) as response:
                test = await response.read()
                encoded_string = base64.b64encode(test)
                return  encoded_string
    
    async def getLangs(self, user_session:aiohttp.ClientSession):
        async with user_session as session:
            async with session.get(url=self.langsUrl) as response:
                html = await response.text()
                soup = GitSoup(html)
                langs = soup.getLangsHtml()
                return langs
                
                
                