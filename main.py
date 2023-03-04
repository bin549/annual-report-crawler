import requests
import time
import pandas as pd
import random
import os
import json


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


def main():
    pdf_infor = pd.DataFrame(columns=['证券代码', '简称', '年表路径', '年表标题', '发布时间'])
    count = 0
    url_head = 'http://disc.static.szse.cn/download/'

    for i in range(1, 10):
        print("爬取深交所年报下载地址第{}页".format(i))
        result = get_pdf_address(i)
        num = len(result['data'])
        for index in range(num):
            secName = result['data'][index]['secName'][0]
            title = result['data'][index]['title']
            if any(x in secName for x in ["银行"]) or any(x in title for x in ["（已取消）", "摘要" , "（英文版）"]):
                continue
            pdf_infor.at[count, '证券代码'] = result['data'][index]['secCode'][0]
            pdf_infor.at[count, '简称'] = secName
            pdf_infor.at[count, '年表路径'] = url_head + result['data'][index]['attachPath']
            pdf_infor.at[count, '年表标题'] = title
            pdf_infor.at[count, '发布时间'] = result['data'][index]['publishTime']
            count += 1
        print(pdf_infor)
        print('获取完成')
        time.sleep(random.uniform(1, 2))
    pdf_infor['Year'] = pdf_infor['年表标题'].str.extract('([0-9]{4})')
    file_path = "/Users/Shared/annual-report-crawler/reports"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    # for each in range(pdf_infor.shape[0]):
    #     Stkcd = pdf_infor.at[each, 'secCode']
    #     firm_name = pdf_infor.at[each, 'secName'].replace("*", "")
    #     Year = pdf_infor.at[each, 'Year']
    #     print("开始下载{}，股票代码{}的{}年报".format(firm_name, Stkcd, Year))
    #     file_name = "{}{}{}.pdf".format(Stkcd, firm_name, Year)
    #     file_full_name = os.path.join(file_path, file_name)
    #     pdf_url = pdf_infor.at[each, 'url']
    #     rs = requests.get(pdf_url, headers=headers, stream=True)
    #     with open(file_full_name, "wb") as fp:
    #         for chunk in rs.iter_content(chunk_size=10240):
    #             if chunk:
    #                 fp.write(chunk)
    #     time.sleep(random.uniform(1, 2))
    #     print("===================下载完成==========================")


# 、证券、保险
# 2007-2019 年间有过 ST 特殊处理、退市
# 上市公司 IPO
# 连续三年及以上

def classification():
    topic = {
        "人工智能技术":
            ["人工智能",
             "商业智能",
             "图像理解",
             "投资决策辅助系统",
             "智能数据分析",
             "智能机器人",
             "机器学习",
             "深度学习",
             "语义搜索",
             "生物识别技术",
             "人脸识别",
             "语音识别",
             "身份验证",
             "自动驾驶",
             "自然语言处理"],
        "人工智能技术":
            [
                "大数据",
                "数据挖掘",
                "文本挖掘",
                "数据可视化",
                "异构数据",
                "征信",
                "增强现实",
                "混合现实",
                "虚拟现实"],
        "云计算技术": [
            "云计算",
            "流计算",
            "图计算",
            "内存计算",
            "多方安全计算",
            "认知计算",
            "融合架构",
            "亿级并发",
            "EB",
            "物联网",
            "信息物理系统"],
        "区块链技术":
            ["区块链",
             "数字货币",
             "分布式计算",
             "差分隐私技术",
             "智能金融合约"],
        "数字技术运用":
            [
                "C2B",
                "O2O",
                "网联",
                "智能穿戴",
                "移动支付",
                "第三方支付",
                "NPC", "支付",
                "移动互联网",
                "工业互联网",
                "移动互联",
                "互联网医疗",
                "电子商务",
                "级存储", "智能能源",
                "B2B",
                "B2C",
                "智慧农业",
                "智能交通",
                "智能医疗",
                "智能客服",
                "智能家居",
                "智能投顾",
                "智能文旅",
                "智能环保",
                "智能电网",
                "智能营销",
                "数字营销",
                "无人零售",
                "互联网金融",
                "数字金融",
                "Fintech",
                "金融科技",
                "量化金融",
                "开放银行"]
    }

if __name__ == '__main__':
    main()
