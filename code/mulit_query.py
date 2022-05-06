# Codes developer: Sizhuo Ouyang
#lisheng rewrite
# HZAU BioNLP Lab
# 2022-04
# 代码目的：读取PubTator结果文件，根据关键词生成命中句及其标注。
#增加多进程功能。
from multiprocessing import Pool
import getopt
import sys
import nltk
from nltk.tokenize import sent_tokenize
import re
import time
time1=time.time()
def usage():
	print(
		"""
Usage:
  python  keywords_query_pubtator.py -i <inputfile1> -w <wordfile> -o <outputfile> -h <help>
  
function: query whatever you want!!!!

 text input format:
*************************************
26389399|t|Bladder Cancer Treatment (PDQ ): Health Professional Version
26389399|a|This PDQ cancer information summary for health professionals provides comprehensive, peer-reviewed, evidence-based information about the treatment of bladder cancer. It is intended as a resource to inform and assist clinicians who care for cancer patients. It does not provide formal guidelines or recommendations for making health care decisions. This summary is reviewed regularly and updated as necessary by the PDQ Adult Treatment Editorial Board, which is editorially independent of the National Cancer Institute (NCI). The summary reflects an independent review of the literature and does not represent a policy statement of NCI or the National Institutes of Health (NIH).
26389399	0	14	Bladder Cancer	Disease	MESH:D001749
26389399	70	76	cancer	Disease	MESH:D009369
26389399	211	225	bladder cancer	Disease	MESH:D001749
26389399	301	307	cancer	Disease	MESH:D009369
26389399	308	316	patients	Species	9606
26389399	562	568	Cancer	Disease	MESH:D009369
*************************************

word input format:

word1
word2
word3 
	"""
	)


# target_pubtator = open('./data/pubtator_blca.txt','r',encoding='utf-8')
# sent_report = open('tmp_pubtator_blca_key_query.txt','w',encoding='utf-8')

def filter_sent(keyword,target_pubtator,sent_report):
	annotation_dic = {} #{O start ： anotions line}
	sent_list = []	#[{'begin'：开始位置},'end':标题长+1，'sent':标题句]
	sentnub = 0	#句子数
	articlenub = [] #文章数
	n=0
	# print("Working progress: ")
	with open(target_pubtator) as ff:
		for line in ff:
			
			if line[8:11] == '|t|':	#标题行
				at = 'pmid:'+line.split('|t|')[0]+'\n'	#标题信息
				title = line.strip().split('|t|')[-1]	#标题内容
				len_title = len(title)	#标题长度
				sent_list.append({"begin":0,"end":len_title+1,"sent":title}) #这个板块加入标题的信息
				continue
				#print(sent_list)
			if line[8:11] == '|a|':	#摘要行
				sent_annotation = {}	
				article = line.strip().split('|a|')[-1]	#摘要内容
				sents = sent_tokenize(article)#分句
				start = len_title+2	#从标题结束往后两格为第一句开始
				sent_start = []	#句子开始位置 列表
				sent_end = []	#句子结束位置 列表
				sent_start.append(start)	#第一句的开始位置
				for sent in sents:	#每个句子 in 句子列表
					start = len(sent) + 2 +start  #每一个句子的开始位置
					sent_start.append(start)	#加入列表
					sent_end.append(start-1)	#后一个句子的前一格，是前一个句子的结尾
				
				for i,s in enumerate(sent_start[0:-1]):	#索引：句子的开始位置
					#{句子的开始位置，结束位置，句子}
					sent_list.append({"begin":s,"end":sent_end[i],"sent":sents[i]})  #一篇文章的每个句子的开始和结尾，以及内容就抽取完成了          
				continue                   
						
			if len(line.strip().split('\t')) == 6: #注释行
				annotation_dic[line.strip().split('\t')[1]] = line	#{实体的开始位置：注释行}
				continue
			
				
			# annotation_dic = {}
			# sent_list = []
			if line == '\n':
				n+=1	#判定一篇文章是否提取完，相当于分隔符
				
				sent_annos = []	#句子注释列表
				for sent_offset in sent_list:	#sent_list:{开始，结束，句子}
					for anno_start in annotation_dic.keys():	#annotation_dic={实体开始的位置：注释行具体内容}
						#判断实体是否在句子内
						if int(anno_start) >= int(sent_offset["begin"]) and int(anno_start) < int(sent_offset["end"]):
							#将判断为True的注释行加入零时列表
							sent_annos.append(annotation_dic[anno_start])
					#sent_offset['sent']==摘要内的句子
					sent_annotation[sent_offset["sent"]] = sent_annos	#sent_annotation	{句子内容：注释行列表}
					
					sent_annos = []	#列表清空
						  
				for each_sent in sent_annotation.keys():
											
					pattern = re.compile(r'\b%s\b' % (keyword))
					if pattern.search(each_sent.lower()) :
									#判断两个关键词是否在句子内（or）
									# print(each_sent,sent_annotation[each_sent])
									#if len(sent_annotation[each_sent]) >= 1:
									#at=标题信息
						with open(sent_report,'a+') as ot:
							ot.write(at+keyword+'\n')
							#写入判定为true的句子内容
							ot.write(each_sent+'\n')
							#sent_annotation的value为注释句
							for a in sent_annotation[each_sent]:
								#a为注释行句子
								ot.write('{0}'.format(a))
								#pmid加入articlenub
								articlenub.append(a.strip().split('\t')[0])
							ot.write('\n')
						#句子数量加一
						sentnub = sentnub + 1

				# print("\r", end="")
				# print('{}%'.format(str(int(100*n/whole))), "▋" * (int(100*n/whole)//2),str(n),"/",str(whole),end='')
				# time.sleep(0.05)

				#清空所有临时列表、字典，进行下一篇文章的提取
				sent_annotation ={}
				sent_list = []
				annotation_dic = {}
				# continue


	#提取统计
	# print('\n{0} sentences and {1} articles.'.format(sentnub,len(set(articlenub))))      
# filter_sent('mutation','rsid')

def work(z):
	print('1',end='')
	filter_sent(z[0],z[1],z[2])

if __name__ == '__main__':
	try:
		options,args=getopt.getopt(sys.argv[1:],"hi:w:o:")	
		if len(sys.argv)==1:
				usage()

		for name,fname in options:
			if name in ('-h'):
				usage()
			if name in ('-i'):
				target_pubtator = fname
				whole=0
				with open (target_pubtator) as ff:
					for line in ff:
						if line[8:11] == '|t|':
							whole+=1
			if name in ('-w'):
				wordlist=[]
				wordfile= fname
				
			if name in ('-o'):
				with open (wordfile) as ff:
					for line in ff:
						wordlist.append((line.strip().lower(),target_pubtator,fname))
				pool = Pool (10)
				pool.map(work,wordlist)
				pool.close()
				pool.join()
				# filter_sent()
	except getopt.GetoptError:
		usage()
print('time:'+str(time.time()-time1))