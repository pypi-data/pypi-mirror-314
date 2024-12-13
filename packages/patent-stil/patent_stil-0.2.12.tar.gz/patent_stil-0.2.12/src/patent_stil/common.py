import re
RE_MAP={
    "cross_reference": [
        re.compile(r"CROSS[-\s]?REFERENCE(?: TO RELATED APPLICATIONS)?", re.IGNORECASE)
    ],
    "related_applications": [
        re.compile(r"RELATED APPLICATIONS", re.IGNORECASE)
    ],
    "technical_field": [
        re.compile(r"Technical Field|技术领域|FIELD OF (?:INVENTION|PRESENT APPLICATION)|TECHNICAL FIELD|FIELD", re.IGNORECASE)
    ],
    "background": [
        re.compile(r"Background|背景技术|BACKGROUND OF (?:THE INVENTION|INVENTION|PRESENT APPLICATION)|BACKGROUND INFORMATION", re.IGNORECASE)
    ],
    "disclosure_of_invention": [
        re.compile(r"(?:\d+\.\s*)?SUMMARY|Disclosure of Invention|发明内容|SUMMARY OF (?:THE INVENTION|INVENTION)|BRIEF SUMMARY OF THE PRESENT APPLICATION|BRIEF DESCRIPTION OF THE INVENTION", re.IGNORECASE)
    ],
    "drawings": [
        re.compile(r"Drawings|附图说明|BRIEF DESCRIPTION OF (?:THE DRAWINGS|DRAWINGS|THE FIGURES)", re.IGNORECASE)

    ],
    "detailed_description": [
        re.compile(r"Detailed Description|具体实施方式|DETAILED DESCRIPTION OF (?:THE INVENTION|INVENTION)|DESCRIPTION OF THE PREFERRED EMBODIMENTS", re.IGNORECASE)
    ]
}
def parsePatentDescription(text, map=None):
    # 定义默认的映射字典
    if map is None:
        map = RE_MAP
    # 使用字典保存结果
    sections = {key: "" for key in map}
    # 按行分割文本并清理空白字符
    lines = text.strip().split("\n")
    current_header = None
    # 遍历每一行，提取对应的文本
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue
        # 查找当前行的标题
        flag=True
        for header, patterns in map.items():
            if any(pattern.search(line) for pattern in patterns):
                current_header = header
                flag=False
                break
        if current_header and flag:
            sections[current_header] += line + "\n"
    # 去除每个部分末尾的换行符
    return {key: value.strip().replace("\n","") if value and value!="" else None for key, value in sections.items()}

def getUSApplicationID(us_application_num):
    match = re.search(r'US(\d+)([A-Z]?)?', us_application_num)
    if match:
        digits = match.group(1)  # 提取数字部分
        return digits
    return None