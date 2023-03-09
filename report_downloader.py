# -*- coding: utf-8 -*- 

import requests
import time
import pandas as pd
import random
import os
import json
import re
import datetime


def download_report_df_data_sh():
    file_path = "E:/p/reports2"
    is_financial_keys = ["银行", "证券", "商行", "保险", "金控", "期货", "资本", "财富", "金科"]
    begin = datetime.date(2020, 1, 19)
    end = datetime.date(2020, 6, 21)
    df = pd.DataFrame(columns=['证券代码', '简称', '文件路径', '年表标题'])
    for i in range((end - begin).days + 1):
        try:
            searchDate = str(begin + datetime.timedelta(days=i))
            response = requests.get(
                'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?&jsonCallBack=jsonpCallback43752&productId=&reportType2=DQGG&reportType=YEARLY&beginDate=' + searchDate + '&endDate=' + searchDate + '&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1561094157400',
                headers={'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/regular/'}
            )
            for report in json.loads(response.text[19:-1])['result']:
                download_url = 'http://www.sse.com.cn/' + report['URL']
                secName = report['title']
                if re.search('年度报告', secName, re.S):
                    if any(x in secName for x in is_financial_keys) or any(x in secName for x in ["摘要"]):
                        continue
                    search_date = (re.search(r"(\d{4})", secName))
                    if search_date == None or int(search_date.group(1)) not in range(2007, 2020):
                        continue
                    filename = report['security_Code'] + secName[0:search_date.span()[0]] + search_date.group(1) + ".pdf"
                    filename = filename.replace("关于", "")
                    filename = filename.replace("*ST", "-ST")
                    filename = filename.replace("*", "")
                    print("Downloading {} ....".format(filename))
                    resource = requests.get(download_url, stream=True)
                    with open(os.path.join(file_path, filename), "wb") as fd:
                        for y in resource.iter_content(102400):
                            fd.write(y)
        except Exception as e:
            continue


def get_pdf_address_sz(pageNum, is_finance_company=False):
    url = 'http://www.szse.cn/api/disc/announcement/annList?random=%s' % random.random()
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/json',
        'Host': 'www.szse.cn',
        'Origin': 'http://www.szse.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.szse.cn/disclosure/listed/fixed/index.html',
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36',
        'X-Request-Type': 'ajax',
        'X-Requested-With': 'XMLHttpRequest'
    }
    pagenum = int(pageNum)
    payload = {"seDate": ["2007-03-01", "2020-12-04"], "channelCode": ["fixed_disc"], "bigCategoryId": ["010301"],
               "pageSize": 30,
               "pageNum": pagenum, "sortSecCode": "asc"}
    if is_finance_company:
        payload["bigIndustryCode"] = ["J"]
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    return result


def get_report_df_data_sz():
    df = pd.DataFrame(columns=['证券代码', '简称', '文件路径', '年表标题'])
    count = 0
    url_head = 'http://disc.static.szse.cn/download/'
    finance_company_codes = get_finance_company_codes()
    for i in range(300, 301):
    # for i in range(115, 501):
        print("爬取第{}页".format(i))
        result = get_pdf_address_sz(i)
        if len(result["data"]) == 0:
            break
        num = len(result['data'])
        for index in range(num):
            secCode = result['data'][index]['secCode'][0]
            secName = result['data'][index]['secName'][0]
            title = result['data'][index]['title']
            search_date = (re.search(r"(\d{4})", title))
            if any(x in secName for x in ["银行", "证券", "保险"]) or any(
                    x in title for x in ["（已取消）", "摘要", "（英文版）"]) or search_date == None or int(
                    search_date.group(1)) not in range(2007, 2020) or secCode in finance_company_codes:
                continue
            df.at[count, '具体年度'] = search_date.group(1)
            df.at[count, '证券代码'] = secCode
            df.at[count, '简称'] = secName
            df.at[count, '文件路径'] = url_head + result['data'][index]['attachPath']
            df.at[count, '年表标题'] = title
            count += 1
        time.sleep(random.uniform(1, 2))
    return df


def download_report_pdf_sz(df):
    file_path = "E:/p/reports"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    for index in range(df.shape[0]):
        Stkcd = df.at[index, '证券代码']
        firm_name = df.at[index, '简称'].replace("*", "")
        Year = df.at[index, '具体年度']
        file_name = "{}{}{}.pdf".format(Stkcd, firm_name, Year)
        file_url = df.at[index, '文件路径']
        print("'[{}]' Downloading ....".format(file_name))
        rs = requests.get(file_url, headers=headers, stream=True)
        with open(os.path.join(file_path, file_name), "wb") as fp:
            for chunk in rs.iter_content(chunk_size=10240):
                if chunk:
                    fp.write(chunk)
        time.sleep(random.uniform(1, 2))


def get_finance_company_codes():
    sets = set()
    for i in range(1, 501):
        # print("爬取深交所年报下载地址第{}页".format(i))
        result = get_pdf_address_sz(i, True)
        if len(result["data"]) == 0:
            break
        for index in range(len(result['data'])):
            sets.add(result['data'][index]['secName'][0])
    return list(sets)


def main():
    # df_sz = get_report_df_data_sz()
    # download_report_pdf_sz(df_sz)
    download_report_df_data_sh()


if __name__ == '__main__':
    main()

# 2007-2019 年间有过 ST 特殊处理、退市
# 上市公司 IPO
# 连续三年及以上
