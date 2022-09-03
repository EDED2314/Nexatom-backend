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
                thing = str(g.text).replace("\n", "").replace("\r", "").strip().strip("%")
                idx = None
                for i in range(len(thing)):
                    try:
                        if thing[-(i+1)] != ".":
                            float(thing[-(i+1)])
                    except ValueError:
                        idx = -(i+1)
                        break
                    
                print(thing[0:idx])
                print(thing[idx:len(thing)-1])
                langs.append({thing[0:idx].strip(): thing[idx:len(thing)-1].strip()})
        
        return langs
                
        