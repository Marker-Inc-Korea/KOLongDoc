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
오늘날 멀티모달과 RAG에 대한 관심이 높아지면서, 공공업무나 행정업무에 ChatGPT, Claude와 같은 AI가 많이 도입되기 시작했습니다.😎  
이러한 흐름에 따라, 해외에는 긴 문서나 복잡한 문서에 대한 여러 벤치마크가 등장하고 있지만 여전히 국내에서는 이러한 데이터셋 및 벤치마크가 부족한 상황입니다.🥲  
  
✨따라서 저희는 **KOLongDoc📄**라는 복잡하고 긴 한국어 문서에 대한 VLM 벤치마크를 소개합니다.✨  
이를 위해, 저희는 한국어 공공기관 문서를 [공공데이터포털](https://www.data.go.kr/)에서 수집한 후, multi-hop question and answering 문제를 제작하였습니다.😎  
**KOLongDoc 벤치마크**는 총 200문항으로 구성되어 있으며, **복잡한 추론, multi-page understanding, 그리고 long-document understanding에 대한 한국어 능력을 평가**할 수 있습니다.⭐  

KOLongDoc가 한국어 벤치마크 및 한국어 멀티모달 모델 평가에 큰 도움이 될 것이라 생각합니다!🤗  

# Details of Dataset📜
KOLongDoc는 총 100개의 문서를 **🌟매우 다양한 도메인🌟**에서 수집하였습니다.  
각 문서들은 총 2가지 type의 문서들로 구분이 되고, 각 문서마다 2개의 multi-hop QA 문항을 구성하였습니다.
- Long document: 60 페이지 미만의 문서들 구성되며, 136문항으로 구성됨. (68개의 문서)
- Super Long document: 60 페이지 이상의 문서들로 구성되며, 64문항으로 구성됨. (32개의 문서)
  
각 문서들에서 multi-hop QA 문항을 제작한 방법은 다음과 같습니다:  
- [gemini-prompt](https://github.com/Marker-Inc-Korea/KOLongDoc/blob/main/gemini-prompt.txt)를 통해 각 문서마다 question과 answer를 자동으로 생성합니다.🤖
- Human verification을 통해, 각 문항의 난이도와 multi-QA 여부를 확인하고, 질문의 퀄리티 향상 및 올바른 답변으로 수정하는 과정을 수행합니다.🧐
- 마지막으로, **정확한 정량적 평가**를 위해서 정답으로 인정되기 위해서 필수적으로 담겨야하는 `keyword`를 인간이 직접 선별하는 과정을 수행합니다.🧐
  
완성된 데이터셋의 예시는 아래와 같습니다:
```
Document name: 

Question:

Answer: 

Keyword: 
```

```
Document name: 인사혁신처_국가공무원인재개발원 교육운영계획_20260310.pdf

Question: '영어권 장기국외훈련자과정' 및 '디지털역량교육과정'을 3일간 듣고 싶은데, 교육비는 얼마나 들까요? (숫자는 전부 적어주세요. 예시로, 100000원.) 그리고 주변에 국내 A회사에 다니는 공무원 친구가 집에서 재택근무를 하고 시간이 많다는데, 2개의 강좌를 동시에 들을 수 있을까요? ('가능' 또는 '불가능'이라고 답해주세요.)

Answer: 850000, 불가능

Keyword: [850000, '불가능']
```

**KOLongDoc 데이터셋**을 통해, 한국어 LLM 및 해외 LLM 등등 다양한 평가를 통해 **long multi-page QA에 대한 성능을 평가**할 수 있을 것이라 기대합니다🔥🔥.  
자세한 평가방식은 다음 섹션을 참고해주세요.

# Evaluation🤖


# Results (Hard Ver.)🤖
| models (input_type) | L-Acc | SL-Acc | Avg. Acc |
| ------ | --- | --- | --- |
| gemini-3.1-pro (text) | 58.82 | 64.06 | - |
| gemini-3.1-pro  (image) | **71.32** | - | - |
| gemini-3.1-flash (text) | 55.15 | 53.13 | - |
| gemini-3.1-flash (image) | 63.97 | 67.19 | - |
| gemini-2.5-pro (text) | 64.71 | 60.94 | - |
| gemini-2.5-pro (image) | 66.91 | 59.38 | - |
| `Open-Source` |
| Qwen/Qwen3.6-35B-A3B | - | - | - |
| Qwen/Qwen3.5-9B | - | - | - |
| google/gemma-4-31B-it | - | - | - |
| google/gemma-4-E4B-it | - | - | - |
| VARCO-VISION-2.0-14B-HF | - | - | - |
| Gukbap-Ovis2-16B | - | - | - |
| Bllossom-AICA-5B | - | - | - |
> L-Acc: Long Document (`< 60 pages`)  
> SL-Acc: Super Long Document (`> 60 pages`)  

# Results (Soft Ver.)🤖
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
| Qwen/Qwen3.5-9B | - | - | - |
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
