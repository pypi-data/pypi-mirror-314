import os
import unittest
from datetime import datetime

from airtestProject.airtest.utils.logwraper import AirtestLogger

from airtestProject.manager.DeviceManager import DeviceManager
from airtestProject.manager.LogManager import LogManager


class TestCaseManager:
    def __init__(self, project):
        """
        初始化测试用例管理器
        :param project:
        """
        self.absolute_log_path = None
        logfile = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\log\\'+project+'\\log.txt'
        self.log_manager = LogManager(logfile=logfile, project=project)
        self.device_manager = DeviceManager(self.log_manager)
        # self.log_manager.log_step('连接设备')
        # todo: 这里的设备ID要根据实际情况修改
        self.app_start_case = self.device_manager.auto_setup()
        self.execution_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.executed_test_cases = []
        self.case_path = None
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def load_tests_from_directory(self, directory, project):
        """
        加载测试套件
        :param directory:
        :return:
        """
        test_loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        base_module = f'airtestProjects.case.{project}'
        for filename in os.listdir(directory):
            if filename.endswith('.py'):
                module_name = filename[:-3]
                module_path = f"{base_module}.{module_name}"
                module = __import__(module_path, fromlist=['*'])
                test_class = getattr(module, module_name)
                test_class.setup(self.log_manager)
                loaded_tests = test_loader.loadTestsFromModule(module)
                suite.addTests(loaded_tests)
        return suite

    def run_tests(self, project):
        """
        运行测试用例，加载cases下面的项目的所有用例，并且执行
        :param project:
        :return:
        """
        # =====================================
        # 测试调用AirtestLogger的log来生成日志
        # log_path = self.current_directory + '\\log\\' + project + '\\log.txt'
        if not os.path.exists(self.project_root + '\\log\\' + project):
            os.makedirs(self.project_root + '\\log\\' + project)
        log_file = self.project_root + '\\log\\' + project + '\\log.txt'
        airtest_log = AirtestLogger(None)
        airtest_log.set_logfile(log_file)
        # =====================================

        test_suite = self.load_tests_from_directory(self.project_root + '/case/' + project, project)
        for suite in test_suite:
            for test_case in suite:
                test_result = {'name': test_case.id(), 'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                result = unittest.TextTestRunner().run(test_case)
                test_result['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if result.wasSuccessful():
                    self.log_manager.log_step(f"测试通过： {test_case}")
                    test_result['status'] = "Passed"
                else:
                    self.log_manager.log_error(f"测试不通过：{test_case}")
                    test_result['status'] = "Failed"
                self.executed_test_cases.append(test_result)

        # 生成测试报告
        report_path = self.project_root + f"\\report\\{project}_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.html"
        self.absolute_log_path = self.current_directory + '\\log\\all.txt'
        self.generate_report(output=report_path, project=project)

    def generate_report(self, output, project):
        """
         生成测试报告，包括设备信息、用例执行情况、执行日期等
        :param output:报告输出路径
        :param project:项目名称
        :return:NONE
        """
        self.log_manager.close_logger()
        # log根目录
        log_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # log的路径
        log_path = os.path.join(log_root, 'log\\' + project)
        # log文件
        log_file = os.path.join(log_path, f'log.txt')
        from airtestProject.manager.ReportManager import simple_report
        # from airtest.report.report import simple_report
        # 生成报告
        simple_report(__file__, logpath=log_path, logfile=log_file, output=output, project=project)


if __name__ == '__main__':
    project = 'zhange'
    test_case_manager = TestCaseManager(project=project)
    test_case_manager.run_tests(project)
