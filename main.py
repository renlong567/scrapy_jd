# -*- coding: UTF-8 -*-
from scrapy.cmdline import execute
import sys
import os

# 这里就不细说了，反正命令行的命令都用这个叫execute的函数来执行就完事了，
# 命令用列表存放
# 每次运行这个文件就行了
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "netbian"])
