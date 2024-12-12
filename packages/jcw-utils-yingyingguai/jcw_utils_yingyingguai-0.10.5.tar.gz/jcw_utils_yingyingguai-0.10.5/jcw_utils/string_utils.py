import pandas as pd
import numpy as np
import json
import re
from icecream import ic
from pprint import  pprint
import numpy
from tqdm import tqdm
import uuid
import inspect

def generate_uuid_from_string(input_string):
    namespace = uuid.NAMESPACE_DNS
    generated_uuid = uuid.uuid5(namespace, input_string)
    return str(generated_uuid)

## 最长公共字串
def longest_common_substring(s1, s2):
    """
    Finds the longest common substring between two input strings.

    Args:
    s1 (str): The first input string.
    s2 (str): The second input string.

    Returns:
    str: The longest common substring between s1 and s2.
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    longest_substr = ""
    max_length = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    longest_substr = s1[i - max_length:i]

    return longest_substr


def longestCommonSubsequence(text1: str, text2: str) -> int:
    '''
    最长公共子序列
    '''
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]
    
def mergingRatioInSubseq(s1,s2):
    s1=s1.lower()
    s2=s2.lower()
    if len(s1)+len(s2)==0:
        return 0
    intersection_len=longestCommonSubsequence(s1,s2)
    union_len=len(s1)+len(s2)
    ic(intersection_len)
    ic(union_len)
    return 2*intersection_len*(1/union_len)
# tests=[['aaa','aab'],['aaadddcccddd','dcccd'],['ajanahagatavba','azaxacavaban'],['acavaban','awaearat']]
# for test in tests:
#     print(longest_common_substring(test[0],test[1]))
#     print(longestCommonSubsequence(test[0],test[1]))
#     print(mergingRatioInSubseq(test[0],test[1]))

def lcs_sim_search(s1s,s2s,include_same=True,case_sensitive=False):
    '''
    include_same=True,返回idx时允许两个字符串一模一样
    case_sensitive=False，将字符串都变为小写比较
    '''
    if case_sensitive==False:
        s1s=[one.lower() for one in s1s]
        s2s=[one.lower() for one in s2s]
    idxs=[]
    scores=[]
    for s1 in s1s:
        cur_score=[]
        for s2 in s2s:
            cur_score.append(mergingRatioInSubseq(s1,s2))
        if include_same:
            cur_max_score=max(cur_score)
        else:
            cur_max_score=max([i for i in cur_score if abs(i-1)>0.001])
        cur_max_score_idx=cur_score.index(cur_max_score)
        idxs.append(cur_max_score_idx)
        scores.append(cur_max_score)
    return idxs,scores

class CustomSentenceTransformers():
    # 1. Load a pretrained Sentence Transformer model
    def __init__(self,modelpath=r'/home/recall/models/gte-large-en-v1.5'):
        import torch
        from sentence_transformers import SentenceTransformer,util
        self.device='cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(modelpath,trust_remote_code=True,device=self.device)
        self.model.to(self.device)
        
    def get_similarity(self,s1,s2):
        return util.pytorch_cos_sim(self.model.encode(s1),self.model.encode(s2)).item()

    def get_corpus_similarity(self,s1s,s2s):
        query_embedding = self.model.encode(s1s, convert_to_tensor=True,show_progress_bar=True,batch_size=1)
        corpus_embeddings = self.model.encode(s2s, convert_to_tensor=True,show_progress_bar=True,batch_size=1)
        hits = util.semantic_search(query_embedding, corpus_embeddings,query_chunk_size=1000,corpus_chunk_size=5000000,top_k=10)
        return hits

    def encode(self,sentence):
        return self.model.encode(sentence,device=self.device)

    def first_diff(self,s1,s2):
        hits=self.get_corpus_similarity(s1,s2)
        outidx=[]
        outscore=[]
        for k,line in enumerate(hits):
            for one in line:
                idx=one['corpus_id']
                score=one['score']
                if s2[idx]!=s1[k]:
                    outidx.append(idx)
                    outscore.append(score)
                    break
        return outidx,outscore
    # sentence1 = [
    #     "The weather is lovely today.",
    #     "It's so sunny outside!",
    #     "He drove to the stadium.",
    # ]
    # sentence2 = [
    #     "The weather is lovely1 today.",
    #     "It's so sun2ny outside!",
    #     "He drove to the stadium1.",
    # ]
    # first_diff(sentence1,sentence2)

    def get_similaritys(self,s1s,s2s):

        # s1s_embedding = self.model.encode(s1s, convert_to_tensor=True,show_progress_bar=True,batch_size=1)
        # s2s_embeddings = self.model.encode(s2s, convert_to_tensor=True,show_progress_bar=True,batch_size=1)
        # out=util.pytorch_cos_sim(s1s_embedding,s2s_embeddings)
        
        out=[]
        for i,j in tqdm(zip(s1s,s2s)):
            out.append(util.pytorch_cos_sim(self.model.encode(i,device=self.device),self.model.encode(j,device=self.device)).item())
        
        return out
    
class CustomRerank():
    def __init__(self,modelpath='/home/recall/models/bge-reranker-v2-m3'):
        from sentence_transformers.cross_encoder import CrossEncoder
        self.reranker_model = CrossEncoder(modelpath)

    def reranker_sen(self,query,corpus):
        '''
        output e.g.:
        [{'corpus_id': 0, 'score': 0.99990094},
        {'corpus_id': 3, 'score': 0.27255368},
        {'corpus_id': 2, 'score': 2.3667946e-05},
        {'corpus_id': 1, 'score': 1.8344432e-05}]
        '''
        ranks = self.reranker_model.rank(query, corpus)
        return ranks
    # query='what is panda?'
    # corpus=['what is panda?','no','yes','pandas']
    # ic(reranker_sen(query,corpus))

    def get_rerank_topn(self,query,corpus,topn):
        ranks=self.reranker_sen(query,corpus)
        str_list=[]
        if topn>len(corpus):
            print('找的topn大于语料的数量')
            return corpus
        for i in range(topn):
            str_list.append(corpus[ranks[i]['corpus_id']])
        return str_list
    # get_rerank_topn(query,corpus,2)
    
def clean_sentence(text2):
    # # 定义常用标点正则表达式
    # punctuation_pattern = r'[\.\,\!\?\'\"]'
    # # 使用正则表达式替换非常用标点的内容
    # text1 = re.sub(r'[^'+punctuation_pattern+']', '', text)
    # text2=re.sub(r'\t','\n',text)
    # text2=re.sub(r'\r','\n',text2)
    # text2=re.sub(r'[^\w,.!?]\n',' ',text2)#删除换行前不是字母或者标点的部分
    # text2=re.sub(r'\n+','\n',text2)
    # text2=re.sub(r'[\u200b-\u200d\u2028-\u2029\u200e-\u200f]',"",text2)#格式控制字符
    
    # text2=re.sub(r'\d','',text2)
    # text2=text2.replace("&",' and ')
    # text2=re.sub(r'[^a-zA-Z,\.\' \"\-–!?？！，]'," ",text2)#\(\)（）
    # text2=re.sub(r'[ ]+',' ',text2)
    # # text2=re.sub(r'[^\x00-\x7F]+',"",text2)
    
    # final_text=text2
    return text2
# texts=['\n\nnihao\n','ni-hao','\n','SSS \n \n \n \n BBB',"Adjusted R-Squared","cats & cat",
#        'nihao1243,535nihao','nihao             nihao',
#        'ni.hao,ni^hao&','has a form much like .\n\t \n\u202f\nAvar\u202f\n \n\u202f\n \n\u202f\n\u200a\n \n\u202f\n\u202f\ni\n\u202f\n\u202f\nn\n\u202f \n\u202f\nexpxi\u200a\n\u200a\n\u2009\n\u202f\nxi\nxi\u202f\n.\n.\nThe square roots of the diagonal elements of this matrix are the asymptotic standard errors. \nIf the Poisson assumption holds, we can drop \n\u202f\n from the formula because .\nAsymptotic standard errors for censored regression, truncated regression, and the \nHeckit sample selection correction are more complicated, although they share features \nwith the previous formulas. See Wooldridge for details.\nCopyright Cengage Learning. All Rights Reserved. May not be copied, scanned, or duplicated, in whole or in part. Due to electronic rights, some third party content may be suppressed from the eBook andor eChapters. Editorial review has \ndeemed that any suppressed content does not materially affect the overall learning experience. Cengage Learning reserves the right to remove additional content at any time if subsequent rights restrictions require it.',
#        ', has a form much like . Avar \n \n \n i\n n\n expxi \nxi\nxi \n.\n.\nThe square roots ',
#        'BBB\n\u202f\n\n\u200a\n \n\u202f\n\u202f\ni\n\u202f\n\u202fSAA']
# for text in texts:
#     out=clean_sentence(text)
#     # ic(out)
#     print(out)
#     print("*"*99)

class CustomNltk():
    def __init__(self):
        import nltk
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        from nltk.stem import WordNetLemmatizer
        # lemmatizer = WordNetLemmatizer()
        wordnet_lemmatizer = WordNetLemmatizer()
        from nltk.tokenize import sent_tokenize
        import jieba
        
    def tokenize_lemmatize(self,text):
        """
        去除停用词，小写化，词形还原为列表
        """
        #小写化
        text1=text.lower()

        #分词+词性还原
        from nltk.corpus import wordnet
        def get_pos_wordnet(pos_tag):
            pos_dict = {"N": wordnet.NOUN,
                        "V": wordnet.VERB,
                        "J": wordnet.ADJ,
                        "R": wordnet.ADV}
            return pos_dict.get(pos_tag[0].upper(), wordnet.NOUN)
        get_pos_wordnet('VBG')

        words=word_tokenize(text1)
        # ic(len(words))
        pos_tuples=nltk.pos_tag(words)
        words_lemed=[]
        for tup in pos_tuples:
            pos = get_pos_wordnet(tup[1])
            lemma = wordnet_lemmatizer.lemmatize(tup[0], pos=pos)
            words_lemed.append(lemma)
        # ic(len(words_lemed))

        #去停用词
        stop_words = set(stopwords.words('english'))
        final_words=[word for word in words_lemed if word not in stop_words]
        # ic(len(final_words))
        return final_words

    def split_text(self,text,chunk_size=256,max_length=256*20):
        try:
            # workpiece_list=text.split(".")
            # workpiece_list=[one+'.' for one in workpiece_list[:-1]]
            # workpiece_list = sent_tokenize(text)
            #judge if chinese char in text
            # if re.search(u'[\u4e00-\u9fff]', text):
            #     if auto_judge_language:
            english_char_count=len(re.findall(r'[a-zA-Z]',text))
            total_char_count=len(text)
            english_char_ratio=english_char_count/total_char_count
            if english_char_ratio>0.4:
                language='english'
            else:
                language='chinese'
            
            if language=='chinese':
                '''
                中文分句部分是从网上找到复制过来的, 在此基础上修改.
                chunk_size: 本意是单词个数,但是这里没做分词,假设一个词汇长度为4
                '''
                para=text
                para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
                para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
                para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
                para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
                # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
                para = para.rstrip()  # 段尾如果有多余的\n就去掉它
                # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
                workpiece_list= para.split("\n")
                max_length=chunk_size*4
            else:
                workpiece_list=sent_tokenize(text,language='english')
            
            # ic(len(workpiece_list))
            workpiece_list2=[]
            # ic(len(workpiece_list))
            cur_block=''
            for workpiece in workpiece_list:
                cur_block+=workpiece
                if len(cur_block.split(" "))>chunk_size or len(cur_block)>max_length:
                    workpiece_list2.append(cur_block)
                    cur_block=''
            if cur_block!='':
                workpiece_list2.append(cur_block)
            
        except Exception as e:
            ic(f'error when spilt text{e}')
            workpiece_list2=[text]
        return workpiece_list2

    def text_segmentation(self,text,auto_judge_language=True,language='english'):
        '''
        由于存在中医混杂的问题,这里从英文字母百分比判断是否是英文
        '''
        if text==None or text=='':
            return []
        #count english char
        if auto_judge_language:
            english_char_count=len(re.findall(r'[a-zA-Z]',text))
            total_char_count=len(text)
            english_char_ratio=english_char_count/total_char_count
            if english_char_ratio>0.4:
                language='english'
            else:
                language='chinese'
        
            if language=='chinese':
                words=jieba_segmentation(text)
            elif language=='english':
                words=tokenize_lemmatize(text)
        elif language=='english':
            words=tokenize_lemmatize(text)
        else:
            words=jieba_segmentation(text)
        # ic(words)
        return words
        
import hashlib
def get_string_md5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest() 

# jieba.enable_paddle()# 启动paddle模式。 0.40版之后开始支持，早期版本不支持
def jieba_segmentation(text):
    import jieba
    words=jieba.cut(text)
    return  list(words)
# texts=['我来到北京清华大学','小明硕士毕业于中国科学院计算所，后在日本京都大学深造']
# for text in texts:
#     print(jieba_segmentation(text))
    

import re
def remove_puncts(sentence):
    puncts='\\\/!"#$%&\'()*+,-./:;<=>?@\[\]^_`{|}~ ＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､　、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·．！？｡。'
    return re.sub(f'[{puncts}]','',sentence)
# print(remove_puncts('我来,到北\ /京清华大学'))
def chinese_punctuation_to_english(text):
    # 创建一个转换表，将中文标点映射到英文标点
    trans_table = str.maketrans({
        '，': ',',  # 逗号
        '。': '.',  # 句号
        '！': '!',  # 感叹号
        '？': '?',  # 问号
        '；': ';',  # 分号
        '：': ':',  # 冒号
        '《': '"',  # 左书名号
        '》': '"',  # 右书名号
        '“': '"',  # 左引号
        '”': '"',  # 右引号
        '‘': "'",  # 左单引号
        '’': "'",  # 右单引号
        '、': ',',  # 顿号
        '（': '(',  # 左圆括号
        '）': ')',  # 右圆括号
        '【': '[',  # 左方括号
        '】': ']',  # 右方括号
        '〔': '[',  # 左大括号
        '〕': ']',  # 右大括号
        '…': '...',  # 省略号
        '—': '-',  # 破折号
        '《': '<',  # 左尖括号
        '》': '>',  # 右尖括号
    })
    
    # 使用转换表转换文本
    return text.translate(trans_table)
# text = "这是一个测试文本，包含中文标点符号！包括（圆括号）、【方括号】、《书名号》等。"
# translated_text = chinese_punctuation_to_english(text)
# print(translated_text)