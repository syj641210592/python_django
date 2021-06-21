from httprunner.api import HttpRunner
from httprunner.report import gen_html_report

# failfast当用例执行失败之后,会自动暂停,默认为False,可以不写
httprun = HttpRunner(failfast=False, log_level='INFO')
# 创建httprun运行器
httprun.run(
    r"F:\Python\Python_Project\python_test_developer\python_test_developer_django\hprunner\testsuites\test_developer_testsuite.yml"
)
gen_html_report(httprun._summary, report_dir=r"F:\Python\Python_Project\python_test_developer\python_test_developer_django\hprunner\reports")
# print(httprun.content)
