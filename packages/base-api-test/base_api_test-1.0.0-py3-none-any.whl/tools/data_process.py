# coding:utf-8
import copy
import hashlib
import json
import os
import random
import re
import time
import jsonpath
import magic  # 识别文件库
import pdfplumber
import requests
import xlrd
from docx import Document

from tools import logger, extractor, rep_expr, allure_step, allure_step_no
from tools.read_file import ReadFile

class DataProcess:
    """
    数据处理
    """
    # 存放提取参数的池子
    # accessToken x_puat和expiresIn过期时间默认存储
    # extra_pool = {"expiresIn": 0, "x-puat": '', 'grant_access_token_count': 0, "relations": []}
    extra_pool = {}
    header = ReadFile.read_config('$.request_headers')

    @classmethod
    def handle_path(cls, path) -> str:
        """
        path处理
        :param path: 带提取表达式的字符串 /${userId}/abcd/1234
        上述内容表示，从extra_pool字典里取到key为userId 对应的值，假设是001, 最终提取结果如下：/001/abcd/1234
        :return: 提取后的路径
        """

        path = str(path)
        env_Path = None

        if path[0:4] == 'http':
            # 如果就是http开头的，就不拼接url了
            allure_step_no(f'请求地址: {path}')
            return path

        # 获取最终环境的路径
        envPath = ReadFile.read_config('$.hosts.jiaxiao-paas')

        path = rep_expr(path, cls.extra_pool)
        if envPath is None or envPath == 'None' or envPath == False:
            allure_step_no(f'请求地址: {path}')
            return path
        else:
            url = envPath + path
            allure_step_no(f'请求地址: {url}')
            return url

    @classmethod
    def handle_header(cls, header) -> dict:
        """
        处理header， 将用例中的表达式处理后 追加到基础header中
        :param header: 用例中的header
        :return: None
        """

        header_copy = copy.deepcopy(cls.header)
        try:
            # 如果配置了cookies就更新
            cookie = ReadFile.read_config('$.cookie')
            if cookie != False:
                header_copy.update({"cookie": cookie})
        except Exception:
            # 如果没配置cookie，读取不到就跳过
            pass

        # 传的请求头不为空就更新合并，如果有需要替换的数据就handle_data处理
        if header is not None:
            header_copy.update(cls.handle_data(header))

        # 驾校直连才需要x-puat，配置access_token是才在header添加
        token_conig = ReadFile.read_config("$.access_token")
        if token_conig == True:
            header_copy.update({'x-puat': cls.extra_pool['x-puat']})

        allure_step('请求头', header_copy)
        return header_copy

    @classmethod
    def handler_files(cls, file_obj):
        """
        文件上传处理
        :param file_obj: 文件路径
        单文件：{"fileName":path}
        多文件：[{"fileName":[path1,path2]}]
        解释：fileName根据抓包获取对应name,path是文件路径，多文件传列表即可
        :return: None
        """

        files = None

        if file_obj is not None:

            for name, path in file_obj.items():
                # 如果传多个文件，处理如下
                if isinstance(path, list):
                    fileList = []
                    for p in path:
                        filename = os.path.basename(p)
                        filetype = magic.from_file(p, mime=True)
                        fileList.append((filename, open(p, 'rb'), filetype))
                    files = {'name': fileList}
                else:
                    # 单文件上传处理：
                    # 根据文件路径获取文件名称
                    filename = os.path.basename(path)
                    filetype = magic.from_file(path, mime=True)
                    # 第一个参数name是抓包得到的上传文件的name参数；元组中的参数分别是：文件名称、文件路径、文件类型。
                    files = {name: (filename, open(path, 'rb'), filetype)}
            allure_step('上传文件', str(files))
            return files

    @classmethod
    def handle_data(cls, variable):
        """
        请求数据处理，header、params、data、json,从全局池替换
        :param variable: 需要处理的数据
        :return: 处理后的数据
        """

        if variable is not None:
            data = rep_expr(variable, cls.extra_pool)
            return data

    @classmethod
    def handle_extra(cls, extra, response: dict):
        """
        处理提取参数
        :param extra: 提取参数栏内容，需要是 {"参数名": "jsonPath提取式"} 可以有多个
        :param response: 当前用例的响应结果字典
        :return:
        """

        if extra is not None:
            for k, v in extra.items():
                # 如果value的开头是$.开头的就提取一下，不然直接更新
                if isinstance(v, str) and "$." in v:
                    if v[-2:] == "()":
                        after_method_name = v.split(".")[-1][:-2]
                        v = v.split(".")[:-1]
                        v = '.'.join(v)
                        v = extractor(response, v)
                        try:
                            # 解决jsonpath提取只有一条数据时，框架会自动提取数据，这里再转为list
                            if after_method_name in ["max", "min", "avg", "sum", "len"] and not isinstance(v, list):
                                v = [v]
                            v = eval(f"{after_method_name}({v})")
                        except Exception:
                            v = eval(f"cls.{after_method_name}({v})")
                    else:
                        # jsonpath表达式最后没有.xx()就直接提取
                        v = extractor(response, v)

                # 更新字典
                cls.extra_pool.update({k: v})
                extra.update({k: v})
                logger.info(f'加入依赖字典,key: {k}, 对应value: {v}')

            return extra

    @classmethod
    def assert_result(cls, response: dict, expect: dict):
        """
        预期结果实际结果断言方法
        注意：如果断言False，False==False成功。提取不到的时候也返回False，也算成功。支持2种场景
        :param response: 实际响应结果
        :param expect: 预期和实际结果的表达式，从全局或实际响应中提取对比
        :return: True or False
        """
        expect = rep_expr(expect, cls.extra_pool)
        index = 0
        for k, v in expect.items():
            # 获取需要断言的实际结果部分,True表示在断言的时候使用，如果提取不到的时候会返回False而不是json表达式
            # k，v都在响应中提取下数据
            # 判断是否有后置的.sum等函数要处理
            if isinstance(k, str) and "$." in k:
                # 如果最后有()表示提取后有需要执行的函数
                if k[-2:] == "()":
                    # 去掉()拿到方法名
                    after_method_k = k.split(".")[-1][:-2]
                    # 去除最后的方法，再拼接jsonpath表达式
                    k = k.split(".")[:-1]
                    k = '.'.join(k)
                    k = extractor(response, k)
                    if isinstance(k, str):
                        k = f"'{k}'"
                    try:
                        if after_method_k in ["max", "min", "avg", "sum", "len"] and not isinstance(k, list):
                            k = [k]
                        k = eval(f"{after_method_k}({k})")
                    except Exception:
                        k = eval(f"cls.{after_method_k}({k})")
                else:
                    # jsonpath表达式最后没有.xx()就直接提取
                    k = extractor(response, k)

            if isinstance(v, str) and "$." in v:
                # 如果最后有()表示提取后有需要执行的函数
                if v[-2:] == "()":
                    # 去掉()拿到方法名
                    after_method_value = v.split(".")[-1][:-2]
                    v = v.split(".")[:-1]
                    v = '.'.join(v)
                    v = extractor(response, v)
                    if isinstance(v, str):
                        v = f"'{v}'"
                    try:
                        # 如果这个内置方法找不到就拼接cls.找自定义的方法
                        if after_method_value in ["max", "min", "avg", "sum", "len"] and not isinstance(k, list):
                            v = [v]
                        v = eval(f"{after_method_value}({v})")
                    except Exception:
                        v = eval(f"cls.{after_method_value}({v})")
                else:
                    v = extractor(response, v)

            # 如果预期和实际结果是字符串的话，加上引号
            if isinstance(k, str):
                k = f"'{k}'"
            if isinstance(v, str):
                v = f"'{v}'"
            # 如果预期和实际都是list，用sorted防止为list时，服务器返回数据乱序断言会失败
            if isinstance(v, list) and isinstance(k, list):
                k = sorted(k)
                v = sorted(v)

            index += 1
            logger.info(
                f'第{index}个断言,{k} | {v} \n断言结果 {k == v}')
            allure_step(f'第{index}个断言', f'{k} == {v}')
            try:
                assert k == v
            except AssertionError:
                raise AssertionError(
                    f'第{index}个断言失败 -|- {k} ||  {v}')

    @classmethod
    def extract_data(cls, key: str):
        """
        从参数池中提取数据
        :param key: jsonPath表达式
        :return: 提取到的数据，jsonpath提取不到返回False，其它方法返回None
        """
        if key[0:2] == "$.":
            data = jsonpath.jsonpath(cls.extra_pool, key)
        else:
            data = cls.extra_pool.get(key)
            if data is None:
                logger.error(f'{key} - 提取不到内容，{key}提取结果为：None')
        return data

    @classmethod
    def setPool(cls, dic):
        """
        存储数据到全局参数池
        :param dic: 需要设置的数据
        :return: None
        """
        DataProcess.extra_pool.update(dic)

    @classmethod
    def relationCase(cls, relations):
        # 当前时间格式化
        fmt_time = time.strftime('%Y%m%d%H%m%S', time.localtime())
        ENCRYPT_KEY = "d1d1a8b60f2a4a72a69720655bcfa854"

        s = ENCRYPT_KEY + str(fmt_time)

        # md5加密key和格式化时间
        hl = hashlib.md5()
        # 必须encode编码
        hl.update(s.encode(encoding="utf-8"))
        # 获取加密后的字符串
        # hl.hexdigest()

        url = "https://auto-testcase.kakamobi.cn/api/external/test-case/update-complete-status.htm"

        params = {
            "time": fmt_time,
            "sign": hl.hexdigest()
        }

        response = requests.post(url=url, json=relations, params=params)

        logger.info("关联用例id relations个数为：%s" % len(relations))

        try:
            response_json = response.json()
            if response_json.get("success") == True:
                logger.info("关联用例成功！")
            else:
                logger.error("关联用例失败, err: %s" % response.text)
                # 需要查看id时，打开下面注释
                # logger.info("请求数据是：%s" % str(relations))

        except Exception:
            logger.error("关联用例失败，err：%s" % response.text)

    @classmethod
    def expect_custom_handle(cls, response, expect_data):
        func = expect_data.get("func")
        if func is None:
            # 没有func表示不是自定义方法，通过关键字方式断言
            expect = expect_data.get("expect")
            keyword = expect_data.get("keyword")
            actual = expect_data.get("actual")

            if keyword is None:
                # 说明关键字错误，直接返回False
                return "相关参数错误,请检查", False

            # 响应中替换
            if isinstance(expect, str) and "$." in expect:
                jsonpath_result_expect = jsonpath.jsonpath(response, expect)
                # 提取不到会返回false，提取到就替换expect
                if jsonpath_result_expect:
                    if isinstance(jsonpath_result_expect, list):
                        if len(jsonpath_result_expect) > 1:
                            expect = jsonpath_result_expect
                        else:
                            expect = jsonpath_result_expect[0]

            if isinstance(actual, str) and "$." in actual:
                jsonpath_result_actual = jsonpath.jsonpath(response, actual)
                # 提取不到会返回false，提取到就替换expect
                if jsonpath_result_actual:
                    if isinstance(jsonpath_result_actual, list):
                        # 如果是list返回list，如果只有1条数据，返回数据本身
                        if len(jsonpath_result_actual) > 1:
                            actual = jsonpath_result_actual
                        else:
                            actual = jsonpath_result_actual[0]

            # 全局参数池替换(因为先处理了$.格式的，这里就不用排除$.格式)
            if isinstance(expect, str) and "$" in expect:
                pool_get_expect = cls.extra_pool.get(expect[1:])
                if pool_get_expect is not None:
                    expect = pool_get_expect

            if isinstance(actual, str) and "$" in actual:
                pool_get_actual = cls.extra_pool.get(actual[1:])
                if pool_get_actual is not None:
                    actual = pool_get_actual

            # 如果数据是list或元组排序一下
            if isinstance(expect, list) or isinstance(expect, tuple):
                expect = sorted(expect)

            if isinstance(actual, list) or isinstance(actual, tuple):
                actual = sorted(actual)

            # 替换完后再判断expect和actual是否是字符串，是的话需要加个引号处理下
            if isinstance(expect, str):
                expect = f'"""{expect}"""'
            if isinstance(actual, str):
                actual = f'"""{actual}"""'

            expression = f"{expect} {keyword} {actual}"

            try:
                assert_result = eval(expression)
                return expression, assert_result
            except Exception:
                # 说明类型不匹配或其它错误，直接False
                return expression, False
        else:
            # 表示是自定义方法，通过该方式断言
            func_name = func.get("name")
            func_params = func.get("params")
            # 处理参数
            if isinstance(func_params, str):
                if "$." in func_params:
                    if func_params[-2:] == "()":
                        # 去掉()拿到方法名
                        after_method = func_params.split(".")[-1][:-2]
                        func_params = func_params.split(".")[:-1]
                        func_params = '.'.join(func_params)

                        func_params = extractor(response, func_params)
                        if isinstance(func_params, str):
                            func_params = f"'{func_params}'"
                        try:
                            if after_method in ["max", "min", "avg", "sum", "len"] and not isinstance(func_params,
                                                                                                      list):
                                func_params = [func_params]
                            func_params = eval(f"{after_method}({func_params})")
                        except Exception:
                            func_params = eval(f"cls.{after_method}({func_params})")

                else:
                    func_params = extractor(response, func_params)

                if isinstance(func_params, str) and "$" in func_params:
                    get_pool_func_param = cls.extra_pool.get(func_params[1:])
                    if get_pool_func_param is not None:
                        func_params = get_pool_func_param

            if isinstance(func_params, list):
                for i in range(len(func_params)):
                    param = func_params[i]

                    if isinstance(param, str) and "$." in param:
                        if param[-2:] == "()":
                            # 去掉()拿到方法名
                            after_method = param.split(".")[-1][:-2]
                            param = param.split(".")[:-1]
                            param = '.'.join(param)

                            param = extractor(response, param)
                            if isinstance(param, str):
                                param = f"'{param}'"
                            try:
                                if after_method in ["max", "min", "avg", "sum", "len"] and not isinstance(param,
                                                                                                          list):
                                    param = [param]
                                param = eval(f"{after_method}({param})")
                            except Exception:
                                param = eval(f"cls.{after_method}({param})")

                        else:
                            param = extractor(response, param)

                    if isinstance(param, str) and "$" in param:
                        get_pool_func_param = cls.extra_pool.get(param[1:])
                        if get_pool_func_param is not None:
                            param = get_pool_func_param
                    func_params[i] = param

            expression = f"cls.{func_name}({func_params})"
            try:
                assert_func_result = eval(expression)
                return expression[4:], assert_func_result
            except Exception:
                return expression[4:], False

    @classmethod
    def expect_keyword(cls, response, expect_data):
        if isinstance(expect_data, list):
            for i in range(len(expect_data)):
                expression, result = cls.expect_custom_handle(response, expect_data[i])
                logger.info(
                    f'自定义断言：第{i + 1}个自定义断言：{expression} \n断言结果 {result}')
                allure_step(f'第{i + 1}个自定义断言', expression)
                if result != True:
                    raise AssertionError(f'自定义断言：第{i + 1}个自定义断言失败：{expression} \n断言结果 {result}')

        else:
            expression, result = cls.expect_custom_handle(response, expect_data)
            logger.info(f'自定义断言表达式：{expression} \n断言结果 {result}')
            allure_step(f'自定义断言', expression)
            if result != True:
                raise AssertionError(f'自定义断言：自定义断言失败：{expression} \n断言结果 {result}')

    # @classmethod
    # def excel_contain_assert(cls, params):
    #     """
    #     params: ["files/download/油气耗导出.xlsx", "$plateNo", "1234"]
    #     会断言 $plateNo和"1234"是否都包含在files/download/油气耗导出.xlsx中，$plateNo会从全局参数池提取对比
    #     如果还有多个需要断言的参数，继续往后增加即可
    #     """
    #     filename = params[0]
    #     expects = params[1:]
    #     book = xlrd.open_workbook(filename)
    #     sh = book.sheet_by_index(0)
    #     all_rows = []
    #     all_data = []
    #
    #     for rx in range(sh.nrows):
    #         all_rows.append(sh.row(rx))
    #
    #     # 遍历每一行数据并存储
    #     for rows in all_rows:
    #         for one_data in rows:
    #             all_data.append(one_data)
    #
    #     for i in range(len(expects)):
    #         isIn = False
    #         for data in all_data:
    #             if expects[i] in str(data):
    #                 isIn = True
    #                 break
    #
    #         if not isIn:
    #             return False
    #
    #     # 所有数据遍历完都没返回就说明都包含，返回True
    #     return True

    @classmethod
    def excel_contain_assert(cls, params):
        """
        params: ["files/download/油气耗导出.xlsx", "$plateNo", "1234"]
        会断言 $plateNo和"1234"是否都包含在files/download/油气耗导出.xlsx中，$plateNo会从全局参数池提取对比
        如果还有多个需要断言的参数，继续往后增加即可
        """

        try:
            filename = params[0]
            expects = params[1:]
            suffix = filename.split(".")[1]
            all_data = []
            if suffix == "xlsx" or suffix == "xls":
                book = xlrd.open_workbook(filename)
                sh = book.sheet_by_index(0)
                all_rows = []

                for rx in range(sh.nrows):
                    all_rows.append(sh.row(rx))

                # 遍历每一行数据并存储
                for rows in all_rows:
                    for one_data in rows:
                        all_data.append(one_data)

            elif suffix == "docx":
                # world处理
                doc = Document(filename)
                docx_str = ''
                for i in doc.paragraphs:
                    # style.name是样式，text是内容
                    # print(i.style.name,i.text)
                    # 存储内容到变量中
                    docx_str += i.text + "\n"
                all_data = docx_str

            elif suffix == "pdf":
                # pdf文件处理
                # 打开PDF文件
                pdf = pdfplumber.open(filename)
                # 通过pages属性获取所有页的信息，此时pages是一个列表
                pages = pdf.pages

                text_all = []
                for page in pages:
                    # 用extract_text()函数获取每页文本内容
                    text = page.extract_text()
                    text_all.append(text)

                text_all = "".join(text_all)
                # print(text_all)

                pdf.close()
                all_data = text_all

            else:
                return False

            # 断言预期结果是否都包含在alldata中
            for i in range(len(expects)):
                isIn = False
                if isinstance(all_data, list):
                    for data in all_data:
                        if expects[i] in str(data):
                            isIn = True
                            break

                    # 2层for循环，所以判断isIn是否为真
                    if not isIn:
                        # 断言失败时打印出文件中内容
                        allure_step("文件内容", all_data)
                        return False

                elif isinstance(all_data, str):
                    # str类型是word和pdf文件生成的数据，文件内容组合为一个大的字符串
                    if expects[i] in all_data:
                        continue
                    else:
                        # 断言失败前打印文件内容
                        allure_step("文件内容", all_data)
                        return False

            # 所有断言验证通过才会走到这，所以直接返回True
            return True
        except Exception as e:
            allure_step("excel_contain_assert错误", str(e))

    @classmethod
    def reg(cls, params):
        # 接收第一个参数jsonpath表达式，第二个参数正则表达式，然后再提取需要的数据
        jsonpath_ex, re_ex, actual = params
        try:
            expect = re.search(re_ex, jsonpath_ex).group(1)
            assert expect == actual
            return True
        except Exception:
            return False

    @classmethod
    def add(cls, params):
        # 断言预期结果+1 == 实际结果
        actual, expect = params

        if not isinstance(actual, int) or not isinstance(expect, int):
            # 不是int直接返回False
            return False

        return expect + 1 == actual

    @classmethod
    def reduce(cls, params):
        actual, expect = params

        if not isinstance(actual, int) or not isinstance(expect, int):
            # 不是int直接返回False
            return False

        return expect - 1 == actual

    @classmethod
    def update_time(cls, times):
        # 时间戳以毫秒为单位计算，差值不超过1秒
        return abs(abs(int(times[0]) - int(times[1]))) < 1000

    @classmethod
    def actual_only_contain_expect(cls, params):
        # 用于筛选，检查是否只含有某个元素
        expect = params[0]
        actual = params[1]
        if isinstance(actual, list):
            while expect in actual:
                actual.remove(expect)
            if len(actual) == 0:
                return True
            else:
                return False
        elif isinstance(actual, str):
            return actual == expect
        elif actual is False:
            return True
        else:
            return False

    @classmethod
    def expected_and_actual_match(cls, params):
        # 用于模拟匹配，预期与实际匹配,仅限字符串格式数据
        expect = params[0]
        actual = params[1]
        if isinstance(actual, list):
            for value in actual:
                if value.find(expect) == -1:
                    return False
            return True
        elif isinstance(actual, str):
            if actual.find(expect) == -1:
                return False
            else:
                return True
        elif actual is False:
            return True
        else:
            return False

    @classmethod
    def expect_in_or_equal_actua(cls, params):
        # 期望在实际包含或等于期望
        expect = params[0]
        actual = params[1]
        if isinstance(actual, list):
            return expect in actual
        else:
            return str(expect) == str(actual)

    @classmethod
    def expect_not_in_or_not_equal_actua(cls, params):
        # 期望不在实际包含或不等于期望
        expect = params[0]
        actual = params[1]
        if isinstance(actual, list):
            return expect not in actual
        else:
            return str(expect) != str(actual)

    @classmethod
    def str_list_sort_intercept(cls, params):
        """
        actual：实际提取的结果
        expect：预期结果
        transformation_int：数据是否需要转为int
        atypism：预期结果长度是否小于实际结果
        """
        try:
            actual, expect, transformation_int, atypism = params
        except Exception:
            return False

        if not actual or not expect:
            return False

        actualList = sorted(actual.split(","))[:len(actual)]

        if transformation_int:
            tempList = []
            for i in actualList:
                tempList.append(int(i))
            actualList = sorted(tempList)

        expect = sorted(expect)

        # 设置allure报告
        allure_step('actual', {"actual": actualList})
        allure_step('expect', {"expect": expect})

        # 如果是预期结果数据较多，需要在报告展示其余的数据情况
        if atypism:
            # 得到2个列表不同的数据，写入报告
            set_actual = set(actualList)
            set_expect = set(expect)
            # 利用交差补集得到不重复的其余数据
            surplus_list = set_actual.symmetric_difference(set_expect)
            # 日志和报告中显示其余的id
            logger.info("其余的id为：" + str(list(surplus_list)))
            allure_step_no(f'其余的id为：: {list(surplus_list)}')

            # 直接判断预期结果是否为实际结果子集即可，是返回True
            return set_actual >= set_expect

        else:
            if actualList == expect:
                return True
            else:
                return False

    @classmethod
    def str_list_sort_intercept_list(cls, params):
        """
        actual：实际提取的结果
        expect：预期结果
        transformation_int：数据是否需要转为int
        atypism：预期结果长度是否小于实际结果
        """
        try:
            actual, expect, transformation_int, atypism = params
        except Exception:
            return False

        if not actual or not expect:
            return False
        # 多个列表合并成一个列表
        actual = actual[0] + actual[1] + actual[2] + actual[3] + actual[4]
        actualList = sorted(actual)

        if transformation_int:
            tempList = []
            for i in actualList:
                tempList.append(int(i))
            actualList = sorted(tempList)

        expect = sorted(expect)

        # 设置allure报告
        allure_step('actual', {"actual": actualList})
        allure_step('expect', {"expect": expect})

        if atypism:
            # 得到2个列表不同的数据，写入报告
            set_actual = set(actualList)
            set_expect = set(expect)
            # 利用交差补集得到不重复的其余数据
            surplus_list = set_actual.symmetric_difference(set_expect)
            # 日志和报告中显示其余的id
            logger.info("其余的id为：" + str(list(surplus_list)))
            allure_step_no(f'其余的id为: {list(surplus_list)}')

            # 直接判断预期结果是否为实际结果子集即可，是返回True
            return set_actual >= set_expect
        else:
            # 得到2个列表不同的数据，写入报告
            set_actual = set(actualList)
            set_expect = set(expect)
            # 利用交差补集得到不重复的其余数据
            surplus_list = set_actual.symmetric_difference(set_expect)
            # 日志和报告中显示其余的id
            logger.info("其余的id为：" + str(list(surplus_list)))
            allure_step_no(f'其余的id为: {list(surplus_list)}')

            # 直接判断实际结果是否为预期结果子集即可，是返回True
            return set_actual <= set_expect

    @classmethod
    def other_type_data_extract(cls, response, start_boundary, end_boundary, ex, key):
        """
        response: 响应的二进制数据
        start_boundary: 二进制转为str后还需要切片处理的起始值
        end_boundary：结束值
        ex：jsonpath表达式
        key：保存在全局参数池中的key
        """
        # 二进制转字符串
        str_res = response.decode(encoding="utf-8")
        # 截取需要的部分，转为字典，再通过jsonpath提取想要的数据，存储到参数池
        str_res = json.loads(str_res[start_boundary: end_boundary])
        # 提取相应的值
        codes = jsonpath.jsonpath(str_res, ex)
        # 写入全局参数池
        DataProcess.setPool({key: codes})

    @classmethod
    def dic_in_dic(cls, params):
        """
        断言预期结果字典是否包含于实际结果字典中
        :param params: 接收list，其中有2个参数，第1个为预期结果，第2个为实际结果
        :return:
        """
        expect = params[0]
        actual = params[1]

        # 转为集合
        expect = set(expect.items())
        actual = set(actual.items())

        # 判断实际结果是否是预期结果的父集，也就是判断预期结果字典是否包含在实际结果
        if actual.issuperset(expect):
            return True
        else:
            return False

    @classmethod
    def first(cls, li):
        # list中第1条数据
        if not isinstance(li, list):
            li = [li]
        return li[0]

    @classmethod
    def end(cls, li):
        # list中最后1条数据
        if not isinstance(li, list):
            li = [li]
        return li[-1]

    @classmethod
    def choice(cls, li):
        if not isinstance(li, list):
            li = [li]
        # list中随机1条数据
        return random.choice(li)
