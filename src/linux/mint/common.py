# coding=utf-8
import getpass
import os

import sh
from os.path import join
from sh import sudo

from config import config

__author__ = 'peter'


# 打印长输出
def print_msg(msg):
    print("##################################################")
    print("# " + msg)
    print("##################################################")


# 打印短输出
def print_tab(msg, tab_cnt=1):
    prefix = ''
    for i in range(tab_cnt):
        prefix += '    '
    print(prefix + msg)


# 获得HOME目录
def get_home_path():
    return os.environ['HOME']


# 获得当前用户名
def get_user_name():
    return getpass.getuser()


# 获得云同步目录
def get_cloud_path(software=config.cloud_software):
    home = get_home_path()
    path = None
    if software == "Ubuntu One":
        path = join(home, "Ubuntu One")
    elif software == "Dropbox":
        path = join(home, "Dropbox")
    elif software == "KuaiPan":
        path = join(home, "KuaiPan")
    elif software == "Nutstore":
        path = join(home, "Nutstore")
    return path


# 添加软件源
def add_apt_repository(add_apt_repository_list):
    print_msg("添加软件源")
    for item in add_apt_repository_list:
        print('    add: ' + item)
        sudo("add-apt-repository", "-y", "ppa:" + item)


# 更新软件仓库
def apt_get_update():
    print_msg("更新软件仑库")
    sudo("apt", "update")


# 安装软件
def apt_get_install(software):
    if isinstance(software, list):
        print_msg("安装软件")
        for items in software:
            print('    install: ' + items)
            for item in items.split(' '):
                sudo("apt", "install", "-y", item)
    elif isinstance(software, str):
        print('    install: ' + software)
        sudo("apt", "install", "-y", software)


# 卸载软件
def apt_get_remove(software):
    if isinstance(software, list):
        print_msg("安装软件")
        for items in software:
            print('    remove: ' + items)
            for item in items.split(' '):
                sudo("apt", "purge", "-y", item)
    elif isinstance(software, str):
        print('    remove: ' + software)
        sudo("apt", "purge", "-y", software)


# 清理不用的软件包
def apt_get_autoremove():
    print_msg('清理不用的软件包')
    sudo("apt", "autoremove", "-y")


# 通过gsettings设置系统
def gsettings_set(schema, key, value):
    sh.gsettings("set", schema, key, value)


def ln_path(src, desc):
    # 判断目标是否已存在
    if os.path.exists(desc):
        return print_tab("ln error: '%s' already exist" % desc)
    try:
        sh.ln("-s", src, desc)
    except sh.ErrorReturnCode_1 as e:
        print_tab("ln error: " + e.full_cmd)


# 云路径软链接到HOME目录
def ln_cloud_to_home(cloud_sub_path, home_sub_path):
    src = get_cloud_path() + '/' + cloud_sub_path
    desc = get_home_path() + '/' + home_sub_path
    ln_path(src, desc)


# 创建目录
def md2home(dir_name):
    try:
        sh.mkdir("-p", get_home_path() + "/" + dir_name)
    except sh.ErrorReturnCode_1 as e:
        print_tab("mkdir error: '" + dir_name + "' already exist")


# 复制目录
def cp_dir(src, desc):
    sh.cp("-r", src, desc)
