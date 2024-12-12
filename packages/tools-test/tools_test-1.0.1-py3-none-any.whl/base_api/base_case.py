import copy
from base_api.base_requests import BaseRequest
from tools.data_process import DataProcess


class BaseCaseAction:
    """
    基类：通用执行用例类，封装通用断言方法，和不断言的方法
    类属性目的：
            1. 指定可用的关键字
            2. 构造方法中可通过self.xx来获取其父类(此类子类)中的类属性，如果类属性也没有会找到父类的这个属性，为None即可，不然self.xx获取时会报错
    """

    # 请求方式
    method: str = None
    # 请求路径
    path: str = None
    # 测试标题
    title: str = None
    # 测试步骤
    step: str = None
    # 请求头
    header: dict = None
    # params参数
    params: dict = None
    # data参数
    data: dict = None
    # json参数
    json: dict = None
    # 上传文件
    files: dict = None
    # 提取变量
    extract: dict = None
    # 预期结果
    expect: dict = None
    # 自定义断言
    expect_custom: dict = None
    # 关联功能用例id
    relation: dict = None

    # 构造方法就是为了让在实例化对象时，也可以直接指定这些参数
    def __init__(self, method: str = None, path: str = None, title: str = None, step: str = None, header: dict = None,
                 params: dict = None,
                 data: dict = None, json: dict = None,
                 files: dict = None,
                 extract: dict = None, expect: dict = None, expect_custom: dict = None, relation: dict = None):

        # 构造方法中传了参数就以传的为准，不传就拿类的，但是注意深拷贝一份，避免修改会影响其他对象的问题
        # 请求方式
        self.method: str = method or copy.deepcopy(self.method)
        # 请求路径
        self.path: str = path or copy.deepcopy(self.path)
        # 测试标题
        self.title: str = title or copy.deepcopy(self.title)
        # 测试步骤
        self.step: str = step or copy.deepcopy(self.step)
        # 请求头
        self.header: dict = header or copy.deepcopy(self.header)
        # params参数
        self.params: dict = params or copy.deepcopy(self.params)
        # data参数
        self.data: dict = data or copy.deepcopy(self.data)
        # json参数
        self.json: dict = json or copy.deepcopy(self.json)
        # 上传文件
        self.files: dict = files or copy.deepcopy(self.files)
        # 提取变量
        self.extract: dict = extract or copy.deepcopy(self.extract)
        # 预期结果
        self.expect: dict = expect or copy.deepcopy(self.expect)
        # 自定义断言
        self.expect_custom: dict = expect_custom or copy.deepcopy(self.expect_custom)
        # 关联功能用例id
        self.relation: dict = relation or copy.deepcopy(self.relation)

    def action(self):
        """
            action通用方法
        """
        #  -- 该项目用不上
        # 运行前先判断accessToken，未配置不会执行(这是业务的特殊处理)
        # self.__grant_access_token()

        # 这里先用payload传参数，以前的请求封装使用的是类方法，改动太大，后续可优化(初始化BaseRequest对象，直接设置即可)
        # b = BaseRequest() b.title = "测试" ...
        # 拿对象的所有属性即可，但是注意深拷贝，因为这里不是对象，字典会修改引用的数据
        payload = copy.deepcopy(self.__dict__)

        # 执行用例->所有参数字典丢给send_request处理即可
        response, expect, expect_custom = BaseRequest.send_request(payload)
        # 通用断言
        DataProcess.assert_result(response, expect)
        # 自定义断言
        if expect_custom is not None:
            DataProcess.expect_keyword(response, expect_custom)

        return response, expect, expect_custom

    # 有项目限的token再使用
    # def __grant_access_token(self):
    #     """
    #     获取accessToken，有效期5分钟内可获取新token
    #     注意：登录后再获取
    #     """
    #
    #     # 查看配置，如果未配置x-sso-token不处理access_token
    #     token_conig = ReadFile.read_config("$.access_token")
    #     if token_conig != True:
    #         return
    #
    #     # 判断是否小于5分钟300000ms，小于5分钟就再获取一下，后续每个请求携带该token。注意这是在登录后才处理的。
    #     # 由于时间戳存在误差，是四舍五入的，保险起见以4分钟来计算
    #     try:
    #         # 1. 获取当前时间戳
    #         now = round(time.time() * 1000)
    #
    #         # 2. 获取参数池中过期时间
    #         expiresIn = DataProcess.extract_data('expiresIn')
    #
    #         # 3. 如果没有过期时间，或小于当前时间，就调用接口，更新x-puat和过期时间
    #         if not expiresIn or expiresIn < now:
    #             # 定义获取token请求数据
    #             payload_grant_access_token = {
    #                 'path': "/api/paas/core/user/grant-access-token.htm"
    #             }
    #
    #             # 先判断是否设置了cookie，如果设置了就不登录了，如果未配置cookie，先登录再重新获取token
    #             header = {}
    #             cookie = ReadFile.read_config('$.cookie')
    #             # 4. 取配置的cookie或从登录拿paasToken
    #             if cookie != False:
    #                 header.update({"cookie": cookie})
    #
    #             else:
    #                 paasToken = DataProcess.extra_pool.get("access_token_login")
    #                 # 从数据池获取不到token时再请求
    #                 if paasToken is None:
    #                     # 先登录再设置cookie
    #                     payload_login = {
    #                         'path': '/jiaxiao-paas/api/paas/core/user/temp-login.htm',
    #                         'method': 'post',
    #                         'params': {
    #                             'phone': ReadFile.read_config('$.loginUser.phone')
    #                         },
    #                         "extract": {
    #                             "paasToken": "$.data.paasToken",
    #                             "tenant_id": "$.data.tenantList.0.id"
    #                         }
    #                     }
    #
    #                     response_login, _, expect_custom = BaseRequest.send_request(payload_login)
    #                     paasToken = extractor(response_login, "$.data.paasToken")
    #                     DataProcess.extra_pool.update({'access_token_login': paasToken})
    #
    #                     # 如果是多租户，需要再次调用login-tenant.htm接口
    #                     # 读取配置文件中的驾校id
    #                     tenant_id_conf = ReadFile.read_config("$.tenant_id")
    #                     # 第1个租户的驾校id
    #                     tenant_id = DataProcess.extract_data("tenant_id")
    #                     # 根据tenant_id判断是否是多租户，单租户tenant_id是false, 是多租户才执行该接口
    #                     if tenant_id:
    #                         # 如果配置了驾校id就用配置的，未配置，就用获取的第1个驾校id
    #                         if tenant_id_conf:
    #                             id = tenant_id_conf
    #                         else:
    #                             id = tenant_id
    #                         payload_login_tenant = {
    #                             'path': '/api/paas/core/user/login-tenant.htm',
    #                             'method': 'post',
    #                             'header': {
    #                                 'cookie': "_putk_=" + paasToken
    #                             },
    #                             'data': {
    #                                 'tenantId': id
    #                             }
    #                         }
    #                         BaseRequest.send_request(payload_login_tenant)
    #
    #                 cookie = "_putk_=" + paasToken
    #                 header.update({"cookie": cookie})
    #                 # 更新全局header的cookie
    #                 DataProcess.header.update({"cookie": cookie})
    #
    #             # 更新请求头
    #             payload_grant_access_token.update({'header': header})
    #
    #             # 循环3次，避免该接口出现失败情况
    #             for i in range(3):
    #
    #                 # 5. 获取access_token
    #                 response_access_token, _, expect_custom = BaseRequest.send_request(payload_grant_access_token)
    #                 # 6. 提取x-puat
    #                 x_puat = extractor(response_access_token, '$.data.accessToken')
    #                 # 7. 提取过期时间
    #                 expiresIn = extractor(response_access_token, "$.data.expiresIn")
    #                 # 8. 过期时间处理, 5分钟内可重新获取新token，这里保险起见减4分钟
    #                 expiresIn = now + expiresIn - (4 * 60 * 1000)
    #                 # 9. 存储x-puat和expiresIn
    #                 # 10. 如果提取到x_puat直接结束循环
    #                 if x_puat:
    #                     DataProcess.extra_pool.update({'x-puat': x_puat})
    #                     DataProcess.extra_pool.update({'expiresIn': expiresIn})
    #                     break
    #                 else:
    #                     # 打印错误信息
    #                     logger.info("response_access_token" + str(response_access_token))
    #
    #     except Exception as e:
    #         logger.info("x-puat获取异常=======> " + str(e))
    #         # 出错就初始化过期时间，0 即为False，下一次判断不成功会重新请求获取access_token
    #         DataProcess.extra_pool.update({'expiresIn': 0})

# 弃用该方式
# class BaseCaseExecute:
#     """
#     基类：通用执行用例类，可封装通用断言方法，和不断言的方法
#     注意：请求方式不传默认为 GET 请求
#     """
#
#     # 弃用-暂存，原因：所有接口都只维护了path和method，其它数据都有机率需要或不需要，所以这里只处理path和method即可，
#     # 这样模版属性就不用单独维护一个类了
#     # @classmethod
#     # def merge_data(cls, api_obj_data_all, data):
#     #     """
#     #     合并api对象类中的数据和用例中的data数据
#     #     :param api_obj_data: 调用的api对象类中的数据
#     #     :param data: data是用户中传过来的data数据
#     #     :return: 返回合并后的数据
#     #     """
#     #
#     #     api_obj_data = {}
#     #
#     #     for k, v in api_obj_data_all:
#     #         # __开头和结尾、然后不是方法的，提取出来，和data中的数据合并。注意排除实例方法、类方法、和静态方法。
#     #         if not k.startswith('__') and not k.endswith('__') and not callable(v) and not isinstance(v,
#     #                                                                                                   classmethod) and not isinstance(
#     #             v, staticmethod):
#     #             api_obj_data.update({k: v})
#     #
#     #     # 更新请求字典
#     #     merged = merge_dict(api_obj_data, data)
#     #
#     #     return merged
#
#     @classmethod
#     def basic_attr(cls, data):
#         """
#         获取api对象类的path和method然后和请求数据合并
#         """
#         path = cls.__dict__.get("path")
#         method = cls.__dict__.get("method")
#
#         if path is not None:
#             data = merge_dict({"path": path}, data)
#         if path is not None:
#             data = merge_dict({"method": method}, data)
#
#         return data
#
#     @classmethod
#     def execute(cls, data=None, reverse=True):
#         """
#         通用执行用例的方法：默认通用断言，断言响应中的success为True
#         :param data:
#         :return:
#         """
#         # 运行前先判断accessToken
#         cls.__grant_access_token()
#
#         # 调用方法合并path和method
#         data = cls.basic_attr(data)
#
#         # 执行用例->所有参数字典丢给send_request处理即可
#         response, expect, expect_custom = BaseRequest.send_request(data, reverse)
#         # 通用断言
#         if expect is not None:
#             DataProcess.assert_result(response, expect)
#         # 自定义断言
#         if expect_custom is not None:
#             DataProcess.expect_keyword(response, expect_custom)
#
#         return response, expect, expect_custom
#
#     @classmethod
#     def execute_no_assert(cls, data=None, reverse=True):
#         """
#         cls.__dict__.items拿到所有的的类对象属性和方法给到merge_data处理，只要我们需要的属性。
#         :param data: data是用例中请求的数据
#         :return: None
#         """
#
#         # 运行前先判断accessToken
#         cls.__grant_access_token()
#
#         # 调用方法合并path和method
#         data = cls.basic_attr(data)
#
#         # 执行用例->所有参数字典丢给send_request处理即可
#         response, expect, expect_custom = BaseRequest.send_request(data, reverse)
#
#         return response, expect, expect_custom
#
#     @classmethod
#     def __grant_access_token(cls):
#         """
#         获取accessToken，有效期5分钟内可获取新token
#         注意：登录后再获取
#         """
#
#         # 查看配置，如果未配置x-sso-token不处理access_token
#         token_conig = ReadFile.read_config("$.access_token")
#         if token_conig != True:
#             return
#
#         # 判断是否小于5分钟300000ms，小于5分钟就再获取一下，后续每个请求携带该token。注意这是在登录后才处理的。
#         # 由于时间戳存在误差，是四舍五入的，保险起见以4分钟来计算
#         try:
#             # 1. 获取当前时间戳
#             now = round(time.time() * 1000)
#
#             # 2. 获取参数池中过期时间
#             expiresIn = DataProcess.extract_data('expiresIn')
#
#             # 3. 如果没有过期时间，或小于当前时间，就调用接口，更新x-puat和过期时间
#             if not expiresIn or expiresIn < now:
#                 # 定义获取token请求数据
#                 payload_grant_access_token = {
#                     'path': "/api/paas/core/user/grant-access-token.htm"
#                 }
#
#                 # 先判断是否设置了cookie，如果设置了就不登录了，如果未配置cookie，先登录再重新获取token
#                 header = {}
#                 cookie = ReadFile.read_config('$.cookie')
#                 # 4. 取配置的cookie或从登录拿paasToken
#                 if cookie != False:
#                     header.update({"cookie": cookie})
#
#                 else:
#                     paasToken = DataProcess.extra_pool.get("access_token_login")
#                     # 从数据池获取不到token时再请求
#                     if paasToken is None:
#                         # 先登录再设置cookie
#                         payload_login = {
#                             'path': '/jiaxiao-paas/api/paas/core/user/temp-login.htm',
#                             'method': 'post',
#                             'params': {
#                                 'phone': ReadFile.read_config('$.loginUser.phone')
#                             },
#                             "extract": {
#                                 "paasToken": "$.data.paasToken",
#                                 "tenant_id": "$.data.tenantList.0.id"
#                             }
#                         }
#
#                         response_login, _, expect_custom = BaseRequest.send_request(payload_login)
#                         paasToken = extractor(response_login, "$.data.paasToken")
#                         DataProcess.extra_pool.update({'access_token_login': paasToken})
#
#                         # 如果是多租户，需要再次调用login-tenant.htm接口
#                         # 读取配置文件中的驾校id
#                         tenant_id_conf = ReadFile.read_config("$.tenant_id")
#                         # 第1个租户的驾校id
#                         tenant_id = DataProcess.extract_data("tenant_id")
#                         # 根据tenant_id判断是否是多租户，单租户tenant_id是false, 是多租户才执行该接口
#                         if tenant_id:
#                             # 如果配置了驾校id就用配置的，未配置，就用获取的第1个驾校id
#                             if tenant_id_conf:
#                                 id = tenant_id_conf
#                             else:
#                                 id = tenant_id
#                             payload_login_tenant = {
#                                 'path': '/api/paas/core/user/login-tenant.htm',
#                                 'method': 'post',
#                                 'header': {
#                                     'cookie': "_putk_=" + paasToken
#                                 },
#                                 'data': {
#                                     'tenantId': id
#                                 }
#                             }
#                             BaseRequest.send_request(payload_login_tenant)
#
#                     cookie = "_putk_=" + paasToken
#                     header.update({"cookie": cookie})
#                     # 更新全局header的cookie
#                     DataProcess.header.update({"cookie": cookie})
#
#                 # 更新请求头
#                 payload_grant_access_token.update({'header': header})
#
#                 # 循环3次，避免该接口出现失败情况
#                 for i in range(3):
#
#                     # 5. 获取access_token
#                     response_access_token, _, expect_custom = BaseRequest.send_request(payload_grant_access_token)
#                     # 6. 提取x-puat
#                     x_puat = extractor(response_access_token, '$.data.accessToken')
#                     # 7. 提取过期时间
#                     expiresIn = extractor(response_access_token, "$.data.expiresIn")
#                     # 8. 过期时间处理, 5分钟内可重新获取新token，这里保险起见减4分钟
#                     expiresIn = now + expiresIn - (4 * 60 * 1000)
#                     # 9. 存储x-puat和expiresIn
#                     # 10. 如果提取到x_puat直接结束循环
#                     if x_puat:
#                         DataProcess.extra_pool.update({'x-puat': x_puat})
#                         DataProcess.extra_pool.update({'expiresIn': expiresIn})
#                         break
#                     else:
#                         # 打印错误信息
#                         logger.info("response_access_token" + str(response_access_token))
#
#         except Exception as e:
#             logger.info("x-puat获取异常=======> " + str(e))
#             # 出错就初始化过期时间，0 即为False，下一次判断不成功会重新请求获取access_token
#             DataProcess.extra_pool.update({'expiresIn': 0})
