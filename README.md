# KOLongDoc📜
<div align='center'>
<strong>VLM Benchmark for (Very) Long Korean Document😵😵</strong> 
<br></br>
</div>

![img](teaser.png)

# News
**() Dataset Huggingface😊:** [markrAI/KLongDoc]()  
**() KOLongDoc Blog😎**: [Blog Posting]()

# Introduction
오늘날 멀티모달과 RAG에 대한 관심이 높아지면서, 공공업무나 행정업무에 ChatGPT, Claude와 같은 AI가 많이 도입되기 시작했습니다😎  
이러한 흐름에 따라, 해외에는 긴 문서나 복잡한 문서에 대한 여러 벤치마크가 등장하고 있지만 여전히 국내에서는 이러한 데이터셋 및 벤치마크가 부족한 상황입니다.🥲  
  
✨따라서 저희는 **KOLongDoc📄**라는 복잡하고 긴 한국어 문서에 대한 VLM 벤치마크를 소개합니다✨!  
이를 위해, 저희는 한국어 공공기관 문서를 [공공데이터포털](https://www.data.go.kr/)에서 수집한 후, multi-hop question and answering 문제를 제작하였습니다😎.   
**KOLongDoc 벤치마크**는 총 200문항으로 구성되어 있으며, **복잡한 추론, multi-page understanding, 그리고 long-document understanding에 대한 한국어 능력을 평가**할 수 있습니다⭐!

KOLongDoc가 한국어 벤치마크 및 한국어 멀티모달 모델 평가에 큰 도움이 될 것이라 생각합니다!🤗  

# Details of Dataset📜


# Evaluation🤖


# Results (Soft)🤖
| models (input_type) | L-Acc | SL-Acc | Avg. Acc |
| ------ | --- | --- | --- |
| gemini-3.1-pro (text) | 75.29 | 74.77 | 75.03 |
| gemini-3.1-pro  (image) | **85.34** | **81.51** | **83.43** |
| gemini-3.1-flash (text) | 72.46 | 70.69 | 71.58 |
| gemini-3.1-flash (image) | 79.63 | 80.86 | 80.23 |
| gemini-2.5-pro (text) | 77.32 | 75.88 | 76.60 |
| gemini-2.5-pro (image) | 82.39 | 78.91 | 80.65 |
| `Open-Source` |
| Qwen/Qwen3.6-35B-A3B | - | - | - |
| Qwen/Qwen3.6-27B | - | - | - |
| Qwen/Qwen3.5-35B-A3B | - | - | - |
| Qwen/Qwen3.5-27B | - | - | - |
| Qwen/Qwen3.5-9B | - | - | - |
| Qwen3-VL-8B-Instruct | - | - | - |
| google/gemma-4-31B-it | - | - | - |
| google/gemma-4-E4B-it | - | - | - |
| VARCO-VISION-2.0-14B-HF | - | - | - |
| Gukbap-Ovis2-16B | - | - | - |
| Bllossom-AICA-5B | - | - | - |
> L-Acc: Long Document (`< 60 pages`)  
> SL-Acc: Super Long Document (`> 60 pages`)  

# TO-Do list
- [ ] Release dataset
- [ ] Release code

# References🌟
[LongDocURL](https://arxiv.org/abs/2412.18424)  
[공공데이터포털](https://www.data.go.kr/)
