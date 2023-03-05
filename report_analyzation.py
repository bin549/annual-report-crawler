import PyPDF2
import re
import jieba
import os

word_dat = {
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
    "大数据技术":
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


def main():
    file_root = "./reports/"
    jieba.load_userdict('wordWeight.txt')
    for x, y in word_dat.items():
        print("----------------")
        for key_word in y:
            print("----------------")
            print(key_word)
            print("--------")
            print(" {} {} {}".format("公司代码", "年份", "词频"))
            for filename in sorted(os.listdir(os.path.join(file_root))):
                name, ext = os.path.splitext(filename)
                if ext != ".pdf":
                    continue
                f = open(file_root + filename, 'rb')
                pdf_reader = PyPDF2.PdfReader(f)
                word_frequent = 0
                for i in range(0, len(pdf_reader.pages)):
                    text = pdf_reader.pages[i].extract_text()
                    word_frequent += list(jieba.cut(text, cut_all=False, HMM=True)).count(key_word)
                print("  {}  {}  {}".format((re.search(r"(\d{6})", filename)).group(1),
                                            (re.search(r"(\d{4}).pdf", filename)).group(1), word_frequent))
        # print(jieba.lcut(page_one_text))
        # print('|'.join(jieba.cut(page_one_text, cut_all=False, HMM=True)))


if __name__ == '__main__':
    main()

# if __name__ == '__main__':
# #  公司代码 年份 词频
# # 0000001 2007 5
# # 0000001 2008 7