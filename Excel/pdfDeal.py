import glob
from os import path
import os
from aip import AipOcr
from wand.image import Image as wandImage
from PIL import Image
import re

def baiduOCR(picfile,file):
    filename = path.basename(picfile)

    APP_ID = '15106275' # 刚才获取的 ID，下同
    API_KEY = 'TVC9eWFb6KSQ7LwXvyPmLkgW'
    SECRECT_KEY = 'YxTEbw5o672QrfApzS7bKamNhK1zYNen'
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)

    i = open(picfile, 'rb')
    img = i.read()
    print("正在识别图片： " + filename)
    message = client.basicGeneral(img)   # 通用文字识别，每天 50 000 次免费
    #message = client.basicAccurate(img)   # 通用文字高精度识别，每天 800 次免费
    if message:
        print("识别成功！")
    i.close()
    for text in message.get('words_result'):
        if re.search('请号:(\d{7})',text['words']):
            rename_name = re.search('请号:(\d{7})',text['words']).group(1)
            rename_name = rename_name +'.pdf'
            print(rename_name)
            os.rename(file,rename_name)

def get_img(filename):
    jpeg_name = file.split('.')[0]+'.jpeg'
    with wandImage(filename=filename) as img:
        with img.convert('jpeg') as converted:
            converted.save(filename=jpeg_name)
    return jpeg_name

if __name__ == "__main__":
    files = os.listdir('./')

    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            if file.split('.')[-1] == 'pdf':
                print('正在处理'+file)
                try:
                    img_name = get_img(file)
                    baiduOCR(img_name,file)
                except:
                    print('处理失败')