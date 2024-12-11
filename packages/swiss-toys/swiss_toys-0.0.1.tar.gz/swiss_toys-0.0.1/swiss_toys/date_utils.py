from datetime import datetime

def get_current_timestamp():
    """获取当前时间戳"""
    return datetime.now().timestamp()

def format_datetime(dt, format_str="%Y-%m-%d %H:%M:%S"):
    """格式化日期时间"""
    return dt.strftime(format_str) 