# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/5/23 19:37
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : naming.py
# @Software: PyCharm
"""
import re
from pypinyin import pinyin, Style

display_name_pattern = r"^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9_-]*$"


def display_name_to_local_name(display_name):
    """
    从display name生成 local name
    :param display_name: 展示名称
    :return: 生成的local name

    example:
    端到端自动化产线-创建作业-模型-V100： duandaoduanzidonghuacx-cjzy-mx-V100
    ppl-图像-目标检测-7YjT4YDe-模型：ppl-tuxiang-mubiaojianc-7YjT4YDe-mx
    矿山物体+人检测-检测模型-T4： kuangshanwutirenjiance-jiancemox-T4
    """
    if not isinstance(display_name, str) or not display_name:
        return None

    i = 0
    while True:
        # 将中文字符转换为拼音，其余字符保持不变
        pinyin_words = pinyin(display_name, style=Style.NORMAL)
        result = list()
        for index, pinyin_word in enumerate(pinyin_words):
            if index <= len(pinyin_words) + i:
                result.append(pinyin_word[0])
                continue
            if pinyin_word[0].startswith("-"):
                result.append(pinyin_word[0])
            else:
                result.append(pinyin_word[0][0])
        filtered_name = "".join(result)

        # 去除除了字母、数字和连字符 "-"、下划线"_" 之外的字符
        filtered_name = re.sub(r"[^a-zA-Z0-9_-]", "", filtered_name)
        # 如果不是以字母或数字开头和结尾，则删除开头和结尾的非字母或数字的字符
        if not re.match(r"^[a-zA-Z0-9].*[a-zA-Z0-9]$", filtered_name):
            # 删除开头不是字母或数字的字符
            filtered_name = re.sub(r"^[^a-zA-Z0-9]+", "", filtered_name)
            # 删除结尾不是字母或数字的字符
            filtered_name = re.sub(r"[^a-zA-Z0-9]+$", "", filtered_name)

        i = i - 1
        if len(filtered_name) <= 33 or i < -len(pinyin_words):
            break
    # 如果缩写后的名称长度超过36个字符，则截断
    return truncate_local_name(filtered_name)


def truncate_local_name(local_name):
    """
    截断local name长度
    :return:
    """
    if len(local_name) > 33:
        local_name = local_name[-33:]
    # 删除开头不是字母或数字的字符
    local_name = re.sub(r"^[^a-zA-Z0-9]+", "", local_name)
    # 删除结尾不是字母或数字的字符
    local_name = re.sub(r"[^a-zA-Z0-9]+$", "", local_name)
    return local_name
