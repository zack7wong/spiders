# coding=utf8
import copy
import re


class LNode(object):
    #结点初始化函数, p 即模拟所存放的下一个结点的地址
    #为了方便传参, 设置 p 的默认值为 0
    def __init__(self, data, p=0):
        self.data = data
        self.next = p

class Sexagenary(object):

    def __init__(self, input_str):
        '''
        干支序列数字初始化，接受一个纯汉字字符输入，输入格式为干支序列，如“癸丑丁巳”，左边的位大，右边小
        :param input_str: 输入的干支序列字符串，如“癸丑丁巳”
        :return: None
        '''
        self.init_sexagenary_dict()
        self.head = None
        # print(self.sexagenary2int)
        # print(self.int2sexagenary )
        # 判断干支数字是否为以0开头的非零数字，是的话可以返回错误
        # 初始化干支数字链表，过程中判断插入的字符是否在60个干支数字中
        # 打印结果
        if input_str[0] == '0':
            print('ValuError: 初始化错误 ' + input_str)
            return None

        #input_str切割最多4个数字
        # print('正在初始化链表')
        # print('输入值为：'+input_str)
        data = []
        for i in range(0,len(input_str),2):
            if input_str[i:i+2] in self.sexagenary2int.keys():
                pass
                # print(input_str[i:i+2]+'在60个干支数字中，对应的数字是：'+str(self.sexagenary2int[input_str[i:i+2]]))
            else:
                print('ValuError: 初始化错误 '+input_str)
                # print(input_str[i:i+2] + '不在60个干支数字中')
                return None
            #
            # if input_str[i+2:i+4] !='':
            #     if input_str[i+2:i+4] in self.sexagenary2int.keys():
            #         print(input_str[i + 2:i + 4] + '在60个干支数字中，对应的数字是：' + str(self.sexagenary2int[input_str[i + 2:i + 4]]))
            #     else:
            #         print(input_str[i + 2:i + 4] + '不在60个干支数字中')
            #         return False

            data.append(input_str[i:i+2])
        # print(data)
        # 初始化链表与数据
        # data = [1, 2, 3, 4, 5]
        self.initList(data)
        # self.get_sexagenary_string()

    #链表初始化函数, 方法类似于尾插
    def initList(self, data):
        #创建头结点
        self.head = LNode(data[0])
        p = self.head
        #逐个为 data 内的数据创建结点, 建立链表
        for i in data[1:]:
            node = LNode(i)
            p.next = node
            p = p.next

    #链表判空
    def isEmpty(self):
        if self.head.next == 0:
            return 1
        else:
            return 0

    def get_length(self):
        '''
        :return: 返回干支序列大数字的长度
        '''
        # if self.isEmpty():
        #     exit(0)

        p = self.head
        len = 0
        while p:
            len += 1
            p = p.next
        return len

    def insert(self, index, input_str):
        '''
        插入一个纯汉字字符输入，输入格式为干支序列，如“癸丑丁巳”，位置为int
        :param index: 要插入的位置，左边第一个位置为0，可以为负值
        :param input_str: 要插入的干支序列
        :return: 插入后的干支序列串，若插入错误返回False，如果插入失败数字回滚为删除之前的数字
        example: 原串 "癸丑丁巳" self.insert(0,"庚子")后变为"庚子癸丑丁巳"
        example: 原串 "癸丑丁巳" self.insert(-1,"甲子")后变为"癸丑甲子丁巳"
        '''
        # 判断index是否合法，input_str是否不为空
        # 判断结果是否合法，是否在开头插入0
        # 判断插入的字符是否为合法数字，在适当位置插入字符串
        if input_str[0:2] == '甲子' and index == 0:
            print('ValuError: 插入错误 ' + input_str)
            return

        for i in range(0, len(input_str), 2):
            if input_str[i:i + 2] not in self.sexagenary2int.keys():
                print('ValuError: 插入错误 ' + input_str)
                return

        myinput_str = input_str
        myflag = index
        for i in range(0, len(myinput_str), 2):
            input_str = myinput_str[i:i + 2]
            if index == 0:
                data = self.get_sexagenary_string()
                input_str = input_str+data

                data = []
                for i in range(0, len(input_str), 2):
                    data.append(input_str[i:i + 2])

                self.initList(data)
                return

            if index<0:
                index = self.get_length() - abs(index)

            index = index -1
            if self.isEmpty():
                return
            if index > self.get_length() - 1 or index <= -2:
                # print("超出链表长度")
                print('ValuError: 插入错误 ' + input_str)
                return
            p = self.head
            i = 0
            while i <= index:
                pre = p
                p = p.next
                i += 1

            # 遍历找到索引值为 index 的结点后, 在其后面插入结点
            node = LNode(input_str)
            pre.next = node
            node.next = p
            if myflag < 0:
                index = myflag
            else:
                index+=2

    def remove(self, index, rm_len):
        '''
        删除大数字串中起始位置为int，长度为rm_len的子串
        :param index: 删除的位置，可以为负值
        :param rm_len: 删除的长度 备注：删除长度必须为非负值，否则报错
        :return: 删除后的干支序列串，如删除失败返回False, 如果删除失败数字回滚为删除之前的数字
        example: "庚子癸丑丁巳" ，self.remove(0,0) 后变为 "庚子癸丑丁巳"
        example: "庚子癸丑丁巳" ，self.remove(0,2) 后变为 "丁巳"
        example: "庚子癸丑丁巳" ，self.remove(2,2) 后变为 "庚子癸丑" 删除长度过长就删完为止
        example: "庚子癸丑丁巳" ，self.remove(-1,1) 后变为 "庚子癸丑"
        example: "庚子癸丑丁巳" ，self.remove(-1,2) 后变为 "庚子癸丑" 删除长度过长就删完为止
        example: "庚子癸丑丁巳" ，self.remove(-10,1) 删除位置错误
        example: "庚子癸丑丁巳" ，self.remove(10,1) 删除位置错误
        '''
        # 判断index和rm_len合法性
        # 删除对应节点
        # 如果有需要合并端点
        try:
            int(index)
        except:
            print('ValuError: 删除错误 ' + str(index))
            return

        myindex = index

        if index < 0:
            myindex = self.get_length() - abs(index)

        if myindex > self.get_length() - 1:
            # print("删除时超出链表长度")
            print('ValuError: 删除错误 ' + str(index))
            return
        for index in range(myindex,myindex+rm_len):
            if self.isEmpty():
                print('ValuError: 删除错误 ' + str(index))
                return

            if index == 0:
                data = self.get_sexagenary_string()
                input_str = data[2:]

                if data[rm_len*2:rm_len*2+2] == '甲子':
                    print('ValuError: 删除错误 ' + str(index))
                    return

                data = []
                for i in range(0, len(input_str), 2):
                    data.append(input_str[i:i + 2])

                self.initList(data)
                return

            if index<0 or index>self.get_length()-1:
                print('ValuError: 删除错误 ' + str(index))
                return

            i = 0
            p = self.head
            index = myindex
            #遍历找到索引值为 index 的结点
            while p.next:
                pre = p
                p = p.next
                i += 1
                # print(index)
                # print(p.data)
                if i==index:
                    pre.next = p.next
                    p = None

                    break

            #p的下一个结点为空说明到了最后一个结点, 删除之即可
            #pre.next = None


    def toDecimal(self):
        '''
        将当前字符串转换为一个十进制字符串输出，如 "乙丑丙寅"，转为"62"
        :return: 转换后的十进制字符串python string
        '''
        item_Str = 0
        p = self.head
        num_len = self.get_length()-1
        while p:
            res = self.sexagenary2int[p.data] * pow(60,num_len)
            num_len -=1
            item_Str += res
            p = p.next
        return str(item_Str)

    def Decimalint_to_sexagenary(self, num):
        '''
        把一个十进制数字转换为干支序列数字
        :param num: 输入的十进制数字，int型
        :return: 干支序列字符串
        '''
        num = int(num)
        x = 60
        a = ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳',
             '壬午', '癸未', '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥',
             '庚子', '辛丑', '壬寅', '癸卯', '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑', '甲寅', '乙卯', '丙辰', '丁巳',
             '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥']
        # a=[0,1,2,3,4,5,6,7,8,9]
        b = []
        while True:
            s = num // x  # 商
            y = num % x  # 余数
            b = b + [y]
            if s == 0:
                break
            num = s
        b.reverse()
        myres = ''
        for i in b:
            myres += a[i]
        return myres


    def get_sexagenary_string(self):
        '''
        返回当前的干支序列字符串，如返回"甲子癸丑丁巳"
        :return: string 返回的感知序列字符串
        '''

        # 遍历链表
        # if self.isEmpty():
        #     exit(0)
        # print('正在遍历链表')
        item_Str = ''
        p = self.head
        while p:
            # print(p.data, )
            item_Str +=p.data
            p = p.next
        # print(item_Str)
        return item_Str

    def print_sexagenary_string(self):
        '''
        打印当前的干支序列，如输出"甲子癸丑丁巳"
        '''
        item_Str = ''
        p = self.head
        while p:
            # print(p.data, )
            item_Str += p.data
            p = p.next
        # print(item_Str)
        return item_Str

    def toChinese(self, traditional=True):
        '''
        对一个等价10进制数值小于一万亿的干支数字，输出其十进制票据格式，如 "乙丑丙寅" 转为"陆拾贰"
        壹、贰、叁、肆、伍、陆、柒、捌、玖、拾、佰、仟、万、亿、零、整
        :return: 转换后的票据格式的字符串
        '''

        item_Str = 0
        p = self.head
        num_len = self.get_length() - 1
        while p:
            res = self.sexagenary2int[p.data] * pow(60, num_len)
            num_len -= 1
            item_Str += res
            p = p.next

        number = int(item_Str)
        chinese_num = {
            'Simplified': ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九'],
            'Traditional': ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
        }
        chinese_unit = {
            'Simplified': ['个', '十', '百', '千'],
            'Traditional': ['个', '拾', '佰', '仟']
        }
        extra_unit = ['', '万', '亿']

        if traditional:
            chinese_num = chinese_num['Traditional']
            chinese_unit = chinese_unit['Traditional']
        else:
            chinese_num = chinese_num['Simplified']
            chinese_unit = chinese_unit['Simplified']

        num_cn = []

        # 数字转换成字符列表
        num_list = list(str(number))

        # 反转列表，个位在前
        num_list.reverse()

        # 数字替换成汉字
        for num in num_list:
            num_list[num_list.index(num)] = chinese_num[int(num)]

        # 每四位进行拆分，第二个四位加“万”，第三个四位加“亿”
        for loop in range(int(len(num_list) / 4 + 1)):
            sub_num = num_list[(loop * 4):((loop + 1) * 4)]
            if not sub_num:
                continue

            # 是否增加额外单位“万”、“亿”
            if loop > 0 and 4 == len(sub_num) and chinese_num[0] == sub_num[0] == sub_num[1] == sub_num[2] == sub_num[
                3]:
                use_unit = False
            else:
                use_unit = True

            # 合并数字和单位，单位在每个数字之后
            # from itertools import chain
            # sub_num = list(chain.from_iterable(zip(chinese_unit, sub_num)))
            sub_num = [j for i in zip(chinese_unit, sub_num) for j in i]

            # 删除第一个单位 '个'
            del sub_num[0]

            # “万”、“亿”中如果第一位为0则需加“零”: 101000，十万零一千
            use_zero = True if loop > 0 and chinese_num[0] == sub_num[0] else False

            if len(sub_num) >= 7 and chinese_num[0] == sub_num[6]:
                del sub_num[5]  # 零千 -> 零
            if len(sub_num) >= 5 and chinese_num[0] == sub_num[4]:
                del sub_num[3]  # 零百 -> 零
            if len(sub_num) >= 3 and chinese_num[0] == sub_num[2]:
                del sub_num[1]  # 零十 -> 零
            if len(sub_num) == 3 and chinese_num[1] == sub_num[2]:
                del sub_num[2]  # 一十开头的数 -> 十

            # 删除末位的零
            while len(num_list) > 1 and len(sub_num) and chinese_num[0] == sub_num[0]:
                del sub_num[0]

            # 增加额外的“零”
            if use_zero and len(sub_num) > 0:
                num_cn.append(chinese_num[0])

            # 增加额外单位“万”、“亿”
            if use_unit:
                num_cn.append(extra_unit[loop])

            num_cn += sub_num

        # 删除连续重复数据：零，只有零会重复
        num_cn = [j for i, j in enumerate(num_cn) if i == 0 or j != num_cn[i - 1]]
        # 删除末位的零，最后一位为 extra_unit 的 ''
        if len(num_list) > 1 and len(num_cn) > 1 and chinese_num[0] == num_cn[1]:
            del num_cn[1]

        # 反转并连接成字符串
        num_cn.reverse()
        num_cn = ''.join(num_cn)
        return num_cn

        # item_Str = 0
        # p = self.head
        # num_len = self.get_length() - 1
        # while p:
        #     res = self.sexagenary2int[p.data] * pow(60, num_len)
        #     num_len -= 1
        #     item_Str += res
        #     p = p.next
        #
        # num_dict = {'1': '壹', '2': '贰', '3': '叁', '4': '肆', '5': '伍', '6': '陆', '7': '柒', '8': '捌', '9': '玖','0': '零', }
        # index_dict = {1: '', 2: '拾', 3: '佰', 4: '仟', 5: '万', 6: '拾', 7: '佰', 8: '仟', 9: '亿'}
        # nums = list(str(item_Str))
        # nums_index = [x for x in range(1, len(nums) + 1)][-1::-1]
        #
        # mystr = ''
        # for index, item in enumerate(nums):
        #     mystr = "".join((mystr, num_dict[item], index_dict[nums_index[index]]))
        #
        # # str = re.sub("零[十百千零]*", "零", str)
        # # str = re.sub("零万", "万", str)
        # # str = re.sub("亿万", "亿零", str)
        # # str = re.sub("零零", "零", str)
        # # str = re.sub("零\\b", "", str)
        # if mystr[:2] == '壹拾':
        #     return mystr[1:]
        # if mystr[-7:] == '零仟零佰零拾零':
        #     return mystr[:-7]
        # if mystr[-5:] == '零佰零拾零':
        #     return mystr[:-5]
        # if mystr[-3:] == '零拾零':
        #     return mystr[:-3]
        # return mystr

    def tick(self):
        '''
        干支序列中往前走一个，如果走之前是癸亥，走后则回到甲子，并且往后进位 （相当于+1）
        :return: 返回加一后的干支序列字符串
        '''


    def yearToSgnr(self, year):
        '''
        随意输入一个公历年，输出其干支纪年 （60中的一种） 如2018年，就是"戊戌"
        :param year: 输入公历年  int型
        :return: 输出干支纪年的字符串
        '''
        res = year%60 - 4
        if res < 0:
            res = 60 - abs(res)
        return self.int2sexagenary[res]

    def add(self, other):
        '''
        加上另一个Sexagenary数
        :param other: other 也是一个Class Sexagenary的对象
        :return: 加完之后的干支数字，返回一个Class Sexagenary的对象
        '''
        otherNum = other.toDecimal()
        myNum = self.toDecimal()
        # 3659 + 119 = 3778
        myres = self.Decimalint_to_sexagenary(int(otherNum)+int(myNum))

        return Sexagenary(myres)


    def minus(self, other):
        '''
        减去另一个Sexagenary数
        :param other: other 也是一个Class Sexagenary的对象
        :return: 减完之后的干支数字，返回一个Class Sexagenary的对象
        '''
        otherNum = other.toDecimal()
        myNum = self.toDecimal()


        # 3659 + 119 = 3778
        myres = self.Decimalint_to_sexagenary(abs(int(otherNum) - int(myNum)))
        return Sexagenary(myres)

    def multiply(self, other):
        '''
        乘上另一个Sexagenary数
        :param other: other 也是一个Class Sexagenary的对象
        :return: 乘完之后的干支数字，返回一个Class Sexagenary的对象
        '''
        otherNum = other.toDecimal()
        myNum = self.toDecimal()
        myres = self.Decimalint_to_sexagenary(int(otherNum) * int(myNum))

        return Sexagenary(myres)

    def init_sexagenary_dict(self):
        A = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        B = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        sexagenary2int = {}
        int2sexagenary = {}
        i = 0
        j = 0
        for count in range(60):
            sexagenary_str = A[i] + B[j]
            sexagenary2int[sexagenary_str] = count
            int2sexagenary[count] = sexagenary_str
            i = (i + 1) % 10
            j = (j + 1) % 12
        self.sexagenary2int = sexagenary2int
        self.int2sexagenary = int2sexagenary


def mytest():
    test1 = ["戊戌甲子乙丑丙寅", "甲子乙丑丙寅乙子", "甲子", "庚午", "庚", "甲乙", "丙寅庚", "甲子甲子甲子乙丑", "己寅",
             "乙寅"]  # test function __init__初始化，设置bug: 没有对应的干支串
    for test_case in test1:
       test_obj = Sexagenary(test_case)

    # test2 测试插入删除操作
    test2 = Sexagenary("戊戌甲子乙丑丙寅")
    if test2.get_sexagenary_string() != "戊戌甲子乙丑丙寅":
        print("Error")
    test2.insert(1, "甲寅")
    if test2.get_sexagenary_string() != "戊戌甲寅甲子乙丑丙寅":
        print("Error")
    test2.insert(5, "己巳")
    if test2.get_sexagenary_string() != "戊戌甲寅甲子乙丑丙寅己巳":
        print("Error")
    test2.insert(-1, "癸巳")
    if test2.get_sexagenary_string() != "戊戌甲寅甲子乙丑丙寅癸巳己巳":
        print("Error")
    test2.insert(-3, "丙戌乙未戊子")
    if test2.get_sexagenary_string() != "戊戌甲寅甲子乙丑丙戌乙未戊子丙寅癸巳己巳":
        print("Error")
    test2.insert(0, "乙丑")
    if test2.get_sexagenary_string() != "乙丑戊戌甲寅甲子乙丑丙戌乙未戊子丙寅癸巳己巳":
        print("Error")
    test2.insert(0, "甲子甲子乙丑")
    if test2.get_sexagenary_string() != "乙丑戊戌甲寅甲子乙丑丙戌乙未戊子丙寅癸巳己巳":
        print("Error")
    test2.insert(1, "丁卯戊辰庚寅")
    if test2.get_sexagenary_string() != "乙丑丁卯戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未戊子丙寅癸巳己巳":
        print("Error")
    test2.insert(100, "癸酉")
    if test2.get_sexagenary_string() != "乙丑丁卯戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未戊子丙寅癸巳己巳":
        print("Error")
    test2.insert(2, "辛寅")
    if test2.get_sexagenary_string() != "乙丑丁卯戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未戊子丙寅癸巳己巳":
        print("Error")
    test2.insert(-100, "癸未")
    if test2.get_sexagenary_string() != "乙丑丁卯戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未戊子丙寅癸巳己巳":
        print("Error")
    test2.remove(0, 1)
    if test2.get_sexagenary_string() != "丁卯戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未戊子丙寅癸巳己巳":
        print("Error")
    test2.remove(14, 2)
    if test2.get_sexagenary_string() != "丁卯戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未戊子丙寅癸巳己巳":
        print("Error")
    test2.remove(12, 10)
    if test2.get_sexagenary_string() != "丁卯戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未戊子丙寅癸巳":
        print("Error")
    test2.remove(-3, 1)
    if test2.get_sexagenary_string() != "丁卯戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅癸巳":
        print("Error")
    test2.remove(-1, 10)
    if test2.get_sexagenary_string() != "丁卯戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.insert(1, "甲子")
    if test2.get_sexagenary_string() != "丁卯甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.remove(0, 1)

    if test2.get_sexagenary_string() != "丁卯甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.insert(1, "己未丁亥甲辰癸亥己丑壬子戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰丙申己卯戊申壬辰丁丑甲申庚午辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子")

    if test2.get_sexagenary_string() != "丁卯己未丁亥甲辰癸亥己丑壬子戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰丙申己卯戊申壬辰丁丑甲申庚午辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.insert(21, "甲戌庚午辛酉丁亥丙子辛巳丁巳己巳庚子戊子")
    if test2.get_sexagenary_string() != "丁卯己未丁亥甲辰癸亥己丑壬子戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰丙申己卯戊申壬辰丁丑甲申甲戌庚午辛酉丁亥丙子辛巳丁巳己巳庚子戊子庚午辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.insert(32, "戊午辛未甲戌壬寅丙午壬辰丁巳乙亥戊辰癸酉")
    if test2.get_sexagenary_string() != "丁卯己未丁亥甲辰癸亥己丑壬子戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰丙申己卯戊申壬辰丁丑甲申甲戌庚午辛酉丁亥丙子辛巳丁巳己巳庚子戊子庚午戊午辛未甲戌壬寅丙午壬辰丁巳乙亥戊辰癸酉辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.insert(5, "戊午辛未")
    if test2.get_sexagenary_string() != "丁卯己未丁亥甲辰癸亥戊午辛未己丑壬子戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰丙申己卯戊申壬辰丁丑甲申甲戌庚午辛酉丁亥丙子辛巳丁巳己巳庚子戊子庚午戊午辛未甲戌壬寅丙午壬辰丁巳乙亥戊辰癸酉辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.insert(7, "甲戌壬寅")
    if test2.get_sexagenary_string() != "丁卯己未丁亥甲辰癸亥戊午辛未甲戌壬寅己丑壬子戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰丙申己卯戊申壬辰丁丑甲申甲戌庚午辛酉丁亥丙子辛巳丁巳己巳庚子戊子庚午戊午辛未甲戌壬寅丙午壬辰丁巳乙亥戊辰癸酉辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.insert(6, "丁卯己未丁亥甲辰癸亥戊午")

    if test2.get_sexagenary_string() != "丁卯己未丁亥甲辰癸亥戊午丁卯己未丁亥甲辰癸亥戊午辛未甲戌壬寅己丑壬子戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰丙申己卯戊申壬辰丁丑甲申甲戌庚午辛酉丁亥丙子辛巳丁巳己巳庚子戊子庚午戊午辛未甲戌壬寅丙午壬辰丁巳乙亥戊辰癸酉辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")

    test2.remove(5, 10)

    if test2.get_sexagenary_string() != "丁卯己未丁亥甲辰癸亥己丑壬子戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰丙申己卯戊申壬辰丁丑甲申甲戌庚午辛酉丁亥丙子辛巳丁巳己巳庚子戊子庚午戊午辛未甲戌壬寅丙午壬辰丁巳乙亥戊辰癸酉辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.remove(3, 4)

    if test2.get_sexagenary_string() != "丁卯己未丁亥戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰丙申己卯戊申壬辰丁丑甲申甲戌庚午辛酉丁亥丙子辛巳丁巳己巳庚子戊子庚午戊午辛未甲戌壬寅丙午壬辰丁巳乙亥戊辰癸酉辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.remove(11, 6)
    if test2.get_sexagenary_string() != "丁卯己未丁亥戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰甲戌庚午辛酉丁亥丙子辛巳丁巳己巳庚子戊子庚午戊午辛未甲戌壬寅丙午壬辰丁巳乙亥戊辰癸酉辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.remove(14, 2)
    if test2.get_sexagenary_string() != "丁卯己未丁亥戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰甲戌庚午辛酉辛巳丁巳己巳庚子戊子庚午戊午辛未甲戌壬寅丙午壬辰丁巳乙亥戊辰癸酉辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子甲子戊辰庚寅戊戌甲寅甲子乙丑丙戌乙未丙寅":
        print("Error")
    test2.remove(-5, 3)
    if test2.get_sexagenary_string() != "丁卯己未丁亥戊戌乙酉癸卯丙寅庚子甲戌辛酉丙辰甲戌庚午辛酉辛巳丁巳己巳庚子戊子庚午戊午辛未甲戌壬寅丙午壬辰丁巳乙亥戊辰癸酉辛酉甲申戊寅戊申壬午丙申丙戌庚寅庚子甲子戊辰庚寅戊戌甲寅乙未丙寅":
        print("Error")





    #加法操作检查

    test3 = Sexagenary("乙丑甲子癸亥")
    test4 = Sexagenary("乙丑癸亥")
    test5 = test4.add(test3)
    if test5.get_sexagenary_string() != "乙丑丙寅壬戌":
        print("Error")
    test3 = Sexagenary("乙丑癸亥癸亥")
    test4 = Sexagenary("壬戌癸亥")
    test5 = test4.add(test3)
    if test5.get_sexagenary_string() != "丙寅壬戌壬戌":
        print("Error")
    test3 = Sexagenary("癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥")
    test4 = Sexagenary("癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥")
    test5 = test4.add(test3)
    if test5.get_sexagenary_string() != "乙丑甲子甲子癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥壬戌":
        print("Error")
    '''
    '''
    #减法操作检查
    test3 = Sexagenary("乙丑甲子癸亥")
    test4 = Sexagenary("乙丑癸亥")
    test5 = test3.minus(test4)
    if test5.get_sexagenary_string() != "癸亥甲子":
        print("Error")
    test3 = Sexagenary("乙丑癸亥")
    test4 = Sexagenary("乙丑癸亥")
    test5 = test3.minus(test4)
    if test5.get_sexagenary_string() != "甲子":
        print("Error")
    test3 = Sexagenary("丙寅壬戌壬戌")
    test4 = Sexagenary("壬戌癸亥")
    test5 = test3.minus(test4)
    if test5.get_sexagenary_string() != "乙丑癸亥癸亥":
        print("Error")
    test3 = Sexagenary("辛酉庚申乙丑癸亥")
    test4 = Sexagenary("壬午己卯甲子戊申")
    test5 = test3.minus(test4)
    if test5.get_sexagenary_string() != "癸卯乙巳乙丑己卯":
        print("Error")
    test3 = Sexagenary("乙丑甲子甲子癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥壬戌")
    test4 = Sexagenary("癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥")
    test5 = test3.minus(test4)
    if test5.get_sexagenary_string() != "癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥":
        print("Error")
    test3 = Sexagenary("辛巳")
    test4 = Sexagenary("庚申")
    test5 = test3.minus(test4)
    test3 = Sexagenary("辛巳")
    test4 = Sexagenary("乙丑庚申")
    test5 = test3.minus(test4)
    test3 = Sexagenary("辛巳")
    test4 = Sexagenary("庚丑")
    test5 = test3.minus(test4)
    '''
    '''
    #乘法操作检查
    test3 = Sexagenary("乙丑甲子癸亥")
    test4 = Sexagenary("乙丑癸亥")
    test5 = test4.multiply(test3)
    if test5.get_sexagenary_string() != "丙寅甲子辛酉乙丑":
        print("Error")
    test3 = Sexagenary("乙丑癸亥癸亥")
    test4 = Sexagenary("壬戌癸亥")
    test5 = test4.multiply(test3)

    if test5.get_sexagenary_string() != "乙丑辛酉辛酉乙丑乙丑":
        print("Error")
    test3 = Sexagenary("癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥")
    test4 = Sexagenary("癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥")
    test5 = test4.multiply(test3)
    if test5.get_sexagenary_string() != "癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥壬戌癸亥癸亥甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子乙丑":
        print("Error")
    '''
    '''
    #测试toDecimal函数和toChinese函数以及yearToSgnr函数
    test6 = Sexagenary("乙丑丙寅")
    if test6.toDecimal() != "62":
        print("Error")
    if test6.toChinese() != "陆拾贰":
        print("Error")
    test6 = Sexagenary("壬寅癸未庚申戊辰")
    if test6.toDecimal() != "8279764":
        print("Error")
    if test6.toChinese() != "捌佰贰拾柒万玖仟柒佰陆拾肆":
        print("Error")
    test6 = Sexagenary("己巳壬午辛丑")
    if test6.toDecimal() != "19117":
        print("Error")
    if test6.toChinese() != "壹万玖仟壹佰壹拾柒":
        print("Error")
    test6 = Sexagenary("甲子")

    if test6.toDecimal() != "0":
        print("Error")
    if test6.toChinese() != "零":
        print("Error")
    test6 = Sexagenary("丙子")

    if test6.toDecimal() != "12":
        print("Error")
    if test6.toChinese() != "拾贰":
        print("Error")
    test6 = Sexagenary("乙丑丁卯丁巳甲申")
    if test6.toDecimal() != "230000":
        print("Error")

    if test6.toChinese() != "贰拾叁万":
        print("Error")

    test6 = Sexagenary("辛亥乙酉丁未甲申")
    if test6.toDecimal() != "10230200":
        print("Error")
    if test6.toChinese() != "壹仟零贰拾叁万零贰佰":
        print("Error")
    test6 = Sexagenary("庚午丙午丙辰丁丑丁酉")
    if test6.toDecimal() != "87020013":
        print("Error")

    if test6.toChinese() != "捌仟柒佰零贰万零壹拾叁":
        print("Error")
    test6 = Sexagenary("戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅")
    if test6.toDecimal() != "528657976112464059180067355005830508474576271186440677966101694915254":
        print("Error")
    if test6.yearToSgnr(1022) != "壬戌":
        print("Erroe")
    if test6.yearToSgnr(2018) != "戊戌":
        print("Erroe")



    #加法操作检查
    test3 = Sexagenary("乙丑甲子癸亥")
    test4 = Sexagenary("乙丑癸亥")
    test5 = test4.add(test3)
    if test5.get_sexagenary_string() != "乙丑丙寅壬戌":
        print("Error")
    test3 = Sexagenary("乙丑癸亥癸亥")
    test4 = Sexagenary("壬戌癸亥")
    test5 = test4.add(test3)
    if test5.get_sexagenary_string() != "丙寅壬戌壬戌":
        print("Error")
    test3 = Sexagenary("癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥")
    test4 = Sexagenary("癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥")
    test5 = test4.add(test3)
    if test5.get_sexagenary_string() != "乙丑甲子甲子癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥壬戌":
        print("Error")
    '''
    '''
    #减法操作检查
    test3 = Sexagenary("乙丑甲子癸亥")
    test4 = Sexagenary("乙丑癸亥")
    test5 = test3.minus(test4)
    if test5.get_sexagenary_string() != "癸亥甲子":
        print("Error")
    test3 = Sexagenary("乙丑癸亥")
    test4 = Sexagenary("乙丑癸亥")
    test5 = test3.minus(test4)
    if test5.get_sexagenary_string() != "甲子":
        print("Error")
    test3 = Sexagenary("丙寅壬戌壬戌")
    test4 = Sexagenary("壬戌癸亥")
    test5 = test3.minus(test4)
    if test5.get_sexagenary_string() != "乙丑癸亥癸亥":
        print("Error")
    test3 = Sexagenary("辛酉庚申乙丑癸亥")
    test4 = Sexagenary("壬午己卯甲子戊申")
    test5 = test3.minus(test4)
    if test5.get_sexagenary_string() != "癸卯乙巳乙丑己卯":
        print("Error")
    test3 = Sexagenary("乙丑甲子甲子癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥壬戌")
    test4 = Sexagenary("癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥")
    test5 = test3.minus(test4)
    if test5.get_sexagenary_string() != "癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥":
        print("Error")
    test3 = Sexagenary("辛巳")
    test4 = Sexagenary("庚申")
    test5 = test3.minus(test4)
    test3 = Sexagenary("辛巳")
    test4 = Sexagenary("乙丑庚申")
    test5 = test3.minus(test4)
    test3 = Sexagenary("辛巳")
    test4 = Sexagenary("庚丑")
    test5 = test3.minus(test4)
    '''
    '''
    #乘法操作检查
    test3 = Sexagenary("乙丑甲子癸亥")
    test4 = Sexagenary("乙丑癸亥")
    test5 = test4.multiply(test3)
    if test5.get_sexagenary_string() != "丙寅甲子辛酉乙丑":
        print("Error")
    test3 = Sexagenary("乙丑癸亥癸亥")
    test4 = Sexagenary("壬戌癸亥")
    test5 = test4.multiply(test3)
    if test5.get_sexagenary_string() != "乙丑辛酉辛酉乙丑乙丑":
        print("Error")
    test3 = Sexagenary("癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥")
    test4 = Sexagenary("癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥")
    test5 = test4.multiply(test3)
    if test5.get_sexagenary_string() != "癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥癸亥壬戌癸亥癸亥甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子甲子乙丑":
        print("Error")
    '''
    '''
    #测试toDecimal函数和toChinese函数以及yearToSgnr函数
    test6 = Sexagenary("乙丑丙寅")
    if test6.toDecimal() != "62":
        print("Error")
    if test6.toChinese() != "陆拾贰":
        print("Error")
    test6 = Sexagenary("壬寅癸未庚申戊辰")
    if test6.toDecimal() != "8279764":
        print("Error")
    if test6.toChinese() != "捌佰贰拾柒万玖仟柒佰陆拾肆":
        print("Error")
    test6 = Sexagenary("己巳壬午辛丑")
    if test6.toDecimal() != "19117":
        print("Error")
    if test6.toChinese() != "壹万玖仟壹佰壹拾柒":
        print("Error")
    test6 = Sexagenary("甲子")
    if test6.toDecimal() != "0":
        print("Error")
    if test6.toChinese() != "零":
        print("Error")
    test6 = Sexagenary("丙子")
    if test6.toDecimal() != "12":
        print("Error")
    if test6.toChinese() != "拾贰":
        print("Error")
    test6 = Sexagenary("乙丑丁卯丁巳甲申")
    if test6.toDecimal() != "230000":
        print("Error")
    if test6.toChinese() != "贰拾叁万":
        print("Error")
    test6 = Sexagenary("辛亥乙酉丁未甲申")
    if test6.toDecimal() != "10230200":
        print("Error")
    if test6.toChinese() != "壹仟零贰拾叁万零贰佰":
        print("Error")
    test6 = Sexagenary("庚午丙午丙辰丁丑丁酉")
    if test6.toDecimal() != "87020013":
        print("Error")
    if test6.toChinese() != "捌仟柒佰零贰万零壹拾叁":
        print("Error")
    test6 = Sexagenary("戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅戊寅")
    if test6.toDecimal() != "528657976112464059180067355005830508474576271186440677966101694915254":
        print("Error")
    if test6.yearToSgnr(1022) != "壬戌":
        print("Erroe")
    if test6.yearToSgnr(2018) != "戊戌":
        print("Erroe")



    print("success")


if __name__ == "__main__":
    mytest()

