import json
import os
import yaml
from datetime import datetime

from django.conf import settings
from httprunner.task import HttpRunner
# from httprunner.api import HttpRunner  # 2.5.7版本
# from httprunner.report import gen_html_report  # 2.5.7版本
from rest_framework.response import Response

from projects.models import ProjectsModel
from configures.models import ConfiguresModel
from debugtalks.models import DebugTalksModel
from testcases.models import TestcasesModel
from envs.models import EnvsModel
from reports.models import ReportsModel


def http_run_env_get(obj):
    path_dict = {}
    # 1、对请求参数env_id进行反序列化校验
    instance = obj.get_object()
    serializer = obj.get_serializer(data=obj.request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    # 2、取出校验后的env_id, 并获得env_id对应的数据
    env_id = validated_data.get("env_id")
    env_instance = EnvsModel.objects.get(id=env_id)
    base_url = env_instance.base_url if env_instance.base_url else ""
    path_dict.update({"instance": instance, "base_url": base_url})
    return path_dict


def http_testcasedir_create(path_dict):
    """创建http项目目录,接口目录和debugtalks文件"""
    # 3、创建以时间戳命名的httprunner项目目录
    dirname = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    dirpath = os.path.join(settings.BASE_DIR, "httprunner", dirname)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    path_dict.update({"dirname": dirname, "dirpath": dirpath})
    # 4、创建以项目名命名的目录
    ht_pro_name = path_dict["instance"].interface.project.name
    ht_pro_path = os.path.join(dirpath, ht_pro_name)
    if not os.path.exists(ht_pro_path):
        os.makedirs(ht_pro_path)
    path_dict.update({"ht_pro_name": ht_pro_name, "ht_pro_path": ht_pro_path})
    # 5、生成debugtalks.py
    debugtalks_file_name = "debugtalk.py"
    debugtalks_file_path = os.path.join(ht_pro_path, debugtalks_file_name)
    debugtalks_instance = DebugTalksModel.objects.get(
        project_id=path_dict["instance"].interface.project.id)
    with open(debugtalks_file_path, "w", encoding='utf-8') as file:
        file.write(debugtalks_instance.debugtalk)
    path_dict.update({
        "debugtalks_file_name": debugtalks_file_name,
        "debugtalks_file_path": debugtalks_file_path
    })
    # 6、创建接口测试用例文件夹
    testcase_dir_name = path_dict["instance"].interface.name
    testcase_dir_path = os.path.join(ht_pro_path, testcase_dir_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
    path_dict.update({
        "testcase_dir_name": testcase_dir_name,
        "testcase_dir_path": testcase_dir_path
    })
    return path_dict


def http_testreportdir_create(path_dict):
    """创建http项目目录和用例文件"""
    # 创建report文件夹
    report_path = os.path.join(path_dict["ht_pro_path"], "report")
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    path_dict.update({"report_path": report_path})
    return path_dict


def http_testcasefile_create(path_dict):
    """创建测试用例yaml文件"""
    # 创建接口测试用例文件[conf, 前置test, test]
    testcase_data = []
    include = json.loads(path_dict["instance"].include)
    # 添加config数据
    config_id = include.get("config")
    if config_id:
        config_instance = ConfiguresModel.objects.get(
            interface__id=path_dict["instance"].interface.id)
        config_data = json.loads(config_instance.request)
        config_data["config"]["request"]["base_url"] = path_dict["base_url"]
    else:
        config_data = {
            "config": {
                "name": path_dict["testcase_dir_name"],
                "request": {
                    "headers": {
                        "Accept": "application/json",
                        "User-Agent": "Mozilla/5.0"
                    },
                    "base_url": path_dict["base_url"]
                }
            }
        }
    testcase_data.append(config_data)
    # 添加前置test数据
    setup_tests_id = include.get("testcases")
    if setup_tests_id:
        for setup_test_id in setup_tests_id:
            setup_test_instance = TestcasesModel.objects.get(id=setup_test_id)
            setup_test_data = json.loads(setup_test_instance.request)
            testcase_data.append(setup_test_data)
    # 添加test数据
    testcase_data.append(json.loads(path_dict["instance"].request))
    # 创建yaml文件
    testcase_file_name = path_dict["instance"].name + ".yaml"
    testcase_file_path = os.path.join(path_dict["testcase_dir_path"],
                                      testcase_file_name)
    with open(testcase_file_path, "w", encoding='utf-8') as file:
        yaml.dump(testcase_data, file, allow_unicode=True)
    path_dict.update({
        "testcase_file_name": testcase_file_name,
        "testcase_file_path": testcase_file_path
    })
    return path_dict


def http_testinterfacesfile_create(path_dict):
    """创建测试接口下的测试用例yaml文件"""
    for instance in path_dict["querysets"]:
        path_dict["instance"] = instance
        path_dict = http_testcasefile_create(path_dict)


def http_runner(path_dict):
    try:
        # failfast当用例执行失败之后,会自动暂停,默认为False,可以不写
        # save_tests可以以json格式在logs文件夹下生成测试用例转换成httprunner可识别的数据结构解析步骤
        # httprun = HttpRunner(failfast=False, log_level='INFO', save_tests=True)  # 2.5.7版本
        httprun = HttpRunner()  # 1.5.8版本
        # 创建httprun运行器
        httprun.run(path_dict["testcase_dir_path"])
        # gen_html_report(httprun._summary, report_dir=report_path)  # 1.5.8版本
        return report_instance_create(httprun, path_dict["testcase_dir_name"])
    except Exception:
        return Response({'msg': '用例执行失败', 'status': 1}, status=400)


def http_run(path_dict):
    path_dict = http_testcasedir_create(path_dict)
    path_dict = http_testreportdir_create(path_dict)
    for instance in path_dict["querysets"]:
        path_dict["instance"] = instance
        path_dict = http_testcasefile_create(path_dict)
    res = http_runner(path_dict)
    return res


def report_instance_create(httprun, report_name):
    """
    创建测试报告数据库数据
    """
    report_name = report_name

    time_stamp = int(httprun.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime(
        '%Y-%m-%d %H:%M:%S')
    httprun.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    httprun.summary['time']['duration'] = round(
        httprun.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    httprun.summary['html_report_name'] = report_name

    for item in httprun.summary['details']:
        try:
            for record in item['records']:
                record['meta_data']['response']['content'] = record['meta_data']['response']['content']. \
                    decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(
                    record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['request'][
                        'body'] = request_body.decode('utf-8')
        except Exception:
            continue

    try:
        summary = json.dumps(httprun.summary, ensure_ascii=False)
    except Exception:
        return Response({'msg': '用例数据转化有误'}, status=400)

    report_name = report_name + '_' + datetime.strftime(
        datetime.now(), '%Y%m%d%H%M%S')
    report_path = httprun.gen_html_report(html_report_name=report_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': httprun.summary.get('success'),
        'success': httprun.summary.get('stat').get('successes'),
        'count': httprun.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
    }
    report_obj = ReportsModel.objects.create(**test_report)
    return Response({'id': report_obj.id})
