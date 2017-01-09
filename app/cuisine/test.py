# !/Users/zhanghan/miniconda2/envs/python3.4/bin python
# coding=utf-8
# @name :  test.py
# @time :  17/1/9 
# @Author : zhanghan
# @Email : klay.zhanghan@gmail.com
import json

f = open('bbc_recipe_name.json', 'w')
jd = json.dumps(bbc_recipe_name)
f.write(jd)
f.close()

f = open('bbc_recipe_name.json','r')
j = f.read()
