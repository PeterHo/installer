# coding=utf-8
from os import walk

from os import listdir

from os.path import isdir, join

from linux.mint.common import print_tab, ln_cloud_to_home, md2home, get_cloud_path, ln_path, get_home_path

__author__ = 'peter'

# Jetbrains产品配置目录列表
jetbrainsConfigDirList = {
    'Android Studio': '.AndroidStudioPreview2.2',
    'IntelliJ IDEA': '.IntelliJIdea2016.2',
    'PyCharm': '.PyCharm2016.2',
    'WebStorm': '.WebStorm2016.2',
    'CLion': '.CLion2016.1',
}

# 配置源根目录
srcConfigRootDir = "Settings/JetBrains"


def clearLinks():
    pass


def configPlugins():
    pass


def config(srcConfigDir, targetConfigDir):
    srcConfigFullDir = join(get_cloud_path(), srcConfigRootDir, srcConfigDir)
    md2home(targetConfigDir)
    md2home(join(targetConfigDir, 'config/plugins'))
    # 普通配置文件
    for (dirPath, _, fileNames) in walk(srcConfigFullDir):
        # 对所有包含文件的非插件目录中的文件做软链接
        if fileNames and not dirPath.endswith('/config/plugins') and dirPath.find('/config/plugins/') == -1:
            newDir = targetConfigDir + dirPath[len(srcConfigFullDir):]
            md2home(newDir)
            for fileName in fileNames:
                ln_path(join(dirPath, fileName), join(get_home_path(), newDir, fileName))

    # 插件
    try:
        srcPluginDir = join(srcConfigFullDir, 'config/plugins')
        pluginDirs = [f for f in listdir(srcPluginDir) if isdir(join(srcPluginDir, f))]
        for pluginDir in pluginDirs:
            ln_path(join(srcPluginDir, pluginDir), join(get_home_path(), targetConfigDir, 'config/plugins', pluginDir))
    except FileNotFoundError:
        pass


def configCommon():
    print_tab("Common Configs")
    for configDir in jetbrainsConfigDirList.values():
        config("Commons", configDir)


def configPycharm():
    ideName = "PyCharm"
    print_tab(ideName)
    config(ideName, jetbrainsConfigDirList[ideName])


def configJetbrains():
    print_tab("JetBrains")
    ln_cloud_to_home("Settings/JetBrains/_ideavimrc", ".ideavimrc")
    configCommon()
    configPycharm()


if __name__ == '__main__':
    configJetbrains()


def config_idea():
    print_tab("IntelliJ IDEA")
    md2home(".IntelliJIdea14/config")
    ln_cloud_to_home("Settings/JetBrains/Intellij IDEA/fileTemplates", ".IntelliJIdea14/config/fileTemplates")
    ln_cloud_to_home("Settings/JetBrains/Intellij IDEA/templates", ".IntelliJIdea14/config/templates")
