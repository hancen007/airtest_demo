# -*- coding: utf-8 -*-

import unittest
import os
import sys
import six
import re
import shutil
import traceback
import warnings
from io import open
from airtest.core.api import G, auto_setup, log
from airtest.core.settings import Settings as ST
from airtest.utils.compat import decode_path
from copy import copy


class AirtestCase(unittest.TestCase):

    PROJECT_ROOT = "."
    SCRIPTEXT = ".air"
    TPLEXT = ".png"

    @classmethod
    def setUpClass(cls):
        # runScrip传进来的参数
        cls.args = args
        # 设置参数，设备、log路径、脚本路径
        setup_by_args(args)

        # setup script exec scope
        cls.scope = copy(globals())
        cls.scope["exec_script"] = cls.exec_other_script

    def setUp(self):
        # 如果参数配置了log路径且recording为Ture
        if self.args.log and self.args.recording:
            for dev in G.DEVICE_LIST:
                try:
                    # 开始录制
                    dev.start_recording()
                except:
                    traceback.print_exc()

    def tearDown(self):
        # 停止录制
        if self.args.log and self.args.recording:
            for k, dev in enumerate(G.DEVICE_LIST):
                try:
                    output = os.path.join(self.args.log, "recording_%d.mp4" % k)
                    dev.stop_recording(output)
                except:
                    traceback.print_exc()

    def runTest(self):
        # 参数传入的脚本路径
        scriptpath = self.args.script
        # 分割路径最后的名字，替换.air为.py，也就是传入‘d:/aaa/bbb.air’，pyfilename就为bbb.py
        pyfilename = os.path.basename(scriptpath).replace(self.SCRIPTEXT, ".py")
        # 再组装py文件的路径，d:/aaa/bbb.air/bbb.py，看过air脚本文件就知道，这才是脚本代码，其他是图片
        pyfilepath = os.path.join(scriptpath, pyfilename)
        pyfilepath = os.path.abspath(pyfilepath)
        self.scope["__file__"] = pyfilepath
        # 读进来
        with open(pyfilepath, 'r', encoding="utf8") as f:
            code = f.read()
        pyfilepath = pyfilepath.encode(sys.getfilesystemencoding())
        # 运行读进来的脚本
        try:
            exec(compile(code.encode("utf-8"), pyfilepath, 'exec'), self.scope)
        except Exception as err:
            tb = traceback.format_exc()
            log("Final Error", tb)
            six.reraise(*sys.exc_info())

    @classmethod
    def exec_other_script(cls, scriptpath):
        """run other script in test script"""

        warnings.simplefilter("always")
        warnings.warn("please use using() api instead.", PendingDeprecationWarning)

        def _sub_dir_name(scriptname):
            dirname = os.path.splitdrive(os.path.normpath(scriptname))[-1]
            dirname = dirname.strip(os.path.sep).replace(os.path.sep, "_").replace(cls.SCRIPTEXT, "_sub")
            return dirname

        def _copy_script(src, dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst, ignore_errors=True)
            os.mkdir(dst)
            for f in os.listdir(src):
                srcfile = os.path.join(src, f)
                if not (os.path.isfile(srcfile) and f.endswith(cls.TPLEXT)):
                    continue
                dstfile = os.path.join(dst, f)
                shutil.copy(srcfile, dstfile)

        # find script in PROJECT_ROOT
        scriptpath = os.path.join(ST.PROJECT_ROOT, scriptpath)
        # copy submodule's images into sub_dir
        sub_dir = _sub_dir_name(scriptpath)
        sub_dirpath = os.path.join(cls.args.script, sub_dir)
        _copy_script(scriptpath, sub_dirpath)
        # read code
        pyfilename = os.path.basename(scriptpath).replace(cls.SCRIPTEXT, ".py")
        pyfilepath = os.path.join(scriptpath, pyfilename)
        pyfilepath = os.path.abspath(pyfilepath)
        with open(pyfilepath, 'r', encoding='utf8') as f:
            code = f.read()
        # replace tpl filepath with filepath in sub_dir
        code = re.sub("[\'\"](\w+.png)[\'\"]", "\"%s/\g<1>\"" % sub_dir, code)
        exec(compile(code.encode("utf8"), pyfilepath, 'exec'), cls.scope)


def setup_by_args(args):
    # init devices
    # 如果传入的设备参数是一个列表，所以命令行可以设置多个设备哦
    if isinstance(args.device, list):
        devices = args.device
    elif args.device:
        # 不是列表就给转成列表
        devices = [args.device]
    else:
        devices = []
        print("do not connect device")

    # set base dir to find tpl 脚本路径
    args.script = decode_path(args.script)

    # set log dir 日志路径
    if args.log is True:
        print("save log in %s/log" % args.script)
        args.log = os.path.join(args.script, "log")
    elif args.log:
        print("save log in '%s'" % args.log)
        args.log = decode_path(args.log)
    else:
        print("do not save log")

    # guess project_root to be basedir of current .air path 脚本的路径设置为工程根目录
    project_root = os.path.dirname(args.script) if not ST.PROJECT_ROOT else None
    # 这个接口很熟悉吧，在IDE里新建一个air脚本就会自动生成这句，里面就设备的初始化连接，设置工程路径，日志路径。
    auto_setup(args.script, devices, args.log, project_root)


def run_script(parsed_args, testcase_cls=AirtestCase):
    global args  # make it global deliberately to be used in AirtestCase & test scripts
    args = parsed_args
    suite = unittest.TestSuite()
    suite.addTest(testcase_cls())
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if not result.wasSuccessful():
        sys.exit(-1)
