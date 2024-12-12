import re
import json
from pathlib import Path

class MDReader:
    def __init__(self):
        # 直接嵌入 daan.md 的内容
        self.content = """二阶段3模块

```
1、 e44e4612f62d2fb8f8738bab118a9850
2、 546c66f2ba115470da0d6052f47bd0b8
```

二阶段4模块

```
1、516834cc-50e448af-bcf9ed53-9ae4328e
2、b1815a96bcbe342afd061ff6f818ec4e
```

三阶段2模块

```
1、18090-15060-17080
2、salvationlieswithin
3、443
```

三阶段3模块

```
1、flag{5a02e0d7-1ffa-b8db-50b9-1dec2ca9edfd}
2、flag{3165e937-9128-ceb9-fa0e-1c0bbb1074a7}
```"""
        self.code_blocks = self._extract_code_blocks()
    
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
            'content': self.content,
            'code_blocks': self.code_blocks
        }
    
    def to_json(self):
        """将内容转换为JSON格式"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def print_content(self):
        """打印所有内容"""
        print("内容:")
        print(self.content)
        print("\n代码块内容:")
        for language, blocks in self.code_blocks.items():
            print(f"\n{language}:")
            for i, block in enumerate(blocks, 1):
                print(f"\n块 {i}:")
                print(block) 