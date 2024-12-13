import pandas as pd
from bs4 import BeautifulSoup

class FpoSearchResult:
    def __init__(self, url,label,pub_num, patent_title, patent_abstract,patent_total_num,page):
        self.label=label
        self.pub_num = pub_num
        self.patent_title = patent_title
        self.patent_abstract = patent_abstract
        self.url = url
        self.patent_total_num=patent_total_num
        self.page=page

class FpoPatentInfo:
    def __init__(self,url,pub_num,title,abstract,inventors,application_number,publication_date,filing_date,assignee,primary_class,other_classes,international_classes,field_of_search,pdf_url,view_patent_images,us_patent_references,other_references,primary_examiner,attorney_agent_or_firm,claims,description):
        self.url=url
        self.pub_num=pub_num
        self.title=title
        self.abstract=abstract
        self.inventors=inventors
        self.application_number=application_number
        self.publication_date=publication_date
        self.filing_date=filing_date
        self.assignee=assignee
        self.primary_class=primary_class
        self.other_classes=other_classes
        self.international_classes=international_classes
        self.field_of_search=field_of_search
        self.pdf_url=pdf_url
        self.us_patent_references=us_patent_references
        self.other_references=other_references
        self.primary_examiner=primary_examiner
        self.attorney_agent_or_firm=attorney_agent_or_firm
        self.claims=claims
        self.descriptions=description
        self.view_patent_images=view_patent_images
    def toDataFrame(self):
        x={
            'pub_num':[self.pub_num],
            'title':[self.title],
            'abstract':[self.abstract],
            'inventors':[self.inventors],
            'application_number':[self.application_number],
            'publication_date':[self.publication_date],
            'filing_date':[self.filing_date],
            'assignee':[self.assignee],
            'primary_class':[self.primary_class],
            'other_classes':[self.other_classes],
            'international_classes':[self.international_classes],
            'field_of_search':[self.field_of_search],
            'pdf_url':[self.pdf_url],
            'us_patent_references':[self.us_patent_references],
            'other_references':[self.other_references],
            'primary_examiner':[self.primary_examiner],
            'attorney_agent_or_firm':[self.attorney_agent_or_firm],
            'claims':[self.claims],
        }
        x1={

        }
        for k,v in self.descriptions.items():
            x1[k]=[v]
        return pd.DataFrame(x),pd.DataFrame(x1)
def parseFpoPatentSearchHtml(html,page,engine="lxml"):
    soup = BeautifulSoup(html, engine)
    # 获取专利总量
    patent_total_num = soup.select_one("#hits")["value"]
    t_table = soup.select_one("#results > div.legacy-container > div > div > table")
    tr_list = t_table.find_all("tr")[1:]
    res = []
    for tr in tr_list:
        td_list = tr.find_all("td")
        label = int(td_list[0].get_text())
        id = td_list[1].get_text().strip()
        url = f"https://www.freepatentsonline.com" + td_list[2].find("a")["href"]
        title = td_list[2].find("a").get_text().strip()
        abstract = td_list[2].get_text().split("\n")[-1].strip()
        res.append(FpoSearchResult(url, label, id, title, abstract, patent_total_num, page))
    return res

def parseFpoPatentInfoHtml(html,url,engine="lxml"):
    soup = BeautifulSoup(html, engine)
    wrapper = soup.select_one("body > div > div > div.fixed-width.document-details-wrapper")
    div_list = wrapper.find_all("div", {"class": "disp_doc2"})
    field_dict = {'title': '', 'abstract': '', 'inventors': '', 'application_number': '', 'publication_date': '',
                  'filing_date': '', 'assignee': '', 'primary_class': '', 'other_classes': '',
                  'international_classes': '', 'field_of_search': '', 'view_patent_images': '',
                  'us_patent_references': '', 'other_references': '', 'primary_examiner': '',
                  'attorney_agent_or_firm': '', 'claims': '', 'description': ''}
    for div in div_list:
        div_title = div.find("div", {"class": "disp_elm_title"})
        div_text = div.find("div", {"class": "disp_elm_text"})
        if div_title:
            title = div_title.get_text().replace(" ", "_").lower().replace(",", "").replace(":", "")
            text = div_text.get_text().strip()
            if title not in field_dict.keys(): continue
            if title == "inventors":
                text = text.replace("\n", ";").replace(" ", "")
            if title == "other_classes":
                text = text.replace("\n", "").replace(" ", "")
            if title == "view_patent_images":
                field_dict["pdf_url"] = "https://www.freepatentsonline.com" + div_text.find("a")["href"]
            if title == "other_references":
                text_list = text.split("\n")
                for index, t in enumerate(text_list):
                    text_list[index] = t.strip()
                text = "|".join(text_list)
            if title == "us_patent_references":
                tr_list = div_text.find_all("tr")
                res_list = []
                for tr in tr_list:
                    us_patent_references_dict = {}
                    td_list = tr.find_all("td")
                    us_patent_references_dict["patent_id"] = td_list[0].get_text().strip()
                    us_patent_references_dict["title"] = td_list[1].get_text().strip()
                    us_patent_references_dict["date"] = td_list[2].get_text().strip()
                    us_patent_references_dict["author"] = td_list[3].get_text().strip()
                    res_list.append(us_patent_references_dict)
                text = res_list
            if title == "description":
                text = div_text.get_text().strip()
            field_dict[title] = text
    field_dict["url"] = url
    return field_dict

def dictToFpoPatentInfo(d,pub_num=None):
    if "pub_num" not in d:
        if pub_num is None:
            raise Exception("请指定pub_num作为唯一标识")
        else:
            d["pub_num"]=pub_num
    return FpoPatentInfo(**d)