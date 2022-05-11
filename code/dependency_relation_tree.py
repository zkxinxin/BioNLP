#导入stanza包
#处理Stanza无法下载语言模型的错误：ConnectionError请看下面的网址
#https://blog.csdn.net/gz927cool/article/details/121868829?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~aggregatepage~first_rank_ecpm_v1~rank_v31_ecpm-3-121868829-null-null.pc_agg_new_rank&utm_term=stanza+%E8%AF%AD%E8%A8%80%E5%8C%85&spm=1000.2123.3001.4430
import stanza
from stanza.utils.conll import CoNLL

def nlp():

    #指定英文
    config = {
        'dir': '.\\stanza_resources\\',
        'lang': 'en'
    }
    #建立管道
    nlp1 = stanza.Pipeline(**config)

    file1 = open('E:\\bionlp\\clean_map3.txt', 'r')
    a = file1.readlines()
    file = open('E:\\bionlp\\result3.txt', 'w')
    for i in range(0, len(a), 2):
        #分词
        doc = nlp1(a[i])
        # print(doc)
        # conll = CoNLL.convert_dict(doc)

        print(i)

        res = doc.to_dict()
        # print(res)
        #以conll格式写入文件
        for s in res[0]:
            # print(s)
            if 'feats' not in s.keys():
                s['feats'] = '_'
            file.write(str(s['id']) + '\t' + s['text'] + '\t' + s['lemma'] + '\t' + s['upos'] + '\t' + s['xpos'] + '\t' + str(s['feats']) + '\t' + str(s['head']) + '\t' + s['deprel'] + '\t' + '_' + '\t' + '_')
            file.write('\n')
        file.write('\n')
    file.close()

    # print(conll)
    # print(type(doc))


if __name__ == '__main__':
    nlp()

