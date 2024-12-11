def read_text_file(file_path, encoding='utf-8'):
    """读取文本文件内容"""
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()

def write_text_file(file_path, content, encoding='utf-8'):
    """写入文本文件内容"""
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content) 