from bs4 import BeautifulSoup
import aiohttp

class GitSoup(BeautifulSoup):
    def __init__(self, html, praser="html.parser", **kwargs):
        super().__init__(html, praser, **kwargs)
        self.html = html
        self.praser = "html.praser"
    
    def getLangsHtml(self):
        langs = []
        mainCardBody = self.find("svg", {"data-testid":"lang-items"})
        info = mainCardBody.find("g", transform="translate(0, 25)")
        infos = info.find_all("g", recursive=False)
        for info in infos:
            gs = info.find_all("g", recursive = False)
            for g in gs:
                langs.append(str(g.text).replace("\n", "").replace("\r", "").strip())
        
        return langs
                
        