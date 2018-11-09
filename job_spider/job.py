#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from job_spider import download
from job_spider import config
# import download
# import config
import db
import time
import json

class Job(object):
    def __init__(self):
        # with open('results.csv','w') as f:
        #     write_res = 'id,用户名,性别,年龄,应聘职位,应聘类型,教育程度,城市,期望薪资,在职状态,工作年限,期望工作性质,入学时间,毕业时间,学校,专业,简历修改时间,自我评价,工作1,工作2,工作3,项目1,项目2,项目3' + '\n'
        #     f.write(write_res)
        #实例化db
        self.mysql = db.MysqlClient()

        #cityid 上海538 苏州639
        self.start_url = 'https://rd5.zhaopin.com/api/custom/search/resumeListV2?_=1540959006801&x-zp-page-request-id=50d84efd11d84f49b1b88d22d774142d-1540958517096-790847'
        self.download = download.Download()

    def get_url(self):
        item_list = []
        for i in range(1, 2):
            pageToken = i
            shanghai_body = {"start":1,"rows":60,"S_DISCLOSURE_LEVEL":2,"S_EXCLUSIVE_COMPANY":"中高科技;研发部","S_DATE_MODIFIED":"181031,181031","S_CURRENT_CITY":"538","S_ENGLISH_RESUME":"1","isrepeat":1,"sort":"complex"}
            shanghai_body['start'] = pageToken
            shanghai_obj = {
                'url': self.start_url,
                'body': shanghai_body,
                'type': '上海'
            }
            item_list.append(shanghai_obj)
        return item_list

        suzhou_body = {"start":2,"rows":60,"S_DISCLOSURE_LEVEL":2,"S_EXCLUSIVE_COMPANY":"中高科技;研发部","S_DATE_MODIFIED":"181028,181031","S_CURRENT_CITY":"538","S_ENGLISH_RESUME":"1","isrepeat":1,"sort":"complex"}

    def parse_html(self, response,url_obj):
        json_obj = json.loads(response)
        if json_obj['code'] == 1:
            with open('failed.txt','a') as f:
                f.write(str(url_obj) + '\n')
            return None
        edu_list = []
        project_list = []
        work_list = []
        for data in json_obj['data']['dataList']:
            jobId = data['id']
            name = data['userName']
            try:
                age = int(data['age'])
            except:
                age = 0
            sex = data['gender']
            url = 'https://rd5.zhaopin.com/resume/detail?resumeNo={id}_1_1%3B{key}%3B{time}'.format(id=data['id'], key=data['k'], time=data['t'])
            imgUrl = 'http:' + data['portrait'] if data['portrait'] != '' else ''
            jobTitle = data['jobTitle'] #应聘职位
            jobType = data['jobType']  #应聘类型
            eduLevel = data['eduLevel'] #教育程度
            city = data['city']
            desiredSalary = data['desiredSalary'] #期望薪资
            careerStatus = data['careerStatus'] #离职状态
            workYears = int(data['workYears']) if data['workYears'] != '' else 0
            modifyDate = '20' + data['modifyDate'] #简历修改时间
            employment = data['employment'] #期望工作性质 全职
            crawlTime = time.strftime('%Y-%m-%d %H:%M:%S')

            detail_obj = self.get_detail(data['id'],data['k'],data['t'])
            # 自我评价
            commentContent = detail_obj['data']['detail']['CommentContent'].replace(',', '，').replace('\n','') if 'CommentContent' in detail_obj['data']['detail'] else ''

            sql = "insert into userInfo(jobId,name,age,sex,url,imgUrl,jobTitle,jobType,eduLevel,city,desiredSalary,careerStatus,workYears,modifyDate,employment,commentContent,crawlTime) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                      % (jobId,name,age,sex,url,imgUrl,jobTitle,jobType,eduLevel,city,desiredSalary,careerStatus,workYears,modifyDate,employment,commentContent,crawlTime)\
                      + "ON DUPLICATE KEY UPDATE name='%s',age='%s',sex='%s',url='%s',imgUrl='%s',jobTitle='%s',jobType='%s',eduLevel='%s',city='%s',desiredSalary='%s',careerStatus='%s',workYears='%s',modifyDate='%s',employment='%s',commentContent='%s',crawlTime='%s'"%(name,age,sex,url,imgUrl,jobTitle,jobType,eduLevel,city,desiredSalary,careerStatus,workYears,modifyDate,employment,commentContent,crawlTime)
            print(sql)
            self.mysql.save(sql)

            #教育经验
            for edu in detail_obj['data']['detail']['EducationExperience']:
                jobId = data['id']
                eduRowId = edu['SubRowId']
                beginDate = edu['DateStart']
                endDate = edu['DateEnd']
                schoolName = edu['SchoolName']
                major = edu['MajorName']
                sql = "insert into education(jobId,eduRowId,beginDate,endDate,schoolName,major) values ('%s','%s','%s','%s','%s','%s')"\
                      % (jobId,eduRowId,beginDate,endDate,schoolName,major)\
                      + "ON DUPLICATE KEY UPDATE beginDate='%s',endDate='%s',schoolName='%s',major='%s'"%(beginDate,endDate,schoolName,major)
                print(sql)
                self.mysql.save(sql)

            # 工作经验
            for work in detail_obj['data']['detail']['WorkExperience']:
                jobId = data['id']
                workRowId = work['SubRowId']
                dateStart = work['DateStart']
                dateEnd = work['DateEnd']
                jobTitle = work['JobTitle']
                company = work['CompanyName']
                description = work['WorkDescription'].replace('\n','').replace('\r','')
                sql = "insert into work(jobId,workRowId,dateStart,dateEnd,jobTitle,company,description) values ('%s','%s','%s','%s','%s','%s','%s')" \
                      % (jobId,workRowId,dateStart,dateEnd,jobTitle,company,description) \
                      + "ON DUPLICATE KEY UPDATE dateStart='%s',dateEnd='%s',jobTitle='%s',company='%s',description='%s'" % (dateStart, dateEnd, jobTitle, company, description)
                print(sql)
                self.mysql.save(sql)

            #项目经验
            for project in detail_obj['data']['detail']['ProjectExperience']:
                jobId = data['id']
                projectRowId = project['SubRowId']
                dateStart = project['DateStart']
                dateEnd = project['DateEnd']
                projectName = project['DateStart']
                responsibility = project['ProjectResponsibility'].replace('\n','').replace('\r','')
                description = project['ProjectDescription'].replace('\n','').replace('\r','')
                sql = "insert into project(jobId,projectRowId,dateStart,dateEnd,projectName,responsibility,description) values ('%s','%s','%s','%s','%s','%s','%s')" \
                      % (jobId,projectRowId,dateStart,dateEnd,projectName,responsibility,description) \
                      + "ON DUPLICATE KEY UPDATE dateStart='%s',dateEnd='%s',projectName='%s',responsibility='%s',description='%s'" % (dateStart, dateEnd, projectName, responsibility,description)
                print(sql)
                self.mysql.save(sql)



            # write_res = id + ',' + username + ',' + sex + ',' + age + ',' + jobTitle + ',' + jobType + ',' + eduLevel + ',' + city + ',' + desiredSalary + ',' + careerStatus + ',' + workYears + ',' + employment\
            # + ',' + school_beginDate + ',' + school_endDate + ',' + school_schoolName + ',' + school_major + ',' + modifyDate + ',' + CommentContent + work_str + project_str + '\n'
            # print(write_res)
            # self.write(write_res)

    def get_detail(self,id,key,time):
        url = config.DETAIL_URL.format(id=id, key=key, time=time)
        print(url)
        response = self.download.get_html(url)
        json_obj = json.loads(response.text)
        return json_obj


    def write(self,results):
        with open('results.csv', 'a') as f:
            f.write(results)