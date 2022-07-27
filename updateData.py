"""
@file       :updateData.py
@version    :0.1
@author     :ticktock
@date       :2022-07-27
@desc       :用于生成批量运行SAS的程序
"""
import os
import sys
from configparser import ConfigParser


class SasData(object):
    curPath = os.path.dirname(os.path.realpath(sys.argv[0]))
    
    def __init__(self) -> None:
        os.chdir(self.curPath)
        self.config = ConfigParser()
        self.firsts = []
        self.lasts = []
        self.ignore = []
        self.getSasPath()
        self.writeConfig()
        self.readConfig()
        self.sort()
        
    def sort(self) -> list:
        first_tmp = []
        last_tmp = []
        ignore_tmp = []
        for first in self.firsts:
            for file in self.filesPath:
                if first in file:
                    first_tmp.append(file)
        
        for last in self.lasts:
            for file in self.filesPath:
                if last in file:
                    last_tmp.append(file)
                    
        for ignore in self.ignore:
            for file in self.filesPath:
                if ignore in file:
                    ignore_tmp.append(file)
                    
        self.firsts = first_tmp
        self.lasts = last_tmp
        self.ignore = ignore_tmp
        self.filesPath = list(set(self.filesPath) - set(self.firsts) - set(self.lasts) - set(self.ignore))
        self.filesPath = self.firsts + self.filesPath + self.lasts
        
    def getSasPath(self) -> None:
        paths = os.listdir()
        self.filesPath = list(filter(lambda x: ".sas" in x,paths))


    
    def writeConfig(self) -> None:
        sections = ['config']
        options = ['firsts','lasts','ignore']
        if os.path.exists('config.ini'):
            self.config.read('config.ini')
        
        for section in sections:
            if not self.config.has_section(section):
                self.config.add_section(section)
            for option in options:
                if not self.config.has_option(section,option):
                    self.config.set(section,option,"")
                    
        with open('config.ini','w+') as f:
            self.config.write(f)
    
    
    def readConfig(self) -> None:
        self.config.read('config.ini')
        firsts = self.config.get('config','firsts')
        if firsts:
            self.firsts = firsts.split(',')
        lasts = self.config.get('config','lasts')
        if lasts:
            self.lasts = lasts.split(',')
        ignore = self.config.get('config','ignore')
        if ignore:
            self.ignore = ignore.split(',')

        with open('config.ini','w+') as f:
            self.config.write(f)
    
    def format(self, fileName) -> str:
        return '%include "{}"'.format(os.path.join(self.curPath,fileName))
    
    def write(self) -> None:
        if 'updateData.sas' in self.filesPath:
            self.filesPath.remove('updateData.sas')
        filesPath = list(map(lambda x:self.format(x),self.filesPath))
        content = ''
        for path in filesPath:
            content += path + ";\n"
        with open('updateData.sas','w+',encoding='gbk') as f:
            f.write(content)
            
    
            
        

if __name__ == '__main__':
    sasData = SasData()
    print(sasData.curPath)
    sasData.write()
    # sasData.readConfig()
    # sasData.sort()
    # sasData.writeConfig()
    # os.chdir(os.path.dirname(__file__))
    # print(sasData.filesPath)
    # print(sasData.firsts)
    # print(sasData.lasts)
    # print(sasData.ignore)
            
