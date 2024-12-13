import json
import os

import requests

from .utils import createDirs, downloadFile
from .google_patent_common import parseGooglePatentInfoHtml, GooglePatentInfo

def getHtml(url,proxies=None,headers=None):
    if proxies:
        if proxies=="clash":
            proxies = {
                'http': 'http://127.0.0.1:7890',
                'https': 'http://127.0.0.1:7890',
            }
    res=requests.get(url,proxies=proxies,headers=headers)
    res.encoding=res.apparent_encoding
    return res.text
def getGooglePatentInfoByUrl(url,proxies=None,headers=None,engine="lxml"):
    html=getHtml(url,proxies=proxies,headers=headers)
    return parseGooglePatentInfoHtml(html,url,engine)

def getGooglePatentInfo(query_txt,base_url="https://patents.google.com",proxies=None,headers=None,language="auto",engine="lxml"):
    if language == "auto":
        if query_txt.find("CN")!=-1:
            language = "zh"
        else:
            language = "en"
    url=f"{base_url}/patent/{query_txt}/{language}?oq={query_txt}"
    d=getGooglePatentInfoByUrl(url,proxies=proxies,headers=headers,engine=engine)
    if d is None:
        return None
    return GooglePatentInfo(**d)
def downloadGooglePdf(pdf_url,save_path):
    return downloadFile(pdf_url,save_path)
def autoGoogleSpider(query_txt,save_dir="data",save_pdf=True,base_url="https://patents.google.com",proxies=None,headers=None):
    google_patent_info=getGooglePatentInfo(query_txt,base_url=base_url,proxies=proxies,headers=headers)
    if google_patent_info is None:return False
    createDirs(save_dir)
    base_patent_dir = os.path.join(save_dir, google_patent_info.publication_number)
    createDirs(base_patent_dir)
    patent_info_dataframe,patent_content_dataframe=google_patent_info.toDataFrame()

    patent_info_file = os.path.join(base_patent_dir, f"info.xlsx")
    patent_info_dataframe.to_excel(patent_info_file,index=False)

    patent_content_file = os.path.join(base_patent_dir, f"content.xlsx")
    patent_content_dataframe.to_excel(patent_content_file,index=False)
    with open(os.path.join(base_patent_dir, f"origin_data.json"), "w", encoding="utf-8") as f:
        json.dump(google_patent_info.__dict__, f, ensure_ascii=False)
    if save_pdf:
        patent_pdf_file = os.path.join(base_patent_dir, f"patent.pdf")
        downloadGooglePdf(google_patent_info.pdf_url, patent_pdf_file)
    return True
