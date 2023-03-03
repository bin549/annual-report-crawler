import requests
import time
import pandas as pd
import random
import os
import json

def get_pdf_address(pageNum):
    url = 'http://www.szse.cn/api/disc/announcement/annList?random=%s' % random.random()
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01'
    ,'Accept-Encoding': 'gzip, deflate'
    ,'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    ,'Content-Type': 'application/json'
    ,'Host': 'www.szse.cn'
    ,'Origin': 'http://www.szse.cn'
    ,'Proxy-Connection': 'keep-alive'
    ,'Referer': 'http://www.szse.cn/disclosure/listed/fixed/index.html'
    ,'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36'
    ,'X-Request-Type': 'ajax'
    ,'X-Requested-With': 'XMLHttpRequest'}
    pagenum = int(pageNum)
    payload = {"seDate":["",""],"channelCode":["fixed_disc"],"bigCategoryId":["010301"],"pageSize":30,"pageNum":pagenum}
    response = requests.post(url,headers =headers,data = json.dumps(payload))
    result = response.json()
    return result



def main():
    pdf_infor= pd.DataFrame(columns =['secCode','secName','url','title','publishTime'])
    count = 0
    url_head ='http://disc.static.szse.cn/download/'
    for i in range(1,2):
        print("爬取深交所年报下载地址第{}页".format(i))
        result = get_pdf_address(1)
        num = len(result['data'])
        print(num)
        for each in range(num):
            pdf_infor.at[count,'secCode'] = result['data'][each]['secCode'][0]
            pdf_infor.at[count,'secName'] = result['data'][each]['secName'][0]
            print(url_head + result['data'][each]['attachPath'])
            pdf_infor.at[count,'url'] = url_head + result['data'][each]['attachPath']
            pdf_infor.at[count,'title'] = result['data'][each]['title']
            pdf_infor.at[count,'publishTime'] = result['data'][each]['publishTime']
            count += 1
        print(pdf_infor)
        print('获取完成')
        time.sleep(random.uniform(1,2))




if __name__ == '__main__':
    main()
