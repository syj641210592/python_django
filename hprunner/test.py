from httprunner.api import HttpRunner
from httprunner.report import gen_html_report

# failfast当用例执行失败之后,会自动暂停,默认为False,可以不写
# save_tests可以以json格式在logs文件夹下生成测试用例转换成httprunner可识别的数据结构解析步骤
httprun = HttpRunner(failfast=False, log_level='INFO', save_tests=True)
# 创建httprun运行器
httprun.run(
    r"F:\Python\Python_Project\python_test_developer\python_test_developer_django\hprunner\testsuites\test_developer_testsuite.yml"
)
gen_html_report(
    httprun._summary,
    report_dir=
    r"F:\Python\Python_Project\python_test_developer\python_test_developer_django\hprunner\reports"
)
# print(httprun.content)
