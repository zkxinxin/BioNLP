#Author Lisheng
from Bio import Entrez #调包
import time
Entrez.email='1826961265@qq.com' #设置访问时的邮箱地址

def work(gene): #搜索函数，返回id列表
	handle=Entrez.esearch(db='gene',term='%s AND Oryza sativa'%(gene))
	record=Entrez.read(handle)
	tmp=[]
	for i in record['IdList']:
		if i in idlist:
			tmp.append(i)
	return tmp


idlist=[]#建立水稻基因参考列表
with open (r'C:\Users\RichenLee\Desktop\文稿\bioNLP\data\gene\rice_id.txt') as ff:
	for line in ff:
		idlist.append(line.strip())

#写入文件
with open('Os.txt') as ff:
	n=0
	for line in ff:
		n+=1
		if n>=4125:
			with open('name_id.txt','a+') as ot:						
				print('---------%s---------' % (n))
				gene=line.strip()
				geneid=work(gene)
				word=''
				for i in geneid:
					word+=i+',' 
				# print(gene+'\t'+word+'\n')
				ot.write(gene+'\t'+word+'\n')
			time.sleep(1)



