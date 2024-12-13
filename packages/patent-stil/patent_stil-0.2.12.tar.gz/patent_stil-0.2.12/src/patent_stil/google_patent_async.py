import json
import os

from aiohttp import ClientSession

from .google_patent_common import parseGooglePatentInfoHtml, GooglePatentInfo
from .utils import createDirs, downloadFile

async def getHtmlAsync(url,proxies=None,headers=None):
    if proxies:
        if proxies=="clash":
            proxies = 'http://127.0.0.1:7890'
    async with ClientSession() as session:
        async with session.get(url,proxy=proxies,headers=headers) as response:
            return await response.text(encoding="utf-8")

async def getGooglePatentInfoByUrlAsync(url,proxies=None,headers=None):
    html=await getHtmlAsync(url,proxies,headers)
    return parseGooglePatentInfoHtml(html,url)
async def dictToGooglePatentInfoAsync(d):
    return GooglePatentInfo(**d)
async def getGooglePatentInfoAsync(query_txt,base_url="https://patents.google.com",proxies=None,headers=None,language="auto"):
    if language == "auto":
        if query_txt.find("CN")!=-1:
            language = "zh"
        else:
            language = "en"
    url=f"{base_url}/patent/{query_txt}/{language}?oq={query_txt}"
    d=await getGooglePatentInfoByUrlAsync(url,proxies=proxies,headers=headers)
    if d is None:
        return None
    return await dictToGooglePatentInfoAsync(d)
async def downloadGooglePdfAsync(pdf_url,save_path):
    return downloadFile(pdf_url,save_path)
async def autoGoogleSpiderAsync(query_txt,save_dir="data",save_pdf=True,base_url="https://patents.google.com",proxies=None,headers=None):
    google_patent_info=await getGooglePatentInfoAsync(query_txt,base_url=base_url,proxies=proxies,headers=headers)
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
        await downloadGooglePdfAsync(google_patent_info.pdf_url, patent_pdf_file)
    return True
