# cache dir 설정
#export HF_HOME="/data1"
export CUDA_VISIBLE_DEVICES=0
export CUDA_LAUNCH_BLOCKING=1

# Qwen/Qwen3.6-27B
# Qwen/Qwen3.5-9B
# google/gemma-4-31B-it
# google/gemma-4-E4B-it
# google/gemma-4-E2B-it
# Markr-AI/Gukbap-Ovis2-16B-VL
# LGAI-EXAONE/EXAONE-4.5-33B
# NCSOFT/VARCO-VISION-2.0-14B
# Bllossom/llama-3.2-Korean-Bllossom-AICA-5B
python eval.py \
    --base_model [..base_model...] \
    --huggingface_token [...your_token...] \
    --dataset_path ./dataset \
    --image_path ./dataset/dataset \
    --cutoff_len 8192