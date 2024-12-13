import json
import os.path

import requests
from bs4 import BeautifulSoup

from .common import getUSApplicationID
from .fpo_patent_common import parseFpoPatentInfoHtml, parseFpoPatentSearchHtml, FpoSearchResult, FpoPatentInfo, \
    dictToFpoPatentInfo
from .utils import createDirs, downloadFile

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
def getFpoSearchResult(query_txt,page=1,sort="relevance",srch="top",patents_us="on",patents_other="off",proxies=None,headers=None):
    url=f"https://www.freepatentsonline.com/result.html?p={page}&sort={sort}&srch={srch}&query_txt={query_txt}&submit=&patents_us={patents_us}&patents_other={patents_other}"
    html=getHtml(url,proxies=proxies,headers=headers)
    if page>200:
        raise Exception("无法浏览超过200页的数据")
    res=parseFpoPatentSearchHtml(html,page=page)
    return res

def getFpoPatentInfoByUrl(url,engine="lxml",proxies=None,headers=None):
    html=getHtml(url,proxies=proxies,headers=headers)
    return parseFpoPatentInfoHtml(html,url=url,engine=engine)
def getFpoPatentInfo(patent_pub_num,engine="lxml",proxies=None,headers=None):
    if patent_pub_num.find("US")!=-1:
        fpo_id=getUSApplicationID(patent_pub_num)
        if fpo_id is None:
            raise Exception("解析专利号出错",patent_pub_num)
    else:
        fpo_id=patent_pub_num
    url = f"https://www.freepatentsonline.com/{fpo_id}.html"
    field_dict = getFpoPatentInfoByUrl(url,engine=engine,proxies=proxies,headers=headers)
    field_dict["pub_num"] = patent_pub_num
    return dictToFpoPatentInfo(field_dict)
def getFpoPatentInfoBySearch(fpo_search_result:FpoSearchResult):
    field_dict=getFpoPatentInfoByUrl(fpo_search_result.url)
    field_dict["pub_num"]=fpo_search_result.pub_num
    return dictToFpoPatentInfo(field_dict)

def downloadFpoPdfByUrl(pdf_url,save_path):
    res=requests.get(pdf_url)
    soup=BeautifulSoup(res.text, "html.parser")
    url_obj=soup.select_one("body > div > div > div:nth-child(3) > center:nth-child(10) > iframe")
    if url_obj:
        return downloadFile(url_obj["src"],save_path)
    else:
        raise Exception(f"无效的地址解析,{pdf_url}")



def downloadFpoPdf(fpo_patent_info:FpoPatentInfo,save_dir):
    if os.path.basename(save_dir).find(".pdf")!=-1:
        downloadFpoPdfByUrl(fpo_patent_info.pdf_url,save_dir)
    else:
        save_dir=os.path.join(save_dir,f"{fpo_patent_info.pub_num}.pdf")
        downloadFpoPdfByUrl(fpo_patent_info.pdf_url,save_dir)
def autoFpoSpider(query_txt,save_dir="data",save_pdf=True,num_in_search=1,id_is_query=True):
    fpo_search_result_list=getFpoSearchResult(query_txt=query_txt)
    createDirs(save_dir)
    for index,fpo_search_result in enumerate(fpo_search_result_list):
        if index+1>num_in_search:
            break
        fpo_patent_info=getFpoPatentInfo(fpo_search_result)
        base_patent_dir=os.path.join(save_dir,fpo_patent_info.pub_num)
        if id_is_query:
            base_patent_dir = os.path.join(save_dir, query_txt)
        createDirs(base_patent_dir)

        patent_info_dataframe,patent_content_dataframe=fpo_patent_info.toDataFrame()
        patent_info_file=os.path.join(base_patent_dir,f"info.xlsx")
        patent_info_dataframe.to_excel(patent_info_file,index=False)

        patent_content_file = os.path.join(base_patent_dir, f"content.xlsx")
        patent_content_dataframe.to_excel(patent_content_file,index=False)

        with open(os.path.join(base_patent_dir, f"origin_data.json"), "w", encoding="utf-8") as f:
            json.dump(fpo_patent_info.__dict__, f, ensure_ascii=False)
        if save_pdf:
            patent_pdf_file = os.path.join(base_patent_dir, f"patent.pdf")
            downloadFpoPdfByUrl(fpo_patent_info.pdf_url,patent_pdf_file)