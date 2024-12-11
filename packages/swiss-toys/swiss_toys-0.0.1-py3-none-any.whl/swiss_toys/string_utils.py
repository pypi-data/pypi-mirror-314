def reverse_string(text):
    """反转字符串"""
    return text[::-1]

def count_chars(text):
    """统计字符出现次数"""
    return {char: text.count(char) for char in set(text)} 