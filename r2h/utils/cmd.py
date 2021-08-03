# coding: utf-8
import subprocess
import sys

from r2h.utils.logger import logger


def run(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if not p.returncode:
        return out
    logger.error(out)
    sys.exit(2)
