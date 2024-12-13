#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 14:08:09 2024

@author: xiaoxiami
"""

def add_one():
    try:
        user_input = input("请输入一个数字: ")
        number = int(user_input)
        print(f"输出结果: {number + 1}")
    except ValueError:
        print("输入无效，请输入一个数字！")

if __name__ == "__main__":
    add_one()