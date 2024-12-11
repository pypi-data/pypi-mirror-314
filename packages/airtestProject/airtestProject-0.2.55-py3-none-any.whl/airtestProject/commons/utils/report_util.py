import json
import os
import traceback
import shutil

from airtestProject.airtest.report.report import LogToHtml


try:
    from jinja2 import evalcontextfilter as pass_eval_context  # jinja2<3.1
except:
    from jinja2 import pass_eval_context  # jinja2>=3.1

from airtestProject.airtest.core.settings import Settings as ST
from airtestProject.airtest.aircv import imread, get_resolution, FileNotExistError
from airtestProject.airtest.aircv.utils import compress_image
from airtestProject.airtest.utils.compat import decode_path, script_dir_name
from airtestProject.airtest.cli.info import get_script_info
from airtestProject.airtest.utils.logger import get_logger


LOGGING = get_logger(__name__)
DEFAULT_LOG_DIR = "log"
DEFAULT_LOG_FILE = "log.txt"
HTML_TPL = "log_template.html"
HTML_FILE = "log.html"
STATIC_DIR = os.path.dirname(__file__)


class ReportUtil(LogToHtml):
    def __init__(self, script_root, log_root="", static_root="", export_dir=None, script_name="", logfile=None, lang="en", plugins=None, profile_report_dir=None):
        self.log = []
        self.devices = {}
        self.script_root = script_root
        self.script_name = script_name
        if not self.script_name or os.path.isfile(self.script_root):
            self.script_root, self.script_name = script_dir_name(self.script_root)
        self.log_root = log_root or ST.LOG_DIR or os.path.join(".", DEFAULT_LOG_DIR)
        self.static_root = static_root or STATIC_DIR
        self.test_result = True
        self.run_start = None
        self.run_end = None
        self.profile_report_new_dir_list = []
        self.export_dir = export_dir
        self.profile_report_dir = profile_report_dir
        self.logfile = logfile or getattr(ST, "LOG_FILE", DEFAULT_LOG_FILE)
        self.lang = lang
        self.init_plugin_modules(plugins)
        super().__init__(script_root, log_root, static_root, export_dir, script_name, logfile,
                         lang, plugins)

    def _make_export_dir(self):
        """mkdir & copy /staticfiles/screenshots"""
        # let dirname = <script name>.log
        dirname = self.script_name.replace(os.path.splitext(self.script_name)[1], ".log")
        # mkdir
        dirpath = os.path.join(self.export_dir, dirname)
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath, ignore_errors=True)

        if self.profile_report_dir:
            for i in self.profile_report_dir:
                if i is not None:
                    report_name = os.path.basename(i)
                    this_profile_report_new_dir = os.path.join(self.export_dir, report_name)
                    if os.path.exists(i):
                        if os.path.isdir(i):
                            self.copy_tree(i, this_profile_report_new_dir)
                    self.profile_report_new_dir_list.append(this_profile_report_new_dir)

        # def ignore_export_dir(dirname, filenames):
        #     # 忽略当前导出的目录，防止递归导出
        #     if os.path.commonprefix([dirpath, dirname]) == dirpath:
        #         return filenames
        #     return []
        # # self.copy_tree(self.script_root, dirpath, ignore=ignore_export_dir)
        # copy log
        logpath = os.path.join(dirpath, DEFAULT_LOG_DIR)
        if os.path.normpath(logpath) != os.path.normpath(self.log_root):
            if os.path.isdir(logpath):
                shutil.rmtree(logpath, ignore_errors=True)
            self.copy_tree(self.log_root, logpath, ignore=shutil.ignore_patterns(dirname))

        # if self.static_root is not a http server address, copy static files from local directory
        if not self.static_root.startswith("http"):
            for subdir in ["css", "fonts", "image", "js"]:
                self.copy_tree(os.path.join(self.static_root, subdir), os.path.join(dirpath, "static", subdir))
        return dirpath, logpath

    def _translate_code(self, step):
        if step["tag"] != "function":
            return None
        step_data = step["data"]
        args = []
        code = {
            "name": step_data["name"],
            "args": args,
        }
        for key, value in step_data["call_args"].items():
            args.append({
                "key": key,
                "value": value,
            })
        for k, arg in enumerate(args):
            value = arg["value"]
            if isinstance(value, dict) and value.get("__class__") == "OcrTemplate":
                arg["value"] = value['filename']
            if isinstance(value, dict) and (value.get("__class__") == "Template" or value.get("__class__")
                                            == "MyTemplate"):
                if self.export_dir:  # all relative path
                    image_path = value['filename']
                    if not os.path.isfile(os.path.join(self.script_root, image_path)) and value['_filepath']:
                        # copy image used by using statement
                        shutil.copyfile(value['_filepath'], os.path.join(self.script_root, value['filename']))
                else:
                    image_path = os.path.abspath(value['_filepath'] or value['filename'])
                arg["image"] = image_path
                try:
                    if not value['_filepath'] and not os.path.exists(value['filename']):
                        crop_img = imread(os.path.join(self.script_root, value['filename']))
                    else:
                        crop_img = imread(value['_filepath'] or value['filename'])
                except FileNotExistError:
                    # 在某些情况下会报图片不存在的错误（偶现），但不应该影响主流程
                    if os.path.exists(image_path):
                        arg["resolution"] = get_resolution(imread(image_path))
                    else:
                        arg["resolution"] = (0, 0)
                else:
                    arg["resolution"] = get_resolution(crop_img)
        return code

    def report_data(self, output_file=None, record_list=None):
        """
        Generate data for the report page

        :param output_file: The file name or full path of the output file, default HTML_FILE
        :param record_list: List of screen recording files
        :return:
        """
        self._load()
        steps = self._analyse()

        script_path = os.path.join(self.script_root, self.script_name)
        info = json.loads(get_script_info(script_path))
        info['devices'] = self.devices

        if record_list:
            records = [os.path.join(DEFAULT_LOG_DIR, f) if self.export_dir
                       else os.path.abspath(os.path.join(self.log_root, f)) for f in record_list]
        else:
            records = []

        if not self.static_root.endswith(os.path.sep):
            self.static_root = self.static_root.replace("\\", "/")
            self.static_root += "/"

        if not output_file:
            output_file = HTML_FILE

        data = {}
        data['steps'] = steps
        data['name'] = self.script_root
        data['scale'] = self.scale
        data['test_result'] = self.test_result
        data['run_end'] = self.run_end
        data['run_start'] = self.run_start
        data['static_root'] = self.static_root
        data['lang'] = self.lang
        data['records'] = records
        data['info'] = info
        data['log'] = self.get_relative_log(output_file)
        data['reports'] = self.get_profile_report()
        data['console'] = self.get_console(output_file)
        # 如果带有<>符号，容易被highlight.js认为是特殊语法，有可能导致页面显示异常，尝试替换成不常用的{}
        info = json.dumps(data).replace("<", "{").replace(">", "}")
        data['data'] = info
        return data

    def report(self, template_name=HTML_TPL, output_file=HTML_FILE, record_list=None):
        """
        Generate the reports page, you can add custom data and overload it if needed

        :param template_name: default is HTML_TPL
        :param output_file: The file name or full path of the output file, default HTML_FILE
        :param record_list: List of screen recording files
        :return:
        """
        if not self.script_name:
            path, self.script_name = script_dir_name(self.script_root)

        if self.export_dir:
            script_root, self.log_root = self._make_export_dir()

            # output_file可传入文件名，或绝对路径
            output_file = output_file if output_file and os.path.isabs(output_file) \
                else os.path.join(script_root, output_file or HTML_FILE)
            if not self.static_root.startswith("http"):
                self.static_root = "static/"

        if not record_list:
            record_list = [f for f in os.listdir(self.log_root) if f.endswith(".mp4")]
        data = self.report_data(output_file=output_file, record_list=record_list)
        return self._render(template_name, output_file, **data)

    def get_script_name(self):
        new_script_name = self.script_name.split('.')[0]
        return self.script_root, new_script_name

    def get_profile_report(self):
        try:
            path_list = []
            for i in self.profile_report_new_dir_list:
                path_list.append(os.path.join(i, "report.html"))
            return path_list
            # return os.path.relpath(os.path.join(self.log_root, self.logfile), html_dir)
        except:
            LOGGING.error(traceback.format_exc())
            return ""