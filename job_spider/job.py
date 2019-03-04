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
import random

chinese_name_list = ['Wang','Li','Zhang','Liu','Chen','Yang','Huang','Zhao','Wu','Zhou','Liang','Song','Tang','Xu','Han','Feng','Deng','Cao','Peng','Zeng','Xiao','Tian','Dong','Yuan','Pan','Yu','Jiang','Cai','Yu','Du','Ye','Cheng','Su','Wei','Lv','Ding','Ren','Shen','Yao','Lu','Jiang','Cui','Zhong','Tan','Lu','Wang','Fan','Jin','Shi','Liao','Jia','Xia','Wei','Fu','Fang','Bai','Zou','Meng','Xiong','Qin','Qiu']
english_name_list = ['Aaron','Abbott','Abel','Abner','Abraham','Adair','Adam','Addison','Adolph','Adonis','Adrian','Ahern','Alan','Albert','Aldrich','Alexander','Alfred','Alger','Algernon','Allen','Alston','Alva','Alvin','Alvis','Amos','Andre','Andrew','Andy','Angelo','Augus','Ansel','Antony','Antoine','Antonio','Archer','Archibald','Aries','Arlen','Armand','Armstrong','Arno','Arnold','Arthur','Arvin','Asa','Ashbur','Atwood','Aubrey','August','Augustine','Avery','Baird','Baldwin','Bancroft','Bard','Barlow','Barnett','Baron','Barret','Barry','Bartholomew','Bart','Barton','Bartley','Basil','Beacher','Beau','Beck','Ben','Benedict','Benjamin','Bennett','Benson','Berg','Berger','Bernard','Bernie','Bert','Berton','Bertram','Bevis','Bill','Bing','Bishop','Blair','Blake','Blithe','Bob','Booth','Borg','Boris','Bowen','Boyce','Boyd','Bradley','Brady','Brandon','Brian','Broderick','Brook','Bruce','Bruno','Buck','Burgess','Burke','Burnell','Burton','Byron','Caesar','Calvin','Carey','Carl','Carr','Carter','Cash','Cecil','Cedric','Chad','Channing','Chapman','Charles','Chasel','Chester','Christ','Christian','Christopher','Clare','Clarence','Clark','Claude','Clement','Cleveland','Cliff','Clifford','Clyde','Colbert','Colby','Colin','Conrad','Corey','Cornelius','Cornell','Craig','Curitis','Cyril','Dana','Daniel','Darcy','Darnell','Darren','Dave','David','Dean','Dempsey','Dennis','Derrick','Devin','Dick','Dominic','Don','Donahue','Donald','Douglas','Drew','Duke','Duncan','Dunn','Dwight','Dylan','Earl','Ed','Eden','Edgar','Edmund','Edison','Edward','Edwiin','Egbert','Eli','Elijah','Elliot','Ellis','Elmer','Elroy','Elton','Elvis','Emmanuel','Enoch','Eric','Ernest','Eugene','Evan','Everley','Fabian','Felix','Ferdinand','Fitch','Fitzgerald','Ford','Francis','Frank','Franklin','Frederic','Gabriel','Gale','Gary','Gavin','Gene','Geoffrey','Geoff','George','Gerald','Gilbert','Giles','Glenn','Goddard','Godfery','Gordon','Greg','Gregary','Griffith','Grover','Gustave','Guy','Hale','Haley','Hamiltion','Hardy','Harlan','Harley','Harold','Harriet','Harry','Harvey','Hayden','Heather','Henry','Herbert','Herman','Hilary','Hiram','Hobart','Hogan','Horace','Howar','Hubery','Hugh','Hugo','Humphrey','Hunter','Hyman','Ian','Ingemar','Ingram','Ira','Isaac','Isidore','Ivan','Ives','Jack','Jacob','James','Jared','Jason','Jay','Jeff','Jeffrey','Jeremy','Jerome','Jerry','Jesse','Jim','Jo','John','Jonas','Jonathan','Joseph','Joshua','Joyce','Julian','Julius','Justin','Keith','Kelly','Ken','Kennedy','Kenneth','Kent','Kerr','Kerwin','Kevin','Kim','King','Kirk','Kyle','Lambert','Lance','Larry','Lawrence','Leif','Len','Lennon','Leo','Leonard','Leopold','Les','Lester','Levi','Lewis','Lionel','Lou','Louis','Lucien','Luther','Lyle','Lyndon','Lynn','Magee','Malcolm','Mandel','Marcus','Marico','Mark','Marlon','Marsh','Marshall','Martin','Marvin','Matt','Matthew','Maurice','Max','Maximilian','Maxwell','Meredith','Merle','Merlin','Michael','Michell','Mick','Mike','Miles','Milo','Monroe','Montague','Moore','Morgan','Mortimer','Morton','Moses','Murphy','Murray','Myron','Nat','Nathan','Nathaniel','Neil','Nelson','Newman','Nicholas','Nick','Nigel','Noah','Noel','Norman','Norton','Ogden','Oliver','Omar','Orville','Osborn','Oscar','Osmond','Oswald','Otis','Otto','Owen','Page','Parker','Paddy','Patrick','Paul','Payne','Perry','Pete','Peter','Phil','Philip','Porter','Prescott','Primo','Quentin','Quennel','Quincy','Quinn','Quintion','Rachel','Ralap','Randolph','Raymond','Reg','Regan','Reginald','Reuben','Rex','Richard','Robert','Robin','Rock','Rod','Roderick','Rodney','Ron','Ronald','Rory','Roy','Rudolf','Rupert','Ryan','Sam','Sampson','Samuel','Sandy','Saxon','Scott','Sean','Sebastian','Sid','Sidney','Silvester','Simon','Solomon','Spencer','Stan','Stanford','Stanley','Steven','Stev','Steward','Tab','Taylor','Ted','Ternence','Theobald','Theodore','Thomas','Tiffany','Tim','Timothy','Tobias','Toby','Todd','Tom','Tony','Tracy','Troy','Truman','Tyler','Tyrone','Ulysses','Upton','Uriah','Valentine','Valentine','Verne','Vic','Victor','Vincent','Virgil','Vito','Vivian','Wade','Walker','Walter','Ward','Warner','Wayne','Webb','Webster','Wendell','Werner','Wilbur','Will','William','Willie','Winfred','Winston','Woodrow','Wordsworth','Wright','Wythe','Xavier','Yale','Yehudi','York','Yves','Zachary','Zebulon','Ziv']
zimu_list = [chr(i) for i in range(97,123)]

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
        for i in range(8, 100):
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
            print('暂停15秒')
            time.sleep(15)
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
            try:
                desiredSalary = data['desiredSalary']
                desiredSalary = desiredSalary.replace('元','').replace('/','').replace('月','').strip()
                if '-' in desiredSalary:
                    minSalary = desiredSalary.split('-')[0] #期望薪资 最小
                    maxSalary = desiredSalary.split('-')[1] #期望薪资 最大
                elif '面议' in desiredSalary:
                    minSalary = desiredSalary
                    maxSalary = ''
                else:
                    minSalary = desiredSalary
                    maxSalary = desiredSalary
            except:
                maxSalary = ''
                minSalary = ''

            careerStatus = data['careerStatus'] #离职状态
            workYears = int(data['workYears']) if data['workYears'] != '' else 0
            modifyDate = '20' + data['modifyDate'] #简历修改时间
            employment = data['employment'] #期望工作性质 全职
            crawlTime = time.strftime('%Y-%m-%d %H:%M:%S')

            detail_obj = self.get_detail(data['id'],data['k'],data['t'])
            # 自我评价
            commentContent = detail_obj['data']['detail']['CommentContent'].replace(',', '，').replace('\n','') if 'CommentContent' in detail_obj['data']['detail'] else ''

            #后面增加的字段
            telephone = ''
            hName = random.choice(english_name_list)+' '+ random.choice(chinese_name_list)
            hId = random.choice(zimu_list)+str(random.randint(1000,9999))
            u_id = 4  #后面再真正随机
            j_type = 1
            evaluate = '' #猎头评价
            status = 1
            surface = random.randint(99,199)
            duty = random.randint(199,599)
            duty_one = random.randint(699,1299)
            duty_three = random.randint(1499,2499)
            modify_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            is_es = 1
            source = 1

            # sql = "insert into userInfo(jobId,name,age,sex,url,imgUrl,jobTitle,jobType,eduLevel,city,desiredSalary,careerStatus,workYears,modifyDate,employment,commentContent,crawlTime) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
            #           % (jobId,name,age,sex,url,imgUrl,jobTitle,jobType,eduLevel,city,desiredSalary,careerStatus,workYears,modifyDate,employment,commentContent,crawlTime)\
            #           + "ON DUPLICATE KEY UPDATE name='%s',age='%s',sex='%s',url='%s',imgUrl='%s',jobTitle='%s',jobType='%s',eduLevel='%s',city='%s',desiredSalary='%s',careerStatus='%s',workYears='%s',modifyDate='%s',employment='%s',commentContent='%s',crawlTime='%s'"%(name,age,sex,url,imgUrl,jobTitle,jobType,eduLevel,city,desiredSalary,careerStatus,workYears,modifyDate,employment,commentContent,crawlTime)

            sql = "insert into userInfo(jobId,name,age,sex,telephone,hName,hId,url,imgUrl,jobTitle,jobType,eduLevel,city,minSalary,maxSalary,careerStatus,workYears,modifyDate,employment,commentContent,crawlTime,u_id,j_type,evaluate,status,surface,duty,duty_one,duty_three,modify_time,is_es,source) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"% (jobId,name,age,sex,telephone,hName,hId,url,imgUrl,jobTitle,jobType,eduLevel,city,minSalary,maxSalary,careerStatus,workYears,modifyDate,employment,commentContent,crawlTime,u_id,j_type,evaluate,status,surface,duty,duty_one,duty_three,modify_time,is_es,source)+"ON DUPLICATE KEY UPDATE name='%s',age='%s',sex='%s',url='%s',imgUrl='%s',jobTitle='%s',jobType='%s',eduLevel='%s',city='%s',careerStatus='%s',workYears='%s',modifyDate='%s',employment='%s',commentContent='%s',crawlTime='%s'"%(name,age,sex,url,imgUrl,jobTitle,jobType,eduLevel,city,careerStatus,workYears,modifyDate,employment,commentContent,crawlTime)
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