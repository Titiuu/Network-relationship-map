import jieba
import jieba.posseg as pseg
from jieba import analyse
tfidf = analyse.extract_tags
import csv
from gensim.models import word2vec, keyedvectors

# changes
stopwords = ['吕州', '林城', '银行卡', '安置费', '任重道远',
             '孤鹰岭', '阿庆嫂', '岳飞', '养老院', '老总']
replace_words = {'师母': '吴慧芬', '陈老': '陈岩石', '老赵': '赵德汉', '达康': '李达康', '高总': '高小琴',
                 '猴子': '侯亮平', '老郑': '郑西坡', '小艾': '钟小艾', '老师': '高育良', '同伟': '祁同伟',
                 '赵公子': '赵瑞龙', '郑乾': '郑胜利', '孙书记': '孙连城', '赵总': '赵瑞龙', '昌明': '季昌明',
                 '沙书记': '沙瑞金', '郑董': '郑胜利', '宝宝': '张宝宝', '小高': '高小凤', '老高': '高育良',
                 '伯仲': '杜伯仲', '老杜': '杜伯仲', '老肖': '肖钢玉', '刘总': '刘新建', "美女老总": "高小琴"}
lines = []  # 句子列表，当两个人物同时出现在一个句子时，我们认为两者有关系
names = {}  # 姓名字典
relationships = {}  # 关系字典
lineNames = []  # 每句内人物的关系
node = []  # 存放处理后的人物

jieba.load_userdict("person.txt")  # 加载人物字典
f = open("drama.txt", 'r', encoding='utf-8')  # 读入剧本
for paragragh in f.readlines():
    if len(paragragh) > 20:  # 去除标题和空行
        gets = paragragh.split('。')  # 分割句子
        lines += gets[0:-2]
# for line in lines:
#     poss = pseg.cut(line)  # 分词并返回该词词形
#     lineNames.append([])  # 为新读入的一段添加人物名称列表
#     for w in poss:
#         if w.word in stopwords:  # 去掉某些停用词
#             continue
#         if w.flag != "nr" or len(w.word) < 2:  # 去指代词和非人名词
#             if w.word not in replace_words:
#                 continue
#         if w.word in replace_words:  # 将某些在文中人物的昵称替换成正式的名字
#             w.word = replace_words[w.word]
#         lineNames[-1].append(w.word)  # 为当前句子增加一个人物
#         if names.get(w.word) is None:  # 如果这个名字从来没出现过，初始化这个名字
#             names[w.word] = 0
#             relationships[w.word] = {}
#         names[w.word] += 1  # 该人物出现次数加1
# for line in lineNames:  # 通过对于每一句句内关系的累加，得到全部关系
#     for name1 in line:
#         for name2 in line:
#             if name1 == name2:
#                 continue
#                 # 如果没有出现过两者之间的关系，则新建项
#             if relationships[name1].get(name2) is None:
#                 relationships[name1][name2] = 1
#             else:
#                 relationships[name1][name2] += 1  # 如果两个人已经出现过，则亲密度加1

# # 写csv文件
# # 在windows这种使用\r\n的系统里，不用newline=‘’的话
# # 会自动在行尾多添加个\r，导致多出一个空行，即行尾为\r\r\n
# csv_edge_file = open("edge.csv", "w", newline="")
# writer = csv.writer(csv_edge_file)
# # 先写入列名,"type"为生成无向图做准备
# writer.writerow(["source", "target", "weight", "type"])
# for name, edges in relationships.items():
#     for v, w in edges.items():
#         if w > 20:
#             node.append(name)
#             writer.writerow((name, v, str(w), "undirected"))  # 按行写入数据
# csv_edge_file.close()
# #生成node文件
# s = set(node)
# csv_node_file = open("node.csv", "w", newline="")
# wnode = csv.writer(csv_node_file)
# wnode.writerow(["ID", "Label", "Weight"])
# for name, times in names.items():
#     if name in s:
#         wnode.writerow((name, name, str(times)))
# csv_node_file.close()

# TF-IDF特征提取关键词分析
content = open("drama.txt", 'r', encoding='utf-8').read()
keywords = tfidf(content, topK=10)
print(keywords)

# word2vec相关词分析
stopwords = [] 
stopword_lines = open('cn_stopwords.txt', 'r', encoding='utf-8').readlines()
for line in stopword_lines:
    stopwords.append(line.strip())
sentences = []
for line in lines:
    words = list(jieba.cut(line))
    words_without_stopwords = []
    for word in words:
        if word not in stopwords:
            words_without_stopwords.append(word)
    sentences.append(words_without_stopwords)

model = word2vec.Word2Vec(sentences)

# 这里我们输出相似度最高的10个词
for k,s in model.wv.most_similar('侯亮平', topn=10):
    print (k,s)

