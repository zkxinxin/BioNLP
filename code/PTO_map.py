import re
from itertools import chain

index = []
data = []
with open("E:/zhangkexin/文本挖掘/RTO-1.0.obo.txt", 'r', encoding='utf-8') as f:
    for line in f:
        # print(line.strip())
        if line.strip().find('[Term]') != -1:
            # print(line.strip())
            index.append(line.strip())  # 2051个性状
        data.append(line.strip())

# 将每个性状拿出来
flag = []
for i in range(len(data)):
    if data[i] == '[Term]':
        flag.append(i)
TO_term = []
for j in range(len(flag)):
    if j != len(flag) - 1:
        TO_term.append(data[flag[j]:flag[j + 1] - 1])
    else:
        TO_term.append(data[flag[-1]:-1])
# 将其整理为字典形式
TO_term_name = []
TO_term_dict = {}
TO_term_id = {}
for i in TO_term:
    synonym = []
    for j in i:
        if j.find('id:') != -1:
            TO_id = j.split(':')[1].strip() + ':' + j.split(':')[2].strip()
        elif j.find('name') != -1:
            name_str = j.split(':')[1].strip()
            TO_term_name.append(name_str)
        elif j.find('synonym') != -1:
            synonym_str = j.split(':')[1].strip()
            synonym_str = synonym_str.split('"')[1]
            # print(synonym_str)
            synonym_str.replace('(related)', '').strip()  # 没起作用
            synonym.append(synonym_str)

    TO_term_dict[name_str] = synonym

# 将带有GO的句子与TO匹配
one_sentence = []
all_sentence = []
with open('E:/zhangkexin/文本挖掘/GOsentence.txt', 'r', encoding='utf-8') as ff:
    for line in ff:
        if line != '\n':
            one_sentence.append(line.strip())
        else:
            all_sentence.append(one_sentence)
            one_sentence = []
with open('E:/zhangkexin/文本挖掘/map_GO_TO.txt', 'w') as ff1:
    for i in range(len(all_sentence)):
        gene_sentence = all_sentence[i][2]
        for j in TO_term_name:
            if gene_sentence.find(j) != -1:
                ff1.write(gene_sentence + '\n' + 'GO:' + all_sentence[i][1] + '\t' + 'TO:' + j + '\n')

# 将PTO对统一为id
GO_dict = {}
with open('E:/QQfiles/WeChat Files/wxid_01cg4d9f6b9422/FileStorage/File/2022-05/GO.txt', 'r', encoding='utf-8') as f2:
    for line in f2:
        GO_dict[line.split('\t')[0]] = (list(map(lambda x: x.lower(), line.split('\t')[1].split(','))))

with open('E:/QQfiles/WeChat Files/wxid_01cg4d9f6b9422/FileStorage/File/2022-05/GO_TO_hits.dic', 'r',
          encoding='utf-8') as f1:
    with open('E:/QQfiles/WeChat Files/wxid_01cg4d9f6b9422/FileStorage/File/2022-05/id.txt', 'w',
              encoding='utf-8') as f3:
        for line in f1:
            oneGO = line.split('\t')[0]
            oneTO = line.split('\t')[1]
            num = line.split('\t')[2]
            for i in GO_dict.values():
                if oneGO in i:
                    GO_id = list(GO_dict.keys())[list(GO_dict.values()).index(i)]
                    break
            for j in TO_term_id.values():
                if oneTO == j:
                    TO_id = list(TO_term_id.keys())[list(TO_term_id.values()).index(oneTO)]
                    break
            f3.write(GO_id + '\t' + TO_id + '\t' + num)
