import os
import sys
import shutil

THISDIR = os.path.dirname(__file__)
DIR = lambda x: os.path.join(THISDIR, x)
ROOT_PATH = DIR("..")
APK = DIR("../playground/test_blackjack.air/blackjack-release-signed.apk")
PKG = "org.cocos2d.blackjack"
OWL = DIR("../playground/test_blackjack.air")
IMG = os.path.join(OWL, "tpl1499240443959.png")
CASENAME = ""
LOG_ROOT = DIR("../result/logs")
OUTPUT_HTML =DIR("../result/output_html")
CASE_RESULT = False
TEMPLATE_PATH = DIR("../template")
print(os.path.abspath(TEMPLATE_PATH))