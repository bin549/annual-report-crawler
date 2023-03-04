import requests
import time
import pandas as pd
import random
import os
import json
import re


def get_pdf_address(pageNum):
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
    payload = {"seDate": ["2007-03-01", "2020-12-04"], "channelCode": ["fixed_disc"], "bigCategoryId": ["010301"], "pageSize": 30,
               "pageNum": pagenum, "sortSecCode": "asc"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    return result

def part_01():
    df = pd.DataFrame(columns=['证券代码', '简称', '文件路径', '年表标题'])
    count = 0
    url_head = 'http://disc.static.szse.cn/download/'
    for i in range(10, 501):
        if i == 20:
            break
        # print("爬取深交所年报下载地址第{}页".format(i))
        result = get_pdf_address(i)
        num = len(result['data'])
        for index in range(num):
            secName = result['data'][index]['secName'][0]
            title = result['data'][index]['title']
            search_date = (re.search(r"(\d{4})", title))
            if any(x in secName for x in ["银行", "证券", "保险"]) or any(x in title for x in ["（已取消）", "摘要" , "（英文版）"]) or search_date == None or int(search_date.group(1)) not in range(2007, 2020):
                continue
            df.at[count, '具体年度'] = search_date.group(1)
            df.at[count, '证券代码'] = result['data'][index]['secCode'][0]
            df.at[count, '简称'] = secName
            df.at[count, '文件路径'] = url_head + result['data'][index]['attachPath']
            df.at[count, '年表标题'] = title
            count += 1
        time.sleep(random.uniform(1, 2))
    return df


def part_02(df):
    file_path = "/Users/Shared/annual-report-crawler/reports"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    for index in range(df.shape[0]):
        Stkcd = df.at[index, '证券代码']
        firm_name = df.at[index, '简称'].replace("*", "")
        Year = df.at[index, '具体年度']
        file_name = "{}{}{}.pdf".format(Stkcd, firm_name, Year)
        file_url = df.at[index, '文件路径']
        print("Downloading -- '{}'....".format(file_name))
        rs = requests.get(file_url, headers=headers, stream=True)
        with open(os.path.join(file_path, file_name), "wb") as fp:
            for chunk in rs.iter_content(chunk_size=10240):
                if chunk:
                    fp.write(chunk)
        time.sleep(random.uniform(1, 2))


def main():
    df = part_01()
    part_02(df)



# 2007-2019 年间有过 ST 特殊处理、退市
# 上市公司 IPO
# 连续三年及以上


if __name__ == '__main__':
    main()
