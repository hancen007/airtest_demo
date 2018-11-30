#!/usr/bin/env
# -*- coding: utf-8 -*-
import os
import io
import unittest
from airtest.core.android.android import ADB
from airtest.core.helper import G
from airtest.__main__ import main as main_parser
from util.testconf import DIR, OWL, LOG_ROOT,OUTPUT_HTML
import util.testconf
from util.commonScript import Common_function
import jinja2


class TestCli(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setUpClass")
        if not ADB().devices(state="device"):
            raise RuntimeError("At lease one adb device required")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
        G.LOGGER.set_logfile(None)

    def test_info(self):
        argv = ["info", OWL]
        main_parser(argv)
        print("test_info")

    def test_report_with_log_dir(self):
        common = Common_function()
        root_dir = "E:\\KAirtest\\playground"
        all_case = common.find_all_script(root_dir)
        results = []
        for case_path in all_case:
            CASENAME = common.get_last_floder(case_path).replace(".air","")
            log_case_path = LOG_ROOT + "\\" + CASENAME
            html_case_path = OUTPUT_HTML + "\\" + CASENAME
            html_case_path_log = html_case_path + "\\" + "log.html"
            common.create_folder(log_case_path)
            common.create_folder(html_case_path)
            try:
                argv = ["run", case_path, "--device", "Android:///", "--log", log_case_path]
                main_parser(argv)
            except:
                pass
            finally:
                argv = ["report", case_path, "--log_root", log_case_path, "--outfile", html_case_path_log]
                main_parser(argv)
                result = dict()
                result["name"] = CASENAME
                result["result"] = util.testconf.CASE_RESULT
                result["output_html"] = html_case_path_log
                results.append(result)

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(util.testconf.TEMPLATE_PATH),
            extensions=(),
            autoescape=True
        )
        template = env.get_template("summary_template.html", util.testconf.TEMPLATE_PATH)
        html = template.render({"results": results})
        output_file = os.path.join(util.testconf.ROOT_PATH, "summary.html")
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        print(output_file)
        print("test_report_with_log_dir")



if __name__ == '__main__':
    unittest.main()
