import os
import fire
import pandas as pd

import torch

from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoProcessor, AutoModelForImageTextToText, AutoModel, LlavaOnevisionForConditionalGeneration, MllamaForConditionalGeneration, MllamaProcessor

def main(
    test_type=None,
    base_model=None,
    thinking_mode=False,
    huggingface_token: str | None = None,
    dataset_path= None,
    image_path= None,
    cutoff_len=8192,
):
    
    print(f'############################### {base_model} ###############################')

    if huggingface_token is not None:
        login(token=huggingface_token)

    ## dataset loading
    l_problem = pd.read_excel(f'{dataset_path}/KLongDocURL_L_ver1.xlsx')
    sl_problem = pd.read_excel(f'{dataset_path}/KLongDocURL_SL_ver1.xlsx')

    less_pdf_list = [pdf for pdf in os.listdir(f'{image_path}/less_60') if '.pdf' in pdf]
    more_pdf_list = [pdf for pdf in os.listdir(f'{image_path}/more_60') if '.pdf' in pdf]

    save_file_name_l = f'{dataset_path}/eval/{base_model.split('/')[-1]}_image_long.xlsx'
    save_file_name_sl = f'{dataset_path}/eval/{base_model.split('/')[-1]}_image_super_long.xlsx'

    save_file_name_l_text = f'{dataset_path}/eval/{base_model.split('/')[-1]}_text_long.xlsx'
    save_file_name_sl_text = f'{dataset_path}/eval/{base_model.split('/')[-1]}_text_super_long.xlsx'

    ## Model loading
    device_map = "auto"

    # torch 2.4.0+cu124
    # transformers 5.2.0
    if 'Qwen3.6' in base_model:
        # load the tokenizer and the model
        tokenizer = AutoTokenizer.from_pretrained(base_model)
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            dtype=torch.bfloat16,
            device_map="auto"
        )

        from function.qwen_eval import evaluate_test_image, evaluate_test_text

        # image-based test
        evaluate_test_image(model, tokenizer, base_model, dataset_path, f'{image_path}_image/less_60', l_problem, less_pdf_list, save_file_name_l)
        evaluate_test_image(model, tokenizer, base_model, dataset_path, f'{image_path}_image/more_60', sl_problem, more_pdf_list, save_file_name_sl)

        # test-based test
        evaluate_test_text(model, tokenizer, base_model, dataset_path, f'{image_path}/less_60', l_problem, less_pdf_list, save_file_name_l_text)
        evaluate_test_text(model, tokenizer, base_model, dataset_path, f'{image_path}/more_60', sl_problem, more_pdf_list, save_file_name_sl_text)

    elif 'Qwen3.5' in base_model:
        # load the tokenizer and the model
        tokenizer = AutoTokenizer.from_pretrained(base_model)
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            dtype=torch.bfloat16,
            device_map="auto"
        )

        from function.qwen_eval import evaluate_test_image, evaluate_test_text

        # image-based test
        evaluate_test_image(model, tokenizer, base_model, dataset_path, f'{image_path}_image/less_60', l_problem, less_pdf_list, save_file_name_l)
        evaluate_test_image(model, tokenizer, base_model, dataset_path, f'{image_path}_image/more_60', sl_problem, more_pdf_list, save_file_name_sl)

        # test-based test
        evaluate_test_text(model, tokenizer, base_model, dataset_path, f'{image_path}/less_60', l_problem, less_pdf_list, save_file_name_l_text)
        evaluate_test_text(model, tokenizer, base_model, dataset_path, f'{image_path}/more_60', sl_problem, more_pdf_list, save_file_name_sl_text)

    # torch 2.6.0+cu124 (cu118)
    # transformers 5.8.0
    elif 'gemma-4' in base_model:
        
        # Load model
        processor = AutoProcessor.from_pretrained(base_model)
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            dtype=torch.bfloat16,
            device_map="auto",
        )

        from function.gemma_eval import evaluate_test_image, evaluate_test_text

        # image-based test
        evaluate_test_image(model, processor, base_model, dataset_path, f'{image_path}_image/less_60', l_problem, less_pdf_list, save_file_name_l)
        evaluate_test_image(model, processor, base_model, dataset_path, f'{image_path}_image/more_60', sl_problem, more_pdf_list, save_file_name_sl)

        # test-based test
        evaluate_test_text(model, processor, base_model, dataset_path, f'{image_path}/less_60', l_problem, less_pdf_list, save_file_name_l_text)
        evaluate_test_text(model, processor, base_model, dataset_path, f'{image_path}/more_60', sl_problem, more_pdf_list, save_file_name_sl_text)

    # torch 2.6.0+cu124
    # transformers 5.8.0
    elif 'EXAONE-4.5' in base_model:

        processor = AutoProcessor.from_pretrained(base_model)
        model = AutoModelForImageTextToText.from_pretrained(
            base_model,
            dtype=torch.bfloat16,
            device_map="auto",
        )

        from function.exaone_eval import evaluate_test_image, evaluate_test_text

        # image-based test
        evaluate_test_image(model, processor, base_model, dataset_path, f'{image_path}_image/less_60', l_problem, less_pdf_list, save_file_name_l)
        evaluate_test_image(model, processor, base_model, dataset_path, f'{image_path}_image/more_60', sl_problem, more_pdf_list, save_file_name_sl)

        # test-based test
        evaluate_test_text(model, processor, base_model, dataset_path, f'{image_path}/less_60', l_problem, less_pdf_list, save_file_name_l_text)
        evaluate_test_text(model, processor, base_model, dataset_path, f'{image_path}/more_60', sl_problem, more_pdf_list, save_file_name_sl_text)

    # torch 2.4.0+cu124
    # transformers 5.5.0
    elif 'VARCO-VISION-2.0' in base_model:
        model = LlavaOnevisionForConditionalGeneration.from_pretrained(
            base_model,
            dtype=torch.bfloat16,
            device_map=device_map,
        )

        processor = AutoProcessor.from_pretrained(base_model, device_map=device_map)

        from function.varco_eval import evaluate_test_image, evaluate_test_text

        # image-based test
        evaluate_test_image(model, processor, base_model, dataset_path, f'{image_path}_image/less_60', l_problem, less_pdf_list, save_file_name_l)
        evaluate_test_image(model, processor, base_model, dataset_path, f'{image_path}_image/more_60', sl_problem, more_pdf_list, save_file_name_sl)

        # test-based test
        evaluate_test_text(model, processor, base_model, dataset_path, f'{image_path}/less_60', l_problem, less_pdf_list, save_file_name_l_text)
        evaluate_test_text(model, processor, base_model, dataset_path, f'{image_path}/more_60', sl_problem, more_pdf_list, save_file_name_sl_text)

    # torch 2.4.0+cu124
    # transformers 4.46.2
    elif 'Gukbap-Ovis2' in base_model:
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            device_map=device_map,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            multimodal_max_length=8192 # 2048
        )

        text_tokenizer = model.get_text_tokenizer()
        visual_tokenizer = model.get_visual_tokenizer()

        from function.ovis_eval import evaluate_test_image, evaluate_test_text

        # image-based test
        evaluate_test_image(model, text_tokenizer, visual_tokenizer, base_model, dataset_path, f'{image_path}_image/less_60', l_problem, less_pdf_list, save_file_name_l)
        evaluate_test_image(model, text_tokenizer, visual_tokenizer, base_model, dataset_path, f'{image_path}_image/more_60', sl_problem, more_pdf_list, save_file_name_sl)

        # test-based test
        evaluate_test_text(model, text_tokenizer, visual_tokenizer, base_model, dataset_path, f'{image_path}/less_60', l_problem, less_pdf_list, save_file_name_l_text)
        evaluate_test_text(model, text_tokenizer, visual_tokenizer, base_model, dataset_path, f'{image_path}/more_60', sl_problem, more_pdf_list, save_file_name_sl_text)
    
    # torch 2.4.0+cu124
    # transformers 5.5.0
    elif 'Bllossom-AICA' in base_model:
        model = MllamaForConditionalGeneration.from_pretrained(
            base_model,
            dtype=torch.bfloat16,
            device_map='auto'
        ).cuda()
        processor = MllamaProcessor.from_pretrained(base_model)

        from function.bllossom_eval import evaluate_test_image, evaluate_test_text

        # image-based test
        evaluate_test_image(model, processor, base_model, dataset_path, f'{image_path}_image/less_60', l_problem, less_pdf_list, save_file_name_l)
        evaluate_test_image(model, processor, base_model, dataset_path, f'{image_path}_image/more_60', sl_problem, more_pdf_list, save_file_name_sl)

        # test-based test
        evaluate_test_text(model, processor, base_model, dataset_path, f'{image_path}/less_60', l_problem, less_pdf_list, save_file_name_l_text)
        evaluate_test_text(model, processor, base_model, dataset_path, f'{image_path}/more_60', sl_problem, more_pdf_list, save_file_name_sl_text)

    else:
        raise NotImplementedError("Not implementation!!")


if __name__ == "__main__":
    torch.cuda.empty_cache()
    fire.Fire(main)
