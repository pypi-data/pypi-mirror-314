# %%
import pandas as pd
import numpy as np
import json
import re
from icecream import ic
from pprint import  pprint
import os
from jcw_utils.string_utils import *
from jcw_utils.other import import_if_not_exists
# %%
import uuid

# %% [markdown]
# ## 读取pdf内容

# %%
import fitz  # PyMuPDF
def get_pdf_text(book_path)-> dict:
    '''
    返回
    [{'index_num': 0, 'text': ''}...]
    '''
    # 打开PDF文件
    pdf_document = fitz.open(book_path)
    book=[]
    # 获取总页数
    num_pages = pdf_document.page_count

    # 按页读取PDF内容
    for page_index in range(num_pages):
        # 获取页面对象
        page = pdf_document.load_page(page_index)
        
        # 获取页面文本
        page_text = page.get_text()
        
        book.append({'index_num':page_index,'text':page_text})
    # 关闭PDF文件
    pdf_document.close()
    ic(f'完成书本读取，共{len(book)}页')
    return book
# path=r'D:\learning\script\temp\book\Jeffrey M. Wooldridge - Introductory Econometrics_ A Modern Approach-Cengage Learning (2012)(2).pdf'
# book=get_pdf_text(path)
# path=r'E:\code\python\rag_1_东蔓健康\数据需求\677例眼科住院眼肿瘤病人的年龄分布特征_蒲黔梅.pdf'
# book=get_pdf_text(path)
# print(book[3])

from jcw_utils.file_utils import jsonl_dump
from jcw_utils.other import clear_print
ocr_package_flag=False
def ocr_pdf_text(pdf_path):
    '''
    读取pdf文件，返回文本
    '''
    # import_if_not_exists(['paddleocr','fitz','PIL','cv2'])
    global ocr_package_flag
    if ocr_package_flag==False:
        ocr_package_flag=True
        import os
        import cv2
        import numpy as np
        from paddleocr import PPStructure,save_structure_res
        from PIL import Image, ImageDraw
        # from paddle.utils import try_import
        from PIL import Image
    
    pdf_page_content=[]
    ocr_engine = PPStructure(table=False, ocr=True, show_log=True,type='ocr',lang='ch')
    imgs = []
    with fitz.open(pdf_path) as pdf:
        for page_index in range(0, pdf.page_count):
            page = pdf[page_index]
            mat = fitz.Matrix(2, 2)
            pm = page.get_pixmap(matrix=mat, alpha=False)

            # if width or height > 2000 pixels, don't enlarge the image
            if pm.width > 2000 or pm.height > 2000:
                pm = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)

            img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            imgs.append(img)
            
    ocr_page_results=[]
    for index, img in enumerate(imgs[:20]):
        ocr_page_results.append(ocr_engine(img))
        # break
        
    #这是保存为图片查看框选效果的代码
    # for index, result in enumerate(ocr_page_results):
    #     block_boxs_in_page=[]
    #     min_boxs_in_page=[]
    #     for block in result:
    #         block_boxs_in_page.append(block['bbox'])
    #         for min_text_info in block['res']:
    #             min_boxs_in_page.append([*min_text_info['text_region'][0],*min_text_info['text_region'][2]])
    #     img=cv2.resize(img,(img.shape[1],img.shape[0]))
    #     # Create a drawing object to draw on the image
    #     img=Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #     draw=ImageDraw.Draw(img)
    #     for bbox in block_boxs_in_page:
    #         draw.rectangle(bbox, outline=(255, 0, 0), width=3)
    #     for min_box in min_boxs_in_page:
    #         draw.rectangle(min_box, outline=(0, 0, 0), width=1)
    #     img.save(os.path.join('./output', f'annotated_{index}.png'))
    
    for index, page_result in enumerate(ocr_page_results):
        cur_block_text={'index_num':index,'texts':[]}
        #先按y轴排,再按x轴排
        page_result.sort(key=lambda x:(x['bbox'][1],x['bbox'][0]))
        for block in page_result:
            cur_block_text['texts'].append("\n".join([one['text'] for one in block['res']]))
            # clear_print(cur_block_text)
        
        pdf_page_content.append(cur_block_text)
        # clear_print(pdf_page_content)
    return pdf_page_content
# path=r'E:\code\python\rag_1_东蔓健康\数据需求\677例眼科住院眼肿瘤病人的年龄分布特征_蒲黔梅.pdf'
# path=r'E:\code\python\高频常用函数\OCR\pdf\index_page.pdf'
path=r'E:\高频常用函数\jcw_utils\data\pdf_data\chinese_paper.pdf'
book=ocr_pdf_text(path)
print(book)
# dump_jsonl(book,'ocr_pdf_text_glossary.json')
# print(book[3])

# %% [markdown]
# ## 设置pdf页码

# %%
def longest_increasing_subsequence(seq):
    if not seq:
        return []

    # 初始化一个数组，存储以每个元素结尾的最长递增子序列的长度
    dp = [1] * len(seq)
    # 初始化一个数组，存储最长递增子序列的前一个元素的索引
    prev = [-1] * len(seq)

    # 动态规划计算最长递增子序列的长度
    for i in range(1, len(seq)):
        for j in range(i):
            if seq[i] > seq[j] and dp[i] < dp[j] + 1:
                dp[i] = dp[j] + 1
                prev[i] = j

    # 找到最长递增子序列的最长长度
    max_length = max(dp)
    # 找到最长递增子序列的起始索引
    max_index = dp.index(max_length)
    # 回溯找到最长递增子序列
    lis = []
    while max_index != -1:
        lis.append(seq[max_index])
        max_index = prev[max_index]
    lis.reverse()
    return lis

# %%
def set_pdf_read_num(book):
    possible_total_read_num=[]
    for one_page in book:
        possible_read_num=0
        try:
            workpiece_text=one_page['text']
            workpiece_list=workpiece_text.split("\n")
            workpiece_block=''
            if len(workpiece_list)>10:
                workpiece_block="\n".join(workpiece_list[:5]+workpiece_list[-5:])
            else:
                workpiece_block="\n".join(workpiece_list)
            possible_read_num=re.findall(r'\b\d+\b',workpiece_block)[0]
        except Exception as e:
            ic(f'error when find num in this page 10 line{e}')
            pass
        possible_total_read_num.append(possible_read_num)
    # print(possible_total_read_num)
    # return possible_total_read_num
    
    possible_total_read_num=[int(a) for a in possible_total_read_num]
    specific_read_num=[]
    lis=longest_increasing_subsequence(possible_total_read_num)
    cur_lis_idx=0
    for pos_num in possible_total_read_num:
        cur_lis_num=lis[cur_lis_idx] if cur_lis_idx<=len(lis)-1 else 1e10
        if pos_num==cur_lis_num:
            specific_read_num.append(cur_lis_num)
            cur_lis_idx+=1
        else:
            specific_read_num.append(1 if len(specific_read_num)==0 else specific_read_num[-1]+1)
            
    for page,idx in zip(book,specific_read_num):
        page['read_num']=idx
            

# %%

def get_pdf_node(book,chunk_size=256,max_length=256*20):
    node={"doc_id":'xxx','node_id':'xxx','text':'xxx'}
    node.update({'index_num':0,"read_num":0})
    nodes=[]
    idx=0
    for page in book:
        text=page['text']
        texts=split_text(text,chunk_size=chunk_size,max_length=max_length)
        for one_text in texts:
            cur_uuid=generate_uuid_from_string(page['text']+str(idx))
            nodes.append({"node_id":cur_uuid,"text":one_text,"index":idx,"index_num":page['index_num'],"read_num":page['read_num']})
            idx+=1
    return nodes

# def generate_pdf_nodes(pdf_path):
#     book=get_pdf_text(pdf_path)
#     set_pdf_read_num(book)
#     nodes=get_pdf_node(book)
#     return nodes

def generate_uuid_from_string(input_string):
    # 使用命名空间 UUID（可以使用预定义的命名空间，如 NAMESPACE_DNS）
    namespace = uuid.NAMESPACE_DNS
    # 根据输入字符串和命名空间生成 UUID
    generated_uuid = uuid.uuid5(namespace, input_string)
    return str(generated_uuid)

def generate_pdf_nodes(path,chunk_size=256,max_length=256*20):
    '''
    output e.g.:
    [dict_keys(['node_id', 'text', 'index_num', 'read_num'])....]
    '''
    book=get_pdf_text(path)
    set_pdf_read_num(book)
    for page in book:
        page['text']=clean_sentence(page['text'])
        
    nodes=get_pdf_node(book,chunk_size=chunk_size,max_length=max_length)
    #give each node key file_path and value path
    for node in nodes:
        node['file_path']=path
    # for one in nodes:
    #     one['text']=one['text'].lower()
    # for node in nodes:
    #     node['text']=" ".join(tokenize_lemmatize(node['text']))
    return nodes


if __name__=='__main__':
    # path=r'D:\learning\script\temp\book\Jeffrey M. Wooldridge - Introductory Econometrics_ A Modern Approach-Cengage Learning (2012)(2).pdf'
    # nodes=generate_pdf_nodes(path)
    # ic(len(nodes))
    # df=pd.DataFrame(nodes)
    # df['lentext']=df['text'].apply(lambda x:len(x.split(" "))).tolist()
    # print(df.describe())
    # # for one in nodes:
    #     print(len(one['text']))
    
    pass

# %%
