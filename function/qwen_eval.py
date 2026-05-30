import os
import pandas as pd
import json
import random

from tqdm import tqdm

import pathlib
import ast
import fitz

#from openai import OpenAI
#from huggingface_hub import InferenceClient

system_prompt = '''당신은 제공된 한국어 문서에만 기반하여 질문에 답하는 신뢰할 수 있는 어시스턴트입니다.
단편적인 검색을 넘어, 문서 내 여러 정보를 논리적으로 연결하고 종합(Multi-hop reasoning)하여 완성도 높은 답변을 도출하세요.
제공된 문서에서 근거를 찾을 수 없는 내용은 절대 지어내지 말고(환각 방지), 반드시 "제공된 문서에서는 해당 내용을 찾을 수 없습니다"라고 명확히 밝혀야 합니다.
'''

# https://github.com/QwenLM/Qwen3
def model_inference(model, tokenizer, messages, max_new_tokens):

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # conduct text completion
    generated_ids = model.generate(
        **model_inputs,
        temperature=1.0,
        top_p=0.95,
        top_k=20,
        #presence_penalty=0.0,
        repetition_penalty=1.0,
        min_p=0.0,
        max_new_tokens=max_new_tokens,
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

    # parsing thinking content
    try:
        # rindex finding 248069 (</think>); Qwen3.6 and 3.5
        index = len(output_ids) - output_ids[::-1].index(248069)
    except ValueError:
        index = 0

    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

    #print("thinking content:", thinking_content)  # no opening <think> tag
    print("content:", content)

    return content

def eval_acc(output, gt_keyword):
    clean_output = output.replace(',', '') # 1089 = 1,089

    point = 0
    for key in gt_keyword:
        key_str = str(key)
        clean_key = key_str.replace(',', '')

        if clean_key in clean_output:
            point += 1

    return point / len(gt_keyword)


def evaluate_test_image(model, tokenizer, model_name, dataset_path, image_path, test_df, pdf_list, save_file_name):

    if '3.5' in model_name:
        presence_penalty_parameter = 1.5
    elif '3.6' in model_name:
        presence_penalty_parameter = 0.0

    #'''
    if save_file_name.split("/")[-1] in os.listdir(f'{dataset_path}/eval'):
        df_answer = pd.read_excel(save_file_name)
        pass_len = len(df_answer)
    else:
        df_answer = pd.DataFrame(columns=['pdf', 'question', 'gt_answer', 'gt_keyword', 'model_answer', 'accuracy'])
        pass_len = 0

    # first, evaluate to less_pdf_list
    # (images) input version    
    for i in tqdm(range(len(test_df))):

        if i < pass_len:
            continue
        
        # ready
        pdf_name = test_df.iloc[i, 0]
        question = test_df.iloc[i, 1]
        gt_answer = test_df.iloc[i, 2]
        gt_keyword = test_df.iloc[i, -1]

        # 실제 리스트로 변환
        gt_keyword = ast.literal_eval(gt_keyword)

        print(f'pdf name: {pdf_name}')
        assert pdf_name in pdf_list, f'check the files {pdf_name}'

        # ready for test
        pdf_img_path = f"{image_path}/{pdf_name[:-4]}"
        pdf_img_list = os.listdir(pdf_img_path)
        pdf_img_list = sorted(
            [f for f in pdf_img_list if f.endswith(".png")],
            key=lambda x: int(x.split(".")[0])
        ) # sorting
        img_bytes_list = []
        for img_name in pdf_img_list:
            with open(f"{pdf_img_path}/{img_name}", 'rb') as f:
                image_bytes = f.read()
                img_bytes_list.append(image_bytes)
        assert len(img_bytes_list) == len(pdf_img_list), "wrong dataset files. please check."

        ###
        query = f'{system_prompt}\n질문: {question}'
        print(f'queestion: {question}')
        print(f'Keyword: {gt_keyword}; {len(gt_keyword)}')

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": pdf_img_list,
                    },
                    {
                        "type": "text",
                        "text": query,
                    }
                ]
            }
        ]

        output = model_inference(model, tokenizer, messages, max_new_tokens=8192)
        
        # check accuracy
        accuracy = eval_acc(output, gt_keyword)
        print(f'Acc: {accuracy}')

        df_answer.loc[i] = [pdf_name, question, gt_answer, gt_keyword, output, accuracy]
        df_answer.to_excel(save_file_name, index=False)

def evaluate_test_text(model, tokenizer, model_name, dataset_path, image_path, test_df, pdf_list, save_file_name):

    if '3.5' in model_name:
        presence_penalty_parameter = 1.5
    elif '3.6' in model_name:
        presence_penalty_parameter = 0.0

    #'''
    if save_file_name.split("/")[-1] in os.listdir(f'{dataset_path}/eval'):
        df_answer = pd.read_excel(save_file_name)
        pass_len = len(df_answer)
    else:
        df_answer = pd.DataFrame(columns=['pdf', 'question', 'gt_answer', 'gt_keyword', 'model_answer', 'accuracy'])
        pass_len = 0

    # first, evaluate to less_pdf_list
    # (images) input version    
    for i in tqdm(range(len(test_df))):

        if i < pass_len:
            continue
        
        # ready
        pdf_name = test_df.iloc[i, 0]
        question = test_df.iloc[i, 1]
        gt_answer = test_df.iloc[i, 2]
        gt_keyword = test_df.iloc[i, -1]

        # 실제 리스트로 변환
        gt_keyword = ast.literal_eval(gt_keyword)

        print(f'pdf name: {pdf_name}')
        assert pdf_name in pdf_list, f'check the files {pdf_name}'

        filepath = pathlib.Path(f'{image_path}/{pdf_name}')

        # pymuPDF
        pymupdf_doc = fitz.open(filepath)
        print(f"--- Extracting text from {filepath} ---")
        pdf_text = ""
        for page_num in range(len(pymupdf_doc)):
            page = pymupdf_doc[page_num]
            pdf_text += page.get_text("text")

        ###
        query = f'{pdf_text}\n\n{system_prompt}\n질문: {question}'
        print(f'question: {question}')
        print(f'Keyword: {gt_keyword}; {len(gt_keyword)}')

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": query
                    }
                ]
            }
        ]

        output = model_inference(model, tokenizer, messages, max_new_tokens=8192)
        
        # check accuracy
        accuracy = eval_acc(output, gt_keyword)
        print(f'Acc: {accuracy}')

        df_answer.loc[i] = [pdf_name, question, gt_answer, gt_keyword, output, accuracy]
        df_answer.to_excel(save_file_name, index=False)