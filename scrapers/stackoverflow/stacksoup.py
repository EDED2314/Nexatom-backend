from bs4 import BeautifulSoup 

class StackSoup(BeautifulSoup):
    def __init__(self, html, praser="html.parser", **kwargs):
        super().__init__(html, praser, **kwargs)
        self.html = html
        self.praser = "html.praser"
    
    def findTopTags(self) -> list:
        tag_data = []
        div_tags = self.find("div", id="top-tags")
        div_tags = div_tags.find_all("div")[2]
        tags = div_tags.find_all("div", recursive=False)
        for tag in tags:
            a_tag = {}
            a_tag["name"] =str(tag.find("div", class_="flex--item ws-nowrap").text).strip()
            data_of_tag = {}
            more_data_of_name = tag.find("div", class_="flex--item ml-auto") 
            more_data_of_name = more_data_of_name.find_all("div", class_="flex--item d-flex ai-center")
            for data in more_data_of_name:
                first_n_second = data.find_all("div", recursive=False)
                first = first_n_second[0]
                second = first_n_second[1]
                data_of_tag[str(second.text).strip()] = str(first.text).strip()
            a_tag['data'] = data_of_tag
            tag_data.append(a_tag)
        return tag_data
    
    def findBadgeCounts(self):
        badges = {}
        badge_grid = self.find("div", class_="d-flex flex__fl-equal fw-wrap gs24").findChildren("div", recursive=False)
        # print(len(badge_grid))
        for idx, badge in enumerate(badge_grid):
            infoBox = badge.findNext().findNext()
            badgeInfo = str(infoBox.findChildren(recursive = False)[1].text).strip().split("\r\n")[0]
            badges[idx+1] = badgeInfo
        return badges
            
            

    

            
    
    
    