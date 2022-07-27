"""
@file       :c2c.py
@version    :0.1
@author     :ticktock
@date       :2022-07-27
@desc       :description
"""
import os
import chardet

ans = None
while True:
    ans = input('输入要转换的编码格式序号\n\
1.GBK\n\
2.UTF-8\n\
:')
    if ans == '1':
        encoding = 'gbk'
        break
    elif ans == '2':
        encoding = 'UTF-8'
        break
    else:
        print("序号输入错误请重新输入!\n")
        
sasfiles = list(filter(lambda x:'.sas' in x,os.listdir('.')))
for sasfile in sasfiles:
    with open(sasfile,'rb') as f:
        result = chardet.detect(f.read())
    with open(sasfile,'r',encoding=result['encoding']) as f:
        content = f.read()
    with open(sasfile,'w',encoding=encoding) as f:
        f.write(content)
