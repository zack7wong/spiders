from bs4 import BeautifulSoup as bsp
import requests
import time
import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from PIL import Image
from os import path
import numpy as np

def tieba_crawl():
    # Tieba search keyword
    keyword = input("Please input your search keyword:")

    pageNumber = int(input("Please input the number of pages that your want to crawl:"))
    # keyword="山东大学"
    # pageNumber=1
    # Change the page number into the number that can be used in the url
    pn = [str(i) for i in range(0, ((pageNumber * 50) + 1), 50)]
    filename = "tieba_" + keyword + "_" + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + ".txt"
    # Generate a list of params to be used in the url
    for i in range(pageNumber):
        params = {"kw": keyword, "ie": "utf-8", "pn": pn[i]}

        # Use requests to get the corresponding pages
        r = requests.get("http://tieba.baidu.com/f", params=params, timeout=5)

        # Wait 3 seconds for each page
        time.sleep(3)

        # Extract page content using bsp library
        page_content = bsp(r.content, "html.parser")

        # Extract titles from the content
        titles1 = page_content.find_all(class_="j_th_tit ")
        autor1 = page_content.find_all(class_='tb_icon_author ')
        time1 = page_content.find_all(class_='pull-right is_show_create_time')


        # Remove unnecessary codes from the titles
        titles2 = [title.text for title in titles1]
        autor2 = [autor.text for autor in autor1]
        time2 = [time_.text for time_ in time1]

        # Save the titles into file,using append mode

        try:
            with open(filename, mode="a", encoding="utf-8") as f:
                f.truncate()
                for i in range(len(autor2)):
                    f.write('%s\t%s\t%s\n' % (titles2[i], autor2[i], time2[i]))
        except FileNotFoundError:
            print(filename, "not found.")
    return filename


def get_ciyun(filename):
    text = open(filename, "rb").read()
    # 结巴分词
    wordlist = jieba.cut(text, cut_all=True)
    wl = " ".join(wordlist)

    d = path.dirname(__file__)

    alice_mask = np.array(Image.open(path.join(d, "baidu.jpeg")))
    # 设置词云
    wc = WordCloud(background_color="white",  # 设置背景颜色
                   mask=alice_mask,  # 设置背景图片
                   max_words=2000,  # 设置最大显示的字数
                   # stopwords = "", #设置停用词
                   # font_path="C:\Windows\Fonts\SimHei.ttf",
                   font_path="/System/Library/Fonts/PingFang.ttc",
                   max_font_size=50,  # 设置字体最大值
                   random_state=30,
                   )
    myword = wc.generate(wl)  # 生成词云

    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()

# Call the function defined
filename = tieba_crawl()
get_ciyun(filename)


