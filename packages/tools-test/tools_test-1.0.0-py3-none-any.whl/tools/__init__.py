import copy
import datetime
import json
import random
import string
import time
import allure
from dateutil.relativedelta import relativedelta
from jsonpath import jsonpath
from loguru import logger
from urllib3 import encode_multipart_formdata
from xlrd import open_workbook
from xlutils.copy import copy as xlcopy
import itertools


def exec_func(func: str):
    """
    执行字符串类型函数
    :param func: 字符串形式调用函数
    :return: 返回str类型结果
    """

    # 得到一个局部的变量字典，来修正exec函数中的变量，在其他函数内部使用不到的问题
    loc = locals()
    exec(f"result = {func}")
    return str(loc['result'])


def extractor(obj: dict, expr: str = '.'):
    """
       jsonPath语法提取数据，返回list，用法同extractor
       :param obj: 数据
       :param expr: jsonPath表达式
       :return: 提取到的数据列表 或 False
       """

    try:
        # 有时候需要list,这里还是取到什么返回什么
        result = jsonpath(obj, expr)
        if result == False:
            return False
        # 只有一个数时，直接返回这个数，不返回列表
        if len(result) == 1:
            result = result[0]
        return result
    except Exception as e:
        logger.error(f'{expr} - 提取不到内容，丢给你一个错误！{e}')
        return False


def rep_expr(data, pool):
    """
    替换数据
    :param data: 源数据，$name 或 ${name} 中的数据会被替换
    :param pool: 参数池，在参数池中匹配
    :return: 返回源数据替换后的数据，没匹配到不替换
    注意：为了保证报告中的断言顺序，这里没有替换数据也会删除key再重新添加一次
    """
    if '$' not in str(data):
        return data

    # data为字典处理
    if isinstance(data, dict):
        copy_data = copy.deepcopy(data)
        for k, v in data.items():
            temp_k = None

            # 为str的key才处理
            if isinstance(k, str):
                # 删除copy_data相应k的数据
                del copy_data[k]
                # key处理，$开头时处理，除去jsonPath表达式
                if k[0] == '$' and k[1] != '.' and k[1] != '{':
                    # 从pool中取出变量替换key
                    temp_k = pool.get(k[1:])

                # 如果存在temp_k，说明是$var 或${}格式
                if temp_k is not None:
                    k = temp_k

                # 再判断是否还有$的数据，直接当字符串替换
                if isinstance(k, str) and "$" in k:
                    # 按字符串模版替换
                    k = string.Template(k).safe_substitute(pool)

                copy_data[k] = v

            else:
                # 其它数据类型，直接删除再添加一次即可
                del copy_data[k]
                copy_data[k] = v

            # value处理直接递归即可
            value = rep_expr(v, pool)
            # 都用赋值方式操作，updata数据会为None
            copy_data[k] = value
        # 最终需要返回data,深拷贝是为了修改key
        data = copy_data


    # list和元组就循环递归处理
    elif isinstance(data, list):

        for i in range(len(data)):
            data[i] = rep_expr(data[i], pool)
        return data

    # 元组处理
    elif isinstance(data, tuple):
        data_list = list(data)
        for i in range(len(data)):
            data_list[i] = rep_expr(data[i], pool)
        data = tuple(data_list)
        return data

    # 字符串处理，除去上面的，如果包含$的都是字符串处理,但是为了匹配数据类型，还是得判断一下
    else:
        # 从数据池获取替换
        if data[0] == '$' and data[1] != '.' and data[1] != '{':
            slices_data = data[1:]
        else:
            # 如果其中还有$，就直接字符串模版方式替换
            return string.Template(str(data)).safe_substitute(pool)

        res = pool.get(slices_data)

        if res is not None:
            return res
        # 如果没获取到就返回本身
        else:
            return data

    return data


def allure_title(title):
    # """
    # allure中生成动态用例标题。文档不对外开放，注释。
    # :param title: 需要设置的title
    # :return: None
    # """

    title = str(title)
    allure.dynamic.title(title)


def allure_step(step: str, var):
    # """
    # allure中生成步骤及附件。文档不对外开放，注释。
    # :param step: 步骤及附件名称
    # :param var: 附件内容
    # :return: None
    # """

    with allure.step(step):
        allure.attach(
            json.dumps(
                var,
                ensure_ascii=False,
                indent=4),
            step,
            allure.attachment_type.JSON)


def allure_step_no(step):
    # """
    # allure中无附件的操作步骤。文档不对外开放，注释。
    # :param step: 步骤名称
    # :return: None
    # """

    with allure.step(step):
        pass


def get_r(version=1):
    # """
    # _r参数的生成,版本默认1。文档不对外开放，注释。
    # :param version:
    # :return: _r 参数
    # """

    # 第一步：计算13位时间戳 * 0-1随机数 * 10000的值的绝对值
    # 13位时间戳生成,默认是10位的，以秒为单位，用round四舍五入一下即可
    key = str(abs(int(round(time.time() * 1000) * random.random() * 10000)))

    # 第二步：key每一位转为int，循环相加，得到sum
    sum = 0
    for i in range(len(key)):
        sum = sum + int(key[i])

    # 第三步：sum加上key的长度
    sum = sum + len(str(key))

    # 第四步：不足3位的前面补0
    sum = str("{0:03d}".format(sum))

    # 第五步：版本号(默认1) + key + sum
    _r = str(version) + key + sum
    return _r


def updateDict(src, k, v):
    # """
    # 文档不对外开放，注释。
    # 给src源数据字典更新值，如果源数据为空，创建空字典，有数据就更新，没数据就增加
    # 使用场景：url拼接_r参数
    # :param src: 源字典
    # :param k: 需要更新字典的key
    # :param v: 更新值
    # :return: src更新后的dict
    # """
    if src is None:
        src = {}
    src.update({k: v})
    return src


def chinas():
    """
    随机汉字
    """
    while True:
        try:
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xfe)
            val = f'{head:x} {body:x}'
            str = bytes.fromhex(val).decode('gb2312')
            return str
        except Exception:
            pass


def rand_num(n):
    """"
    生成范围内随机数据
    """
    # 下限
    start = 10 ** (n - 1)
    # 上限
    end = 10 ** n - 1

    return random.randint(start, end)


def Random_To_List(Punctuations=0, Chinas=0, Numbers=0, Englishs=0, StrNumbers=0, All='yes', Add=[]):
    """
    :param Punctuations: 随机N个特殊符号
    :param Chinas: 随机N个中文
    :param Numbers: 随机N个数字
    :param Englishs: 随机N个英文单词
    :param All:  yes/no  是否把所有的随机数变成字符串
    :param Add: 往列表内插入自己想要的数据
    :return: 随机组合成为列表
    """

    List = []
    str_result = ''

    if Punctuations != 0:
        for i in range(Punctuations):
            punctuation = ''
            not_included_str = ["'", "/", "\"", "\\", "$", "%", "?", "=", "|"]
            while True:
                generate_str = random.sample(string.punctuation, 1)[0]
                if generate_str not in not_included_str:
                    punctuation += generate_str
                    break

            List.append(punctuation)
            str_result += punctuation

    if Chinas != 0:
        chinese = ''
        for i in range(0, Chinas):
            val = chinas()
            chinese += val
        List.append(chinese)
        str_result += chinese

    if Numbers != 0:
        digits = rand_num(Numbers)
        List.append(digits)
        str_result += str(digits)

    if Englishs != 0:
        english = ''.join(random.sample(string.ascii_letters, Englishs))
        List.append(english)
        str_result += english

    if StrNumbers != 0:
        str_digits = str(rand_num(StrNumbers))
        List.append(str_digits)
        str_result += str_digits

    if Add != []:
        for i in Add:
            List.append(i)

    if All == 'no':
        # 如果只有1条数据就返回数据本身
        if len(List) == 1:
            List = List[0]
        return List
    else:
        return str_result


def time_to_make(Time: int):
    """
    :param Time:获取N天前后的年月日
    :return:返回年月日
    """
    # 获取当前时间
    today = datetime.date.today()
    # 获取下个月的今天

    # 前一个月的月份
    if Time >= 0:
        lastMonth = today + datetime.timedelta(days=Time)
        return str(lastMonth)
    else:
        lastMonth = today + datetime.timedelta(days=Time)
        return str(lastMonth)


def merge_dict(dic1, dic2):
    """
    递归合并两个字典所有数据,有相同的就更新，不相同的就添加
    :param dic1: 基本数据
    :param dic2: 以dic2数据为准，dic1和dic2都有的数据，合并后以dic2为准
    :return: 合并后的字典
    """

    # 类型不同就直接赋值,返回第2个参数数据，是因为我们以第2个数据为准，来更新第1个数据的。
    if type(dic1) != type(dic2):
        return dic2

    # 两个字典深拷贝一下，避免影响之前数据
    obj1 = copy.deepcopy(dic1)
    obj2 = copy.deepcopy(dic2)

    # 都是字典时处理
    if isinstance(obj2, dict):
        for k, v in obj2.items():

            obj1_value = obj1.get(k)
            if obj1_value is None:
                obj1[k] = v
            else:
                obj1[k] = merge_dict(obj1[k], obj2[k])


    elif isinstance(obj2, list):
        for i in range(len(obj2)):
            try:
                obj1[i] = merge_dict(obj1[i], obj2[i])
            except IndexError:
                obj1.append(obj2[i])

    elif isinstance(obj2, tuple):
        for i in range(len(obj2)):
            try:
                # 元组不能修改，先转list再修改后再转回元组
                obj1 = list(obj1)
                obj1[i] = merge_dict(obj1[i], obj2[i])
                obj1 = tuple(obj1)

            except IndexError:
                obj1 += (obj2[i],)


    else:
        # 以第2个参数数据为准，返回obj2
        return obj2

    return obj1


def upload_excel_template(file_path: str, data: dict, sheet_index=0):
    """
    根据文件路径读取文件，并追加内容
    :param file_path:
    :param file_path: 源文件路径
    :param data: 需要追加的内容，格式为{key:[v1,v2...]}这里的key就是表头，注意value的列表长度一致
    :return: None，追加完内容会覆盖源文件
    """
    r_xls = open_workbook(file_path)  # 读取excel文件
    # 拿到第一个sheet页的表头数据处理保存在字典
    sh = r_xls.sheet_by_index(sheet_index)
    # 存储表头数据
    one_row = sh.row(0)
    for i in range(len(one_row)):
        one_row[i] = str(one_row[i]).split(":")[-1].split("'")[1]

    row = r_xls.sheets()[sheet_index].nrows  # 获取已有的行数
    excel = xlcopy(r_xls)  # 将xlrd的对象转化为xlwt的对象
    sheet = excel.get_sheet(sheet_index)  # 获取要操作的sheet

    # 获取第一条数据的value值长度
    length = len(list(data.values())[0])
    row_num = row
    # 先追加序号,有些excel无序号，这里弃用
    # for i in range(length):
    #     sheet.write(row_num, 0, row_num)
    #     row_num += 1

    # 循环追加数据
    row_num_key = row

    for k, v in data.items():
        if k in one_row:
            index = one_row.index(k)
            for j in range(length):
                sheet.write(row_num_key, index, v[j])
                row_num_key += 1
            # 下一个键值重置行序号
            row_num_key = row

    excel.save(file_path)  # 保存并覆盖文件


def form_data_type_judge(data):
    type = data.get("data_type")

    if type != "multipart/form-data":
        return data
    if type == "multipart/form-data":
        del data["data_type"]

    # 注意data字典中的value要是json字符串，不能是字典
    encode_data = encode_multipart_formdata(data)
    return encode_data


def basis_key_get_dic(dic, key, type=1):
    """
    :param dic: 源字典
    :param key: 需要获取或删除的key,需要为list
    :param type: 1表示从源字典中获取这些key组成新字典，其它表示从源字典删除这些key返回源字典
    :return: 处理后的字典数据
    """
    result_dic = {}
    if type == 1:
        for k, v in dic.items():
            if k in key:
                result_dic.update({k: v})
    else:
        result_dic = copy.deepcopy(dic)
        for k, v in dic.items():
            if k in key:
                result_dic.pop(k)

    return result_dic


# def case_data_generate(case_dic):
#     """
#     用例数据生成，例：
#         传的参数为：{"plateNo": [["用例1", "预期1"],["用例2", "预期2"]]}
#         生成参数化用例结果为：[["plateNo", "用例1", "预期1"], ["plateNo", "用例2", "预期2"]]
#         因为要拿到参数名，在用例执行时，每次更新参数名，参数化所有字段进行用例执行
#     """
#     dic = copy.deepcopy(case_dic)
#     case_list = []
#     for k, v in dic.items():
#         for case in v:
#             # 注意深拷贝问题
#             case2 = copy.deepcopy(case)
#             case2.insert(0, k)
#             case_list.append(case2)
#     return case_list

def case_data_generate(case_dic, actual_ex="$.data.itemList.0.%s", type=0) -> list:
    """
    用例数据生成，例：
        传的参数为：{"plateNo": [["用例1", "预期1"],["用例2", "预期2"]]}
        生成参数化用例结果为：[["plateNo", "用例1", {"$.data.itemLIst.0.plateNo": "预期1"}], ["plateNo", "用例2", {"$.data.itemLIst.0.plateNo": "预期1"}]]
        因为要拿到参数名，在用例执行时，每次更新参数名，参数化所有字段进行用例执行
        actual_ex参数，如果预期结果为字典直接替换，如果为字符串，拼接为字典,因为expect需要的是字典，实际和预期结果
        如果指定了预期结果为字典，如下：
        {"plateNo": [["用例1", {"$.data.itemLIst.0.plateNo": "预期1"}],["用例2", {"$.data.itemLIst.0.plateNo": "预期1"}]]}
        结果同上，只是这里的实际结果，可根据需要更改，默认为$.data.itemList.0.%s，%s为变量
    """

    dic = copy.deepcopy(case_dic)
    case_list = []

    for k, v in dic.items():
        for case in v:
            # 注意深拷贝问题
            case2 = copy.deepcopy(case)
            case2.insert(0, k)
            # 如果没有预期结果，预期结果就是传的参数
            try:
                # 报错说明不存在
                temp = case2[2]
            except:
                case2.insert(2, case2[1])

            # 如果预期结果不是字典，就默认转为字典，因为expect接收字典(实际结果和预期结果),实际结果默认为$.data.itemList.0.%s
            if not isinstance(case2[2], dict):
                if "%s" in actual_ex:
                    actual = actual_ex % k
                else:
                    actual = actual_ex
                temp = case2[2]
                case2[2] = {actual: temp}

            case_list.append(case2)
            # 如果!=0表示只执行一次，拿所有参数的第一条用例数据
            if type != 0:
                break

    if type == 0:
        # 直接返回
        return case_list
    else:
        # 组合所有参数的第一条用例参数和预期结果为一条覆盖所有参数的用例
        request_dic = {}
        expect_dic = {}
        for case in case_list:
            request_dic.update({case[0]: case[1]})
            expect_dic.update(case[2])
        # 返回的数据是列表，是因为参数化时需要传入list或tuple
        return [(request_dic, expect_dic)]


def data_generate(values: list, handle_value=None):
    """
    针对每个字段的数据生成方法，生成预期和数据相同的用例数据
    values为list，传入相应生成的参数如["0","1"]
    handle_values=None时生成数据为[["0","0"], ["1","1"]]
    handle_values="int(%s)"时生成数据为[["0", 0], ["1", 1]]
    handle_values={"status": "正常"}时生成数据为["0": {"status":"正常"}, "1": {"status": "正常"}]
    handle_values={"status": "%s", "success": True}时生成数据为["0": {"status":"0", "success": True}, "1": {"status": "1", "success": True}]
    总结：handle_values为空时预期值为参数值本身
        handle_values为字符串表达式，包含%s时，%s会替换为参数值，不包含%s不替换
        handle_valeus为字典时，字典的值规则同上
    """
    case_list = []
    if handle_value is not None:
        for value in values:
            case = []
            # 先添加每个值，这是实际传的参数值
            case.append(value)

            if isinstance(handle_value, dict):
                dic = copy.deepcopy(handle_value)
                # 如果为字典，表示需要处理整个字典为预期结果的判断，需要处理其中的占位符%s
                for k, v in handle_value.items():
                    if "%s" in v:
                        replace_value = value
                        # 用eval执行，字符串需要处理
                        replace_value = f'"{replace_value}"'
                        v = eval(v % (replace_value))
                        dic.update({k: v})
                case.append(dic)
            # 作为str处理
            else:
                if isinstance(handle_value, str):
                    if "%s" in handle_value:
                        # 用eval执行，字符串需要处理
                        value = f'"{value}"'
                        # 根据%s替换表达式，然后利用eval执行得到结果，添加到列表即可
                        handle_res = eval(handle_value % (value))
                        case.append(handle_res)
                    else:
                        case.append(handle_value)

            case_list.append(case)
    else:
        # 如果不需要处理预期数据，直接生成用例数据，参数值和预期结果一致
        for value in values:
            case_list.append([value, value])

    return case_list


def batch_generate_param(params, data, handle_value=None, data_single=False):
    """
    多个字段，批量生成数据的方法
    批量生成用例数据方法，如果数据和预期的值都相同，可批量生成
    如：["a","b","c"],[1,2,3]
    结果为：{'a': [[1, 1], [2, 2], [3, 3]], 'b': [[1, 1], [2, 2], [3, 3]], 'c': [[1, 1], [2, 2], [3, 3]]}
    data_single=True时，表示数据和预期都相同，每个参数都使用相同的数据和预期结果，如下示例：
    参数为：["name", "age"]，值为：[["a", "字数超短"],[" ", "不能为空"]]
    结果为：{'name': [['a', '字数超短'], [' ', '不能为空']], 'age': [['a', '字数超短'], [' ', '不能为空']]}
    """
    dic = {}
    if not data_single:

        for param in params:
            if isinstance(data, list):
                dic.update({param: data_generate(data, handle_value)})
    else:
        for param in params:
            dic.update({param: data})

    return dic


def data_generate_boundary(value, nums: list, handle_value=None):
    """
    根据数据生成相应边界的用例，只支持传入参数为list情况，比如：value=$url，nums=[1,2]
    结果为：[[['$url'], ['$url']], [['$url', '$url'], ['$url', '$url']]]
    :param value: 需要生成的的值
    :param nums: 生成用例的边界，如1,2,9,10
    :return: 生成后的用例数据
    """

    result_data = []
    for num in nums:
        one_data = []
        param_data = []
        for i in range(num):
            # 处理预期结果数据
            if handle_value is not None:
                if isinstance(value, str):
                    value = f'"{value}"'
                value = eval(handle_value % (value))
            one_data.append(value)
        # 添加2次，因为有参数和断言
        param_data.append(one_data)
        param_data.append(one_data)
        result_data.append(param_data)

    return result_data


def generate_expect_data(request_data: dict, modify_data: dict = None, add: dict = None, delete: list = None,
                         default_expect_ex: str = None):
    """
    根据所有字段模版，生成expect断言的实际结果和预期结果，适用于所有字段断言的测试场景
    :param request_data: 请求的模版数据
    :param modify_data: 需要手动修改的字段的实际结果和预期结果
    :param default_expect_ex: 可指定实际结果提取的表达式，%s为占位符，如$.data.%s
    :param add: 要增加的key value
    :param delete: 要删除的key value只用传key即可，注意需要是list
    :return: 生成的expect断言数据
    示例：
    request_dadta = {
        "remark": Random_To_List(Englishs=10),
        "picture": "$url"
    }

    modify_data = {
        "remark": {"$.data.remark": 'remarks'},
    }
    default_expect_ex = "$.data.itemList.%s"
    结果：
    {'$.data.remark': 'remarks', '$.data.itemList.picture': '$url'}
    注意：如果default_expect_ex不填，默认为$.data.%s，一般测试的view接口是$.data.xxx，默认即可
    """
    expect = {}
    for k, v in request_data.items():
        if default_expect_ex is None:
            handle_k = f"$.data.{k}"
        else:
            handle_k = default_expect_ex % (k)

        # 如果存在删除的key中不处理
        if delete is not None and k in delete:
            continue

        # 如果k在需要修改的字典中存在就直接更新为需要手动修改的值
        if modify_data != None and k in modify_data:
            expect.update(modify_data.get(k))
        else:
            expect.update({handle_k: v})

    # 增加要断言的key value
    if add is not None:
        expect = merge_dict(expect, add)

    return expect


def time_generate():
    """
    根据当前时间创建今天、昨天、当月、上个月、当年、上一年的开始和结束时间
    解释：所有后缀都是00:00:00，因为传的这个时间后端没处理，开始时间都是00:00:00,结果时间都是23:59:59
    :return: 相应的时间
    """
    # 后缀
    suffix = " 00:00:00"

    # 当天时间
    today = datetime.date.today()

    # 今天时间
    today_time = str(today) + suffix

    # 昨天时间
    yesterday_time = str(today - datetime.timedelta(days=1)) + suffix

    # 明天时间
    tomorrow_time = str(today + datetime.timedelta(days=1)) + suffix

    # 当月时间
    currentMonth_start_time = str(datetime.datetime(today.year, today.month, 1))
    # 下个月第1天，减1天就是这个月最后一天
    # 关键字加s表示做加减，不加s表示指定为xx时间，比如day=1，表示指定为1号，days=1表示在某个时间上加1天
    currentMonth_end_time = str(datetime.datetime(today.year, today.month, 1) + relativedelta(months=+1, days=-1))

    # 上月开始时间
    lastMonth_start_time = str(today + relativedelta(months=-1, day=1))
    # 上月结束时间
    lastMonth_end_time = str(today + relativedelta(days=-1))

    # 本年的第一天和最后一天
    currentYear_start_time = str(datetime.datetime(today.year, 1, 1))
    currentYear_end_time = str(datetime.datetime(today.year, 1, 1) + relativedelta(years=+1, days=-1))

    # 去年第一天和最后一天
    lastYear_start_time = str(datetime.datetime(today.year - 1, 1, 1))
    lastYear_end_time = str(datetime.datetime(today.year, 1, 1) + relativedelta(days=-1))

    result = {
        "today_time": today_time,
        "yesterday_time": yesterday_time,
        "tomorrow_time": tomorrow_time,
        "currentMonth_start_time": currentMonth_start_time,
        "currentMonth_end_time": currentMonth_end_time,
        "lastMonth_start_time": lastMonth_start_time,
        "lastMonth_end_time": lastMonth_end_time,
        "currentYear_start_time": currentYear_start_time,
        "currentYear_end_time": currentYear_end_time,
        "lastYear_start_time": lastYear_start_time,
        "lastYear_end_time": lastYear_end_time,
    }

    return result


def generate_expect(case_dic: dict = None, actual_ex: str = "$.data.%s", del_expect: list = None,
                    add_expect: dict = None):
    """
    根据必填字段，或所有字段模板生成断言数据，也就是expect中需要的数据
    :param case_dic: 请求数据字典
    :param actual_ex: 根据表达式断言，%s提取请求数据的每一个key替换
    :param del_expect: 要排除的key（不需要断言的，或断言需要更改的）,list的方式如["name", "age"]，就会排除
    :param add_expect: 新增需要断言的key value，字典格式即可，如：{"$.data.itemList.0.id": 123},会追加断言
    :return:
    """
    res = {}
    if case_dic is not None:
        case = copy.deepcopy(case_dic)
        for k, v in case.items():
            # 排除某些字段
            if del_expect is not None:
                if k in del_expect:
                    continue
            # 排除有些异常场景断言都是一样的key的情况如:$.message，没有%s会报错，这里处理下
            if "%s" in actual_ex:
                k = actual_ex % k
                res.update({k: v})
            else:
                # 如果断言的实际结果一样，为key会重复，只保留一个，所以这里把v改为key，但是要注意值不重复-不推荐使用此方案
                k = actual_ex
                res.update({v: k})

    # 更新某些断言
    if add_expect is not None:
        for k, v in add_expect.items():
            res.update({k: v})

    return res


def makeTime(str_time):
    """
    将结构化时间转为13位时间戳
    """
    # 先转换为格式化时间
    str_time = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳
    timestamp = int(time.mktime(str_time)) * 1000

    return timestamp


def case_generate_cartesian_product(*args):
    """
    笛卡尔积用例数据生成
    *args: 多个list
    :return: 生成的用例数据
    """

    res = [[list(res), ""] for res in itertools.product(*args)]
    return res


if __name__ == '__main__':
    res = Random_To_List(Chinas=4, Englishs=4, Numbers=12, Punctuations=4, StrNumbers=12, Add=['1', 123], All="no")
    print(res)
    r = get_r()
    print(r)
