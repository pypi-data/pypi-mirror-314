
import pandas as pd
import numpy as np
import json
import re
from icecream import ic

from lxml import etree
from docx import Document

# file_path=r'/home/recall/temp240715/rag_rebuild/0801_作业检查/work_corazon_4_Writing materials(1) - Copy.docx'
# file_path=r'/home/recall/temp240715/rag_rebuild/0801_作业检查/cho1_1_Services Marketing_2.docx'
def read_docx_xml_content(file_path):
    doc = Document(file_path)
    xml_content = doc._element.xml
    return xml_content


# 解析XML字符串

def find_element_childen(element,cur_p=False,namespaces='')->list:
    finded_elements=element.xpath('./w:sdt | ./w:p | ./w:r[.//w:t]',namespaces=namespaces)
    # ic(len(fined_elements))
    output=[]
    if len(finded_elements)==0:
        finded_elements=element.xpath('.//w:sdt | .//w:p',namespaces=namespaces)
    if len(finded_elements)==0:
        finded_elements=element.xpath('.//w:r[.//w:t]',namespaces=namespaces)
    for element in finded_elements:
        local_name = element.tag.split('}')[1] if '}' in element.tag else element.tag #p,sdt,r
        element_path=element.getroottree().getpath(element)
        cur_dict={'local_name':local_name,'element_path':element_path}
        if local_name=='r':#w:r下只有一个w:t
            w_t_string=element.xpath('.//w:t',namespaces=namespaces)[0].text
            w_rPrs=element.xpath('.//w:rPr',namespaces=namespaces)
            w_rPr_string=etree.tostring(w_rPrs[0], pretty_print=True).decode() if len(w_rPrs)>0 else ''
            w_b_find=re.findall(r'<w:b/>', w_rPr_string)
            w_b=1 if len(w_b_find)>0 else 0
            cur_dict['w_b']=w_b
            cur_dict['w_rPr_string']=w_rPr_string
            cur_dict['w_t_string']=w_t_string
        elif local_name=='p':
            content=find_element_childen(element,namespaces=namespaces)
            w_pPrs=element.xpath('./w:pPr',namespaces=namespaces)
            cur_dict['w_pPr']=etree.tostring(w_pPrs[0]).decode() if len(w_pPrs)>0 else ''
            pStyle=re.findall(r'<w:pStyle w:val="(.*?)"/>',cur_dict['w_pPr'])
            cur_dict['pStyle']=pStyle[0] if len(pStyle)>0 else '-1'
            # ic(pStyle)
            cur_dict['content']=content
        elif local_name=='sdt':
            content=find_element_childen(element,namespaces=namespaces)
            w_docPartGallery_find=element.xpath('.//w:docPartGallery/@w:val',namespaces=namespaces)
            cur_dict['docPartGallery_val']=w_docPartGallery_find[0] if len(w_docPartGallery_find)>0 else ''
            cur_dict['content']=content
        output.append(cur_dict)
    return output

def generate_para_content(node):
    cur_content=''

    if node['local_name']=='r':
        cur_content+=node['w_t_string']
    else:
        for one in node['content']:
            if node['local_name']=='p':
                cur_content+=generate_para_content(one)
            else:
                if cur_content=='':
                    cur_content+=generate_para_content(one)
                else:
                    cur_content=cur_content+'\n'+generate_para_content(one)
    return cur_content


def port_to_return(file_path):
    xml_string = read_docx_xml_content(file_path)
    docx_contents=[]
    xml_root = etree.fromstring(xml_string)
    namespaces={'w':re.findall(r'\{(.*?)\}',xml_root.tag)[0]}
    
    docx_contents=find_element_childen(xml_root.xpath('./w:body',namespaces=namespaces)[0],namespaces=namespaces)
    docx_content_p_sdt=[]

    reference_flag=0
    references=[]
    for node in docx_contents:
        if node['local_name']=='p':
            cur_content=generate_para_content(node)
            if 'reference' in cur_content[:20].lower() or reference_flag==1:
                if reference_flag==1:
                    references.append(cur_content)
                reference_flag=1
            else:
                docx_content_p_sdt.append(cur_content)
        elif node['local_name']=='sdt':
            if node['docPartGallery_val']=="Table of Contents":
                table_of_content=1
                continue
            else:
                cur_content=generate_para_content(node)
                if 'reference' in cur_content[:20].lower():
                    references=cur_content.split("\n")[1:]
                    references=[one for one in references if len(one)>5]
                else:
                    docx_content_p_sdt.append(cur_content)
    
    docx_content_p_sdt=[one for one in docx_content_p_sdt if len(one)>1]
    