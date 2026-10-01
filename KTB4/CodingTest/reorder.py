import re

filepath = "/Users/emet/TIL/KTB4/CodingTest/20260930/CheatSheet.md"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start indices of each section
sec1_match = re.search(r'## 1\. 자주 사용된 핵심 라이브러리', content)
sec4_match = re.search(r'## 4\. 파이썬 표준 입출력', content)

# Split the content
header = content[:sec1_match.start()]
body = content[sec1_match.start():sec4_match.start()]
io_section = content[sec4_match.start():]

# Rename the section headers
io_section = io_section.replace('## 4. 파이썬 표준 입출력 (Standard I/O) 템플릿', '## 1. 파이썬 표준 입출력 (Standard I/O) 템플릿')
body = body.replace('## 1. 자주 사용된 핵심 라이브러리', '## 2. 자주 사용된 핵심 라이브러리')
body = body.replace('## 2. 빈출 알고리즘', '## 3. 빈출 알고리즘')
body = body.replace('## 3. 자주 나오는 핵심 구현', '## 4. 자주 나오는 핵심 구현')

new_content = header + io_section + '\n\n---\n\n' + body

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Success")
