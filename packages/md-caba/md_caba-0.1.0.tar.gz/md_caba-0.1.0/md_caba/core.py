import re
import json
from pathlib import Path

class MDReader:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.content = self._read_file()
        self.code_blocks = self._extract_code_blocks()
        
    def _read_file(self):
        """读取MD文件内容"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _extract_code_blocks(self):
        """提取所有代码块"""
        pattern = r'```(.*?)\n(.*?)```'
        matches = re.finditer(pattern, self.content, re.DOTALL)
        blocks = {}
        
        for match in matches:
            language = match.group(1).strip()
            content = match.group(2).strip()
            if language not in blocks:
                blocks[language] = []
            blocks[language].append(content)
            
        return blocks
    
    def get_code_blocks(self, language=None):
        """获取指定语言的代码块"""
        if language:
            return self.code_blocks.get(language, [])
        return self.code_blocks
    
    def to_dict(self):
        """将内容转换为字典格式"""
        return {
            'file_path': str(self.file_path),
            'code_blocks': self.code_blocks
        }
    
    def to_json(self):
        """将内容转换为JSON格式"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def print_content(self):
        """打印所有内容"""
        print(f"文件路径: {self.file_path}")
        print("\n代码块内容:")
        for language, blocks in self.code_blocks.items():
            print(f"\n{language}:")
            for i, block in enumerate(blocks, 1):
                print(f"\n块 {i}:")
                print(block) 