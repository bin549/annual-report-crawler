# -*- coding: utf-8 -*- 

import PyPDF2
import re
import jieba
import os
import csv
from utils.decorator import timeit
import data

def format_print(company_frequent, word_frequent_dict, filename):
    if company_frequent == 0:
        print("                                 ")
        print("            - EMPTY -            ")
        print("                                 ")
    else:
        print("                                 ")
        print("       {} {}   {}    ".format("公司代码", "年份", "词频"))
        for key_word in word_frequent_dict:
            print("        {}  {}  {}-{}".format((re.search(r"(\d{6})", filename)).group(1),
                                                 (re.search(r"(\d{4}).pdf", filename)).group(1), key_word,
                                                 word_frequent_dict[key_word]))
        print("                                 ")



@timeit
def main():
    file_root = "./reports/"
    jieba.load_userdict('userDict.txt')
    rows = []
    header = ["公司代码", "年份", "词频"]
    for filename in sorted(os.listdir(os.path.join(file_root))):
        print("-----['{}']-----".format(filename))
        company_frequent = 0
        name, ext = os.path.splitext(filename)
        if ext != ".pdf":
            continue
        f = open(file_root + filename, 'rb')
        pdf_reader = PyPDF2.PdfReader(f)
        word_frequent_dict = {}
        for x, y in data.WORD_DIC.items():
            for key_word in y:
                word_frequent_dict[key_word] = 0
        pdf_page_size = 40 if len(pdf_reader.pages) > 40 else len(pdf_reader.pages)
        for i in range(0, pdf_page_size):
            text = pdf_reader.pages[i].extract_text()
            for word_key in word_frequent_dict.keys():
                word_frequent = list(jieba.cut(text, cut_all=False, HMM=True)).count(word_key)
                if word_frequent != 0:
                    word_frequent_dict[word_key] += word_frequent
        word_frequent_dict = {x: y for x, y in word_frequent_dict.items() if y != 0}
        for key_word in word_frequent_dict:
            company_frequent += word_frequent_dict[key_word]
        format_print(company_frequent, word_frequent_dict, filename)
        rows.append({'公司代码': (re.search(r"(\d{6})", filename)).group(1),
                     '年份': (re.search(r"(\d{4}).pdf", filename)).group(1),
                     '词频': "{}".format(company_frequent)
                     })
        print("------------------------------------")

    with open('report_output.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    main()
