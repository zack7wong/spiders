#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from job_spider import download
from job_spider import config
# import download
# import config
import json

class Job(object):
    def __init__(self):
        with open('results.csv','w') as f:
            write_res = 'id,用户名,性别,年龄,应聘职位,应聘类型,教育程度,城市,期望薪资,在职状态,工作年限,期望工作性质,入学时间,毕业时间,学校,专业,简历修改时间,自我评价,工作1,工作2,工作3,项目1,项目2,项目3' + '\n'
            f.write(write_res)

        #cityid 上海538 苏州639
        self.start_url = 'https://rd5.zhaopin.com/api/custom/search/resumeListV2?_=1540959006801&x-zp-page-request-id=50d84efd11d84f49b1b88d22d774142d-1540958517096-790847'
        self.download = download.Download()

    def get_url(self):
        item_list = []
        for i in range(1, 67):
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
        project_list = []
        work_list = []
        for data in json_obj['data']['dataList']:
            id = data['id']
            username = data['userName']
            sex = data['gender']
            age = str(data['age'])
            jobTitle = data['jobTitle'] #应聘职位
            jobType = data['jobType']  #应聘类型
            eduLevel = data['eduLevel'] #教育程度
            city = data['city']
            desiredSalary = data['desiredSalary'] #期望薪资
            careerStatus = data['careerStatus'] #离职状态
            workYears = str(data['workYears']) #工作时间
            employment = data['employment'] #期望工作性质 全职
            # lastJob_beginDate = data['lastJobDetail']['beginDate'] if 'beginDate' in data['lastJobDetail'] else ''
            # lastJob_endDate = data['lastJobDetail']['endDate'] if 'endDate' in data['lastJobDetail'] else ''
            # lastJob_companyName = data['lastJobDetail']['companyName'] if 'companyName' in data['lastJobDetail'] else ''
            # lastJob_department = data['lastJobDetail']['department'] if 'department' in data['lastJobDetail'] else ''
            # lastJob_jobName = data['lastJobDetail']['jobName'] if 'jobName' in data['lastJobDetail'] else ''
            # lastJob_description = data['lastJobDetail']['description'] if 'description' in data['lastJobDetail'] else ''
            # lastJob_description = lastJob_description.replace(',','，')
            school_beginDate = data['schoolDetail']['beginDate'] if 'beginDate' in data['schoolDetail'] else ''
            school_endDate = data['schoolDetail']['endDate'] if 'endDate' in data['schoolDetail'] else ''
            school_schoolName = data['schoolDetail']['schoolName'] if 'schoolName' in data['schoolDetail'] else ''
            school_major = data['schoolDetail']['major'] if 'major' in data['schoolDetail'] else ''
            modifyDate = '20' + data['modifyDate']

            detail_obj = self.get_detail(data['id'],data['k'],data['t'])
            # 自我评价
            CommentContent = detail_obj['data']['detail']['CommentContent'].replace(',', '，').replace('\n', '') if 'CommentContent' in detail_obj['data']['detail'] else ''

            # 工作经验
            for work in detail_obj['data']['detail']['WorkExperience']:
                DateStart = work['DateStart']
                DateEnd = work['DateEnd']
                JobTitle = work['JobTitle']
                CompanyName = work['CompanyName']
                WorkDescription = work['WorkDescription']
                obj = {
                    'DateStart': DateStart,
                    'DateEnd': DateEnd,
                    'JobTitle': JobTitle,
                    'CompanyName': CompanyName,
                    'WorkDescription': WorkDescription,
                }
                work_list.append(obj)

            work_str = ''
            for work in work_list:
                temp_str = str(work) + ','
                work_str +=temp_str

            #项目经验
            for project in detail_obj['data']['detail']['ProjectExperience']:
                DateStart = project['DateStart']
                DateEnd = project['DateEnd']
                ProjectName = project['DateStart']
                ProjectResponsibility = project['ProjectResponsibility']
                ProjectDescription = project['ProjectDescription']

                obj = {
                    'DateStart': DateStart,
                    'DateEnd': DateEnd,
                    'ProjectName': ProjectName,
                    'ProjectResponsibility': ProjectResponsibility,
                    'ProjectDescription': ProjectDescription,
                }
                project_list.append(obj)

            project_str = ''
            for project in project_list:
                temp_str = str(project) + ','
                project_str += temp_str

            # lastJobDetail = data['lastJobDetail']
            # schoolDetail = data['schoolDetail']
            # del lastJobDetail['salary']
            # del lastJobDetail['industry']
            # del lastJobDetail['profession']
            # del lastJobDetail['companyType']
            # del schoolDetail['degree']
            write_res = id + ',' + username + ',' + sex + ',' + age + ',' + jobTitle + ',' + jobType + ',' + eduLevel + ',' + city + ',' + desiredSalary + ',' + careerStatus + ',' + workYears + ',' + employment\
            + ',' + school_beginDate + ',' + school_endDate + ',' + school_schoolName + ',' + school_major + ',' + modifyDate + ',' + CommentContent + work_str + project_str + '\n'
            print(write_res)
            self.write(write_res)

    def get_detail(self,id,key,time):
        url = config.DETAIL_URL.format(id=id, key=key, time=time)
        print(url)
        response = self.download.get_html(url)
        json_obj = json.loads(response.text)
        return json_obj


    def write(self,results):
        with open('results.csv', 'a') as f:
            f.write(results)