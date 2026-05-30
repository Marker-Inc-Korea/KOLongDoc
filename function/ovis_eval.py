import os
import pandas as pd
import json
import random
import torch

from tqdm import tqdm

import pathlib
import ast
import fitz

from PIL import ImageFile, Image
ImageFile.LOAD_TRUNCATED_IMAGES = True

#from openai import OpenAI
#from huggingface_hub import InferenceClient

system_prompt = '''당신은 제공된 한국어 문서에만 기반하여 질문에 답하는 신뢰할 수 있는 어시스턴트입니다.
단편적인 검색을 넘어, 문서 내 여러 정보를 논리적으로 연결하고 종합(Multi-hop reasoning)하여 완성도 높은 답변을 도출하세요.
제공된 문서에서 근거를 찾을 수 없는 내용은 절대 지어내지 말고(환각 방지), 반드시 "제공된 문서에서는 해당 내용을 찾을 수 없습니다"라고 명확히 밝혀야 합니다.
'''

def model_inference(model, text_tokenizer, visual_tokenizer, messages, images, max_new_tokens):
    
    # format conversation
    max_partition = 4
    prompt, input_ids, pixel_values = model.preprocess_inputs(messages, images, max_partition=max_partition)
    attention_mask = torch.ne(input_ids, text_tokenizer.pad_token_id)
    input_ids = input_ids.unsqueeze(0).to(device=model.device)
    attention_mask = attention_mask.unsqueeze(0).to(device=model.device)
    if pixel_values is not None:
        pixel_values = pixel_values.to(dtype=visual_tokenizer.dtype, device=visual_tokenizer.device)
    pixel_values = [pixel_values]

    # generate output
    with torch.inference_mode():
        gen_kwargs = dict(
            max_new_tokens=max_new_tokens,
            do_sample=False,
            top_p=0.95,
            top_k=20,
            temperature=1.0,
            repetition_penalty=None,
            eos_token_id=model.generation_config.eos_token_id,
            pad_token_id=text_tokenizer.pad_token_id,
            use_cache=True
        )
        output_ids = model.generate(input_ids, pixel_values=pixel_values, attention_mask=attention_mask, **gen_kwargs)[0]
        content = text_tokenizer.decode(output_ids, skip_special_tokens=True)

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


def evaluate_test_image(model, text_tokenizer, visual_tokenizer, model_name, dataset_path, image_path, test_df, pdf_list, save_file_name):

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
        img_path_list = []
        for img_name in pdf_img_list:
            img_path_list.append(Image.open(f"{pdf_img_path}/{img_name}").convert("RGB"))
        assert len(img_path_list) == len(pdf_img_list), "wrong dataset files. please check."

        ###
        query = f'{'\n'.join([f'Image {i+1}: <image>' for i in range(len(img_path_list))])}\n{system_prompt}\n질문: {question}'
        print(f'queestion: {question}')
        print(f'Keyword: {gt_keyword}; {len(gt_keyword)}')

        output = model_inference(model, text_tokenizer, visual_tokenizer, query, img_path_list, max_new_tokens=8192)
        
        # check accuracy
        accuracy = eval_acc(output, gt_keyword)
        print(f'Acc: {accuracy}')

        df_answer.loc[i] = [pdf_name, question, gt_answer, gt_keyword, output, accuracy]
        df_answer.to_excel(save_file_name, index=False)

def evaluate_test_text(model, text_tokenizer, visual_tokenizer, model_name, dataset_path, image_path, test_df, pdf_list, save_file_name):

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

        output = model_inference(model, text_tokenizer, visual_tokenizer, query, images=None, max_new_tokens=8192)
        
        # check accuracy
        accuracy = eval_acc(output, gt_keyword)
        print(f'Acc: {accuracy}')

        df_answer.loc[i] = [pdf_name, question, gt_answer, gt_keyword, output, accuracy]
        df_answer.to_excel(save_file_name, index=False)