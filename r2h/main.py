# coding: utf-8
from r2h import config
from r2h.utils.cmd import run
import requests
import sys

from r2h.utils.logger import logger


def login_harbor():
    run("docker login --username {} --password {} {}".format(config["harbor_username"], config["harbor_password"], config["harbor_host"]))


def get_registry_info():
    image_name_url = "http://{}:{}/v2/_catalog".format(config["registry_host"], config["registry_port"])
    resp = requests.get(image_name_url)
    if resp.status_code != 200:
        logger.error("registry请求失败")
        sys.exit(2)
    image_name_list = resp.json()["repositories"]
    return image_name_list


class RegistryHandler():
    def __init__(self):
        self.image_name_url = "http://{}:{}/v2/_catalog".format(config["registry_host"], config["registry_port"])

    def get_image_name(self):
        resp = requests.get(self.image_name_url)
        if resp.status_code != 200:
            logger.error("registry请求失败")
            sys.exit(2)
        self.image_name_list = resp.json()["repositories"]

    def storehouse_name(self):
        self.storehouse_list = []
        for image_name in self.image_name_list:
            storehouse_name = image_name.split("/")[0]
            if storehouse_name not in self.storehouse_list:
                self.storehouse_list.append(storehouse_name)

    def get_image_tag(self):
        for image_name in self.image_name_list:
            image_tag_url = "http://{}:{}/v2/ars/scanner/tags/list".format(config["registry_host"], config["registry_port"])
            resp = requests.get(image_tag_url)
            if resp.status_code != 200:
                logger.error("registry请求失败")
                sys.exit(2)
            image_tags = resp.json()["tags"]
            for tag in image_tags:
                need_load_image_name = "{}:{}/{}:{}".format(config["registry_host"], config["registry_port"], image_name, tag)
                logger.info("开始加载:{}".format(need_load_image_name))
                run("docker pull {}".format(need_load_image_name))
                retag_image_name = "{}/{}:{}".format(config["registry_host"], image_name, tag)
                logger.info("开始重打镜像tag:{}".format(need_load_image_name))
                run("docker push {}".format(retag_image_name))
                logger.info("恢复镜像:{}成功".format(retag_image_name))


if __name__ == '__main__':
    # login_harbor()
    rh = RegistryHandler()
    rh.get_image_name()
    rh.storehouse_name()
