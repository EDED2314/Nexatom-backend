from bs4 import BeautifulSoup
import aiohttp
from  scrapers.github.gitsoup import GitSoup
import json
import base64




class GithubInfo():
    def __init__(self, username:str):
        self.username = username
        self.rootUrl = "https://api.github.com/users"
        
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
                
                
                