import aiohttp
from  scrapers.stackoverflow.stacksoup import StackSoup

class StackoverflowInfo():
    def __init__(self, user_url: str) -> None:
        self.url = user_url
    
    async def  findTags(self, user_session: aiohttp.ClientSession):
        async with user_session as session:
            async with session.get(url=self.url) as response:
                html = await response.text()
                soup = StackSoup(html)
                top_tags = soup.findTopTags()
                return(top_tags)
                
    async def findBadges(self, user_session: aiohttp.ClientSession):
        async with user_session as session:
            async with session.get(url=self.url) as response:
                html = await response.text()
                soup = StackSoup(html)
                badges = soup.findBadgeCounts()
                return(badges)


# async def main():
#     Stackoverflow = StackoverflowInfo("https://stackoverflow.com/users/1/jeff-atwood")
#     async with aiohttp.ClientSession() as session:
        
#         value = await Stackoverflow.findTags(session)
#         # value = await Stackoverflow.findBadges(session)
#         return value
    
# loop = asyncio.get_event_loop()
# print(loop.run_until_complete(main()))