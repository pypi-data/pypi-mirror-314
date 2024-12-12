import pandas as pd
import numpy as np
import json
import re
from icecream import ic
import time
import requests
from pathlib import Path
import openai


def json_llm():
    '''
    仅用作参考的引导预填模式，根据具体场景做修改
    '''
    JSON_PARTIAL = """
    {
        "source": "%s", 
        "target": "%s", 
        "relationship": \""""
    def generate(kp1,kp1_info, kp2,kp2_info):
        form = json.dumps({"source": "xx", "target": "xx", "relationship": "$rel"})
        p = "You're expert in build knowledge graph, now you have two entities and each have a reference text, judge the " \
            "relationship between the two entities. The candidate relationships are " \
            "[include, included, parallel, irrelevant] and you can only chose a relationship from the candidate but no " \
            f"other relationships. The generated triple should be in JSON format: {form}\n" \
            f"Head entity: `{kp1}`\n with info:`{kp1_info}`\n Tail entity: `{kp2}`\n with info: \n`{kp2_info}\n`\nTriple:\n"
        partial = JSON_PARTIAL % (kp1, kp2)
        messages = [
            {"role": "user", "content": p},
            {"role": "assistant", "content": partial, "partial": True}
        ]
        
        completion = client.chat.completions.create(
            model = "moonshot-v1-8k",
            messages =messages,
            temperature = 0.3,)
        reply=completion.choices[0].message.content
        ret_json = partial + reply
        return ret_json
    generate('interesting','jfoiaejfauefhaiuhvosid','tire','jadfhapueghp')

#自定义语言模型
from pathlib import Path
from openai import OpenAI
client = OpenAI(
    api_key = "sk-xKxhsclFENnyOHvNFJhqeIM1HJiQEOGcuSyOrhecWnWqfaWr",
    base_url = "https://api.moonshot.cn/v1",
)
def get_reply(content,temperature=0.6):
    """
    需要自己调prompt
    """
    reply=''
    for _ in range(2):
        try:
            completion = client.chat.completions.create(
            model = "moonshot-v1-8k",
            messages = [
                {"role": "system", "content": "You are Kimi, the AI assistant provided by Moonshot AI, and you are better at Chinese and English conversations. You will provide users with safe, helpful, accurate answers. At the same time, you will refuse to answer any questions about terrorism, racism, pornography, etc. Moonshot AI is a proper term and cannot be translated into other languages."},
                {"role": "user", "content": f"{content}"},
            ],
            temperature = temperature,)
            reply=completion.choices[0].message.content
            break
        except Exception as e:
            print(e)
            time.sleep(5)
            pass
    return reply

def parse_square_brackets_in_str(str1:str)->list:
    refinds=re.findall(r'\[[^\[\]]*\]',str1)
    # ic(refinds[0])
    output=[]
    all_parse=True
    for rf in refinds:
        try:
            l=json.loads(rf)
            output.append(l)
        except Exception as e:
            print('解析llm回答时出错了')
            all_parse=False
            continue
    return output,all_parse


"""
AWS代理的OpenAI请求
"""
import json
import time
from datetime import datetime
import requests
import hashlib

class OpenAIAWS:
    def __init__(self, private_key=None):
        self.req_url = "http://ec2-44-228-232-207.us-west-2.compute.amazonaws.com:19810/chat_completion"
        if private_key is not None:
            self.private_key = private_key
        else:
            self.private_key = "0dc72489e718c93b02618d8c5a7ba6b4"

    def chat_completion(self, messages, model=None, json_mode=False, max_retry=3):
        biz_params = {
            "messages": messages,
            "model": model
        }
        if json_mode:
            biz_params["response_format"] = {"type": "json_object"}
        biz_params = json.dumps(biz_params, ensure_ascii=False)
        timestamp = str(int(datetime.now().timestamp() * 1000))
        sign = hashlib.md5((biz_params + timestamp + self.private_key).encode("utf-8")).hexdigest()

        payload = {
            "biz_params": biz_params,
            "timestamp": timestamp,
            "sign": sign
        }

        status, raw_resp = -1, {}
        for i in range(max_retry):
            resp = requests.post(self.req_url, json=payload).json()
            status, raw_resp = resp["status"], resp["data"]
            if status == 0:
                break
            else:
                time.sleep(5)
        if status != 0:
            err_msg = str(raw_resp)
            raise RuntimeError(f"Failed to request aws-openai after {max_retry} attempts with message: `{err_msg}`")
        return raw_resp

def req_model(input):
    cli = OpenAIAWS()
    instruction = input
    messages = [
        {"role": "user", "content": instruction},
    ]
    model_ret = cli.chat_completion(messages=messages, model="gpt-4o-mini")
    model_ret = json.loads(model_ret)["choices"][0]["message"]["content"]
    # json_str = model_ret.split("```json")[1].split("```")[0]
    return model_ret