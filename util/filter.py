#encoding=utf-8
import emoji
import re

def get_opening_time(str):
    """ 获取开放时间 """
    if '；' in str:
        return str.split('；')[1].strip('明日').strip()
    else:
        return str.strip('明日').strip()

def remove_emoji(text):
    """ 过滤emoji特殊字符 """
    return emoji.replace_emoji(text, ' ').strip(' ')

def remove_line(str):
    """ 过滤多余的空格和换行符 """
    str =  re.sub(r"\s+", " ", str)
    return re.sub(r'\n+', ',', str).strip()

def remove_special_characters(str):
    """ 过滤特殊字符 """
    if str is not None and len(str) != 0:
        return remove_emoji(remove_line(str)).replace(',','').replace(' ', '')
    return

def truncate_chinese(text, length=200):
    # 确保只计算中文字符
    chinese_chars = [char for char in text]

    if len(chinese_chars) > length:
        return ''.join(chinese_chars[:length]) + '...'
    else:
        return text
