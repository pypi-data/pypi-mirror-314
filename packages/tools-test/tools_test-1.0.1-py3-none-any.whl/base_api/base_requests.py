# -*- coding:utf-8 -*-
import datetime
import urllib

import requests

from tools import allure_step, allure_title, logger, allure_step_no, updateDict, get_r, form_data_type_judge
from tools.data_process import DataProcess
from tools.read_file import ReadFile


class BaseRequest(object):
    session = None

    @classmethod
    def get_session(cls):
        """
        单例模式保证测试过程中使用的都是一个session对象
        :return:
        """
        if cls.session is None:
            cls.session = requests.Session()
        return cls.session

    @classmethod
    def send_request(cls, case: dict):
        """
        请求参数处理
        :param case: 读取出来的每一行用例内容，可进行解包
        :param env: 环境名称 默认使用config.yaml server下的 test 后面的基准地址
        return: 响应结果， 预期结果
        """

        title = case.get('title')
        header = case.get('header')
        path = case.get('path')
        method = case.get('method')
        file_obj = case.get('files')
        params = case.get('params')
        data = case.get('data')
        jsonData = case.get('json')
        extract = case.get('extract')
        expect = case.get('expect')
        step = case.get('step')
        # 自定义断言
        expect_custom = case.get('expect_custom')

        logger.debug(
            f"\n用例进行处理前数据: \n用例标题：{title} \n   请求头：{header} \n 接口路径：{path} \n  params：{params} \n    data：{data} \n    json：{jsonData} \n    file：{file_obj} \n  提取参数：{extract} \n  预期结果：{expect} \n")
        # 如果不传title，就不设置
        if title is not None:
            # allure报告 用例标题
            allure_title(title)

        if step is not None:
            # 报告右侧步骤中增加步骤
            allure_step_no(f'步骤: {step}')

        # 如果传method，默认为GET请求
        if method is None:
            method = 'GET'

        # 处理url、header、data、files、的前置方法
        url = DataProcess.handle_path(path)
        params = DataProcess.handle_data(params)
        data = DataProcess.handle_data(data)
        jsonData = DataProcess.handle_data(jsonData)

        # 有请求数据再在报告中展示
        requestsData = {}
        if params:
            requestsData.update({'params': params})
        if data:
            # allure报告数据需要
            requestsData.update({'data': data})

            # 再判断data中有没有传"data_type": "multipart/form-data"，如果有就处理为二进制方式提交数据(上传文件方式)
            data_handle = form_data_type_judge(data)
            if isinstance(data_handle, tuple):
                # 如果是元组，说明是这种类型，第一个数据是data转为二进制的数据，第二个是content-type的类型
                data = data_handle[0]
                content_type = data_handle[1]
                if header is None:
                    header = {}
                header.update({"Content-Type": content_type})
            else:
                data = data_handle

        # 请求头处理
        header = DataProcess.handle_header(header)

        if jsonData:
            requestsData.update({'json': jsonData})
        allure_step('请求数据', requestsData)
        allure_step_no(f'请求时间: {datetime.datetime.now()}')
        file = DataProcess.handler_files(file_obj)
        # 发送请求
        response, status_code = cls.send_api(url, method, header, params, data, jsonData, file)
        # 处理请求前extract在报告中展示
        if extract is not None:
            allure_step("请求前extract", extract)
            # 提取参数
            report_extract = DataProcess.handle_extra(extract, response)
            # 设置报告替换的extract
            if report_extract is not None or report_extract != {} or report_extract != "None":
                logger.info("请求后的extract" + str(report_extract))
                allure_step("请求后extract", report_extract)

        logger.info("当前可用参数池" + str(DataProcess.extra_pool))
        allure_step("当前可用参数池", DataProcess.extra_pool)

        # 如果没有填预期结果，默认断言响应码200
        if expect is not None:
            allure_step("请求前expect", expect)
        else:
            allure_step("请求前expect", {"response_code": 200})
            # 未设置expect就断言响应码为200即可
            expect = {status_code: 200}

        if expect_custom is not None:
            allure_step("请求前expect_custom", expect_custom)
        else:
            allure_step("请求前expect_custom", "未设置expect_custom")

        return response, expect, expect_custom

    @classmethod
    def send_api(cls, url, method, header=None, params=None, data=None, jsonData=None, file=None, allure=True) -> tuple:
        """
        封装请求
        :param url: url
        :param method: get、post...
        :param header: 请求头
        :param params: 查询参数类型，明文传输，一般在url?参数名=参数值
        :param data: 一般用于form表单类型参数
        :param jsonData: json类型参数
        :param file: 文件参数
        :return: 响应结果
        """
        session = cls.get_session()

        res = session.request(method, url, params=params, data=data, json=jsonData, files=file, headers=header)
        try:
            response = res.json()
        except Exception:
            # 这里return 二进制内容，文件下载需要接收
            response = res.content
        if allure:
            allure_step_no(f'响应耗时(s): {res.elapsed.total_seconds()}')

        if isinstance(response, bytes):
            if "html" in str(response):
                response_result = res.text
            else:
                response_result = "响应结果为二进制文件"
        else:
            response_result = response

        if allure:
            allure_step("响应结果", response_result)
        logger.info(
            f'\n最终请求地址：{urllib.parse.unquote(res.url)}\n   请求方法：{method}\n    请求头：{res.request.headers}\n   params：{params}\n     data：{data}\n     json：{jsonData}\n     file：{file}\n  响应数据：{response_result}')

        # 返回响应和响应码
        return response, res.status_code
