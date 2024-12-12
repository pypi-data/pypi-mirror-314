# MD CaBa

一个简单的Markdown文件读取和解析工具。

## 安装

```bash
pip install md_caba
```

## 使用方法

```python
from md_caba import MDReader

# 创建MDReader实例
reader = MDReader('path/to/your/file.md')

# 获取所有代码块
code_blocks = reader.get_code_blocks()

# 获取特定语言的代码块
python_blocks = reader.get_code_blocks('python')

# 打印所有内容
reader.print_content()

# 转换为JSON
json_content = reader.to_json()
``` 