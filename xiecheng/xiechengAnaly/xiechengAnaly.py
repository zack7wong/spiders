import re
import time
import random
import jieba
from collections import defaultdict
import chardet

def words():
    with open('BosonNLP_sentiment_score.txt','r',encoding='utf-8') as f:
        sentiList=f.readlines()
    #print(len(sentiList))
    SentiDict=defaultdict()
    #SentiDict=defaultdict()
    for s in sentiList:
        #print(s)
        s=s.strip('\n')
        #print(s)
        #print(s.split(' ')[0])
        #print(s.split(' ')[1])
        #print('\n')
        try:
            SentiDict[s.split(' ')[0]]=s.split(' ')[1]
        except:
            pass
    # print(len(SentiDict))

    with open('NotList.txt','r',encoding='utf8') as f:
        NotList=f.readlines()
        NotList2=[]
        for line in NotList:
            line=line.strip('\n')
            #print(line)
            NotList2.append(line)
        #print(NotList2)
        # print(len(NotList2))

    with open('Degreelist.txt','r',encoding='gbk') as f:
        DegreeList=f.readlines()
        DegreeDict=defaultdict()
        #DegreeDict=defaultdict()
        n=0
        Degree=[0,2,1.25,1.2,0.8,0.5,1.5]
        for d in DegreeList:
            d=d.strip('\n')
            #print(d)
            cout=re.findall('\”.*?(\d+)',d)
            if len(cout):
                #print(cout)
                n=n+1
                continue
            if n>0:    
                DegreeDict[d]=Degree[n]
        # print(len(DegreeDict))
    return SentiDict,NotList2,DegreeDict

def classifywords(wordDict,SentiDict,NotList,DegreeDict):
    SentiWords=defaultdict()
    NotWords=defaultdict()
    DegreeWords=defaultdict()
    #print(wordDict)
    for word in wordDict.keys():
        if word in SentiDict.keys() and word not in NotList and word not in DegreeDict.keys():
            SentiWords[wordDict[word]] = SentiDict[word]
        elif word in NotList and word not in DegreeDict.keys():
            NotWords[wordDict[word]] = -1
        elif word in DegreeDict.keys():
            DegreeWords[wordDict[word]] = DegreeDict[word]
    #print(Sentiword)
    #print(Notword)
    #print(Degreeword)
    return SentiWords,NotWords,DegreeWords

def scoreSent(senWord, notWord, degreeWord, segResult):
    #print(senWord)
    #print(notWord)
    #print(degreeWord)
    #print(segResult)
    W = 1
    score = 0
    senLoc = senWord.keys()
    notLoc = notWord.keys()
    degreeLoc = degreeWord.keys()
    senloc = -1
    for i in range(0, len(segResult)):
        if i in senLoc:
            senloc += 1
            score += W * float(senWord[i])
            if senloc < len(senLoc) - 1:
                for j in range((list(senLoc))[senloc], (list(senLoc))[senloc + 1]):
                    if j in list(notLoc):
                        W *= -1
                    elif j in list(degreeLoc):
                        W *= float(degreeWord[j])
        if senloc < len(senLoc) - 1:
            i = (list(senLoc))[senloc + 1]
    return score

good_rates={}
words_value=words()
#print(words_value[0])
#print(words_value[1])
#print(words_value[2])
#print('喵')
comments_sum=0
for i in range(1,2):
    score_var=[]
    file_name='994291.txt'
    print(file_name)
    try:
        with open(file_name, 'r', encoding='utf-8',errors='ignore') as f:
            for line in f.readlines():
                segList = jieba.cut(line)

                segResult = []
                for w in segList:
                    segResult.append(w)
                print(line.strip())
                print(segResult)
                with open('Stopwordlist.txt', 'r', encoding='utf8') as f:
                    stopwords = f.readlines()
                    #print(stopwords)
                    newSent = []
                    for word in segResult:
                        if word+'\n' in stopwords:
                            continue
                        else:
                            newSent.append(word)
                    datafen_dist={}
                    for x in range(0, len(newSent)):
                        datafen_dist[newSent[x]]=x
                    #datafen_dist=listToDist(data)
                    #print(datafen_dist)
                    data_1=classifywords(datafen_dist,words_value[0],words_value[1],words_value[2])
                    #print('\n1\n',data_1[0],'\n2\n',data_1[1],'\n3\n',data_1[2])
                    segResult_P = []
                    segList_P = jieba.cut(line)
                    for w in segList_P:
                        segResult_P.append(w)
                    data_2=scoreSent(data_1[0],data_1[1],data_1[2],newSent)
                    print(data_2)
                    if data_2>0:
                        print('好评\n')
                    elif data_2 < 0:
                        print('差评\n')
                    else:
                        print('中评\n')

                    score_var.append(data_2)
        #print(score_var,'\n\n')
        good=0
        normal=0
        bad=0
        for score in score_var:
            if score>0:
                good=good+1
            elif score<0:
                bad=bad+1
            else:
                normal=normal+1
        # print('good_comments:',good,'normal_comments:',normal,'bad_comments:',bad,'Total_comments:',good+normal+bad)
        good_comments_rate=good/(good+normal+bad)
        # print('文本评论好评率：%.2f%%'%(good_comments_rate*100))
        comments_sum=comments_sum+good+normal+bad
        good_rates[i]=good_comments_rate
        #print(good_rates)
    except:
        print('文件不存在！')

# print('总获取的评论数量：',comments_sum)
#
# #原始排序
# with open('994291.txt','r',encoding='utf-8') as f:
#     txt=f.read()
#     print(type(txt))
#
# text=re.findall('\"(.*?)\"\:.*?\"(.*?)\"\,',txt,re.S)
# i=1
# print('原始排序为：')
# for line in text:
#     line=list(line)
#     line[1]=i
#     i=i+1
#     print(line)
#
# #新的排序
# sorted_good_rates=sorted(good_rates.items(),key=lambda item:item[1],reverse=True)
# print(sorted_good_rates)
# print('新的排序为：')
# for line1 in sorted_good_rates:
#     line1=list(line1)
#     #print(line1)
#     i=1
#     for line2 in text:
#         line2=list(line2)
#         line2[1]=i
#         i=i+1
#         #print(line2)
#         if line2[1]==line1[0]:
#             line2[1]=line1[1]
#             print(line2)