# -*- coding:utf-8 -*-

import random


class StudentInfo:
    """
    生成学员数据
    """

    @classmethod
    def student(cls, prePhone='999'):
        """
        生成学员证件号、姓名、性别、生日、手机号数据
        :param prePhone: 默认手机号前3位
        :return: 生成的学员的数据
        """
        # 证件号
        identityCard = cls.identityCard()
        # 姓名
        name = cls.getName()
        # 性别
        gender = cls.getGender(identityCard)
        # 生日
        birthday = cls.getBirthday(identityCard)
        # 手机号
        phone = cls.generatePhone(prePhone)

        stu = {
            'identityCard': identityCard,
            'name': name,
            'gender': gender,
            'birthday': birthday,
            'phone': phone,
        }

        return stu

    @classmethod
    def identityCard(cls):
        """
        生成身份证
        :return: 身份证号码
        """

        li = ["11", "12", "13", "14", "15", "21", "22", "23", "31", "32", "33", "34", "35", "36", "37", "41", "42",
              "43", "44", "45", "46", "50", "51", "52", "53", "54", "61", "62", "63", "64", "65"]
        preTwoCard = random.sample(li, 1)[0]
        preFourCard = random.randint(1000, 9999)

        preSixCard = str(preTwoCard) + str(preFourCard)
        # 拼接生日,拼接随机3位数
        card = preSixCard + cls.randomBirthday() + cls.randomCode()

        # 传入17位算出第18位
        num = cls.calcTrailingNumber(card)
        # 拼接完整证件号

        card += num

        return card

    @classmethod
    def randomBirthday(cls):
        """
        生成生日
        :return: 生成的生日数据
        """
        year = random.randint(1970, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # 28天，解决有的月份没有那么多天问题

        if month < 10:
            month = '0' + str(month)
        if day < 10:
            day = '0' + str(day)

        return str(year) + str(month) + str(day)

    @classmethod
    def randomCode(cls):
        """
        随机4位卡号
        :return: 返回4位卡号
        """
        code = random.randint(1, 1000)
        if code < 10:
            code = '00' + str(code)
        elif code < 100:
            code = '0' + str(code)
        else:
            return str(code)
        return str(code)

    @classmethod
    def calcTrailingNumber(cls, card):
        """
        根据身份证前17位计算第18位
        :param card: 身份证号前17位
        :return: 返回第18位
        """
        "传前17位算出第18位：computList和证件号的每一位相乘并相加，取余11，得到最后一位索引，然后在lastNum"
        if len(card) != 17:
            return '号码不正确，请传入17位号码'
        computList = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        lastNum = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

        res = 0
        for i in range(len(card)):
            res += int(card[i]) * int(computList[i])

        return str(lastNum[res % 11])

    @classmethod
    def getName(cls):
        """
        随机生成姓名
        :return: 姓名
        """
        name1 = "艾爱新觉罗敖爱安陵安国昂奥傲隞奥敦巴把八拜摆百白马柏伯白百里把利板般班邦宝暴鲍贝卑北邶北宫北唐奔本闭比邲蔽碧鲁洪毕卞边表标别宾并丙薄播泊博伯牙吾台博罕岱博鲁特博尔济锦孛儿只斤巴林步禄孤步六孤卜步布菜采彩才才旦苍梧蔡苍臧漕肏曹策茶察岑柴虿产镡单于唱常昌敞苌长兴长沙抄潮朝超钞晁巢车陈郴晨陈没尘称成王城呈承成程迟池茌赤叱干宠种崇充虫禤丑仇由除初厨人楚储褚出啜揣啜剌传解谢新楚特忻辛信心欣信都性刑行姓幸邢熊修修鱼续徐须胥许婿徐离铉玄宣轩辕薛穴踅寻荀押牙亚筵"
        name2 = "壹那蒌弋裔移伊尔根觉罗抑壹倚毅矣银殷尹印阴鄞淫营殷勤勇应英永鄘攸右油由游尤有酉兀有宥由吾遇玉愈宇俞羽尉喻庾虞蔚于余於鱼禹郁语豫吁臾原苑尉迟宇文元袁员爰源辕月乐正乐岳越恽云运贠再宰宰父赞昝臧造遭笮曾迮札拉楚特札哈齐特扎窄绽查翟战湛占詹展章张仉张包掌鄣漳长孙赵柘戢招肇诏召照兆昆钊真甄枕针蒸政征正郑挚郅支职植智陟脂芷致直只芝彘徵中重众衷仲终钟中叔仲长舟钟离仲孙周住烛蓍主父诸竺祝朱竹主诸葛顓孫壮颛顼庄卓禚子丰子革子国子孔子人子驷子轩資子子雅紫訾自子车宗纵宗圣宗政鄹俎柞佐左丘邹祖左"

        preName = None
        preName1 = random.sample(name1, 1)[0]
        preName2 = random.sample(name1, 2)
        lastName = random.sample(name2, 1)[0]
        num = random.randint(1, 2)
        if num == 1:
            preName = preName1
        else:
            preName = preName2[0] + preName2[1]

        return preName + lastName

    @classmethod
    def getGender(cls, identityNumber):
        "算出性别"
        gender = identityNumber[-2]  # 第17位
        gender = int(gender) % 2
        return gender

    @classmethod
    def getBirthday(cls, identityNumber):
        birthday = identityNumber[6:10] + "-" + identityNumber[10:12] + "-" + identityNumber[12:14]

        return birthday

    @classmethod
    def generatePhone(cls, prePhone):
        "生成手机号，前面3位144，根据项目要求固定"
        num = random.randint(11111111, 99999999)

        phone = prePhone + str(num)

        return phone


if __name__ == '__main__':
    res = StudentInfo.student()
    print(res)
