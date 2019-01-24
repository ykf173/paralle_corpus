import sys
for i in range(1, len(sys.argv)):
    path = sys.argv[i]
    with open(path, "r", encoding='utf-8') as f:
        readlines = f.read().replace('\n\n', '\n').rstrip()
    f.close()

    with open(path, "w", encoding='utf-8') as f:
        f.write(readlines)
    f.close()

#问题，去除中文文本最后一个空行

#LF分句-》去空格-》chamopllion句对齐-》提取tmx