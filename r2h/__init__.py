# coding: utf-8
import os

config = {}
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
exec(open("{}/r2h.conf".format(basedir)).read(), config)
