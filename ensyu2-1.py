#演習２


from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd

#URLの設定、アクセス
url="https://next.rikunabi.com/rnc/docs/cp_s00700.jsp?jb_type_long_cd=0100000000&wrk_plc_long_cd=0313000000&wrk_plc_long_cd=0313100000&wrk_plc_long_cd=0314000000"
#siteがメンテナンスを設けているとずっとアクセスし続けることになるので、タイムアウトを設定
r=requests.get(url,timeout=3)
r.raise_for_status()


#BSで解析
soup=BeautifulSoup(r.content,"lxml")

#それぞれの企業情報を格納しているところを探し、指定する　　"div",class_=layoutList02
#companiesに対してfor ループを回す
#企業名がどこに入っているか確認
#top pageから取得したい情報は『求人詳細を見る』のURL

companies=soup.select(".rnn-group")

d_list=[]
for i,company in enumerate(companies):
    print(i)
    company_name=company.select_one(".rnn-linkText").text
    page_url=company.select_one(".rnn-linkText").get("href")

    page_url=page_url.replace("nx1","nx2")
    sleep(3)

    page_r=requests.get(page_url,timeout=3)
    page_r.raise_for_status()
    page_soup=BeautifulSoup(page_r.content,"lxml")
    table=page_soup.select_one("#company_profile_table")
    company_url=table.select_one("a")　
    if company_url:
       company_url=company_url.get("href")

    d_list.append({"company_name":company_name,
                   "company_url":company_url
                  })


df=pd.DataFrame(d_list)
df.to_csv("company_listpt3.csv",index=None,encoding="utf-8-sig")
                  
