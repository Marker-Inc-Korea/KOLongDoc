# KOLongDoc📜
<div align='center'>
<strong>VLM Benchmark for (Very) Long Korean Document😵😵</strong> 
<br></br>
</div>

![img](teaser.png)

# News
**Dataset Huggingface😊:** [Markr-AI/KOLongDoc](https://huggingface.co/datasets/Markr-AI/KOLongDoc)  
**KOLongDoc Blog😎**: [Blog Posting]()

# Introduction
오늘날 멀티모달과 RAG에 대한 관심이 높아지면서, 공공업무나 행정업무에 ChatGPT, Claude와 같은 AI가 많이 도입되기 시작했습니다.😎  
이러한 흐름에 따라, 해외에는 긴 문서나 복잡한 문서에 대한 여러 벤치마크가 등장하고 있지만 여전히 국내에서는 이러한 데이터셋 및 벤치마크가 부족한 상황입니다.🥲  

기존 한국어 VLM의 성능을 측정하기 위한 벤치마크들은 여러가지 목적으로 공개가 되었습니다.🧐🧐
- [KO-VQA](https://github.com/Marker-Inc-Korea/KO-VLM-Benchmark/tree/main/KO-VQA): 한국어 **문서**기반 이해 능력 평가
- [KO-VDC](https://github.com/Marker-Inc-Korea/KO-VLM-Benchmark/blob/main/KO-VDC/README.md): 한국어 **문서** 기반 표/도식/그래프에 대한 적절한 설명문 생성 능력 평가
- [KO-OCRAG](https://github.com/Marker-Inc-Korea/KO-VLM-Benchmark/tree/main/KO-OCRAG): 고해상도 한국어 **문서** OCR 능력 및 문서에 존재하는 visual information에 대한 text description 생성 능력 평가
- [KOFFVQA](https://arxiv.org/html/2503.23730v1): 한국어 **이미지** 기반 객관적이고 신뢰성 있게 평가하기 위한 free-form  VQA 평가
- [KoViDoRe](https://github.com/whybe-choi/KoVidore-benchmark): 한국어 시각 **문서** retrieval 능력 평가
- [K-MMBench](https://huggingface.co/datasets/NCSOFT/K-MMBench) and [K-MMStar](https://huggingface.co/datasets/NCSOFT/K-MMStar): 한국어 기반 **이미지**에 대한 다양한 시각 이해 및 추론 능력 평가
- [K-DTCBench](https://huggingface.co/datasets/NCSOFT/K-DTCBench): 한국어 **이미지** 기반 표·차트 이해 능력을 다양한 형식(디지털 및 손글씨)에서 이해 능력 평가
- [K-LLAVA-W](https://huggingface.co/datasets/NCSOFT/K-LLaVA-W): 한국어 **이미지** 기반 실생활 기반 시각 이해 및 질의응답 능력을 평가

위와 같이 다양한 데이터 형식과 이미지/문서를 기반으로 한국어 능력을 평가하고자 하는 움직임은 있었지만, **길이가 긴 고해상도 한국어 문서에 대한 multi-hop VQA를 종합적으로 고려한 데이터셋**은 없었습니다.⚠️  
   
✨따라서 저희는 **KOLongDoc📄**라는 복잡하고 긴 고해상도 한국어 문서에 대한 VLM 벤치마크를 소개합니다.✨  
이를 위해, 저희는 한국어 공공기관 문서를 [공공데이터포털](https://www.data.go.kr/)에서 수집한 후, multi-hop question and answering 문제를 제작하였습니다.😎  
**KOLongDoc 벤치마크**는 총 200문항으로 구성되어 있으며, **복잡한 추론, multi-page understanding, 그리고 long-document understanding에 대한 한국어 능력을 평가**할 수 있습니다.⭐  

KOLongDoc가 한국어 벤치마크 및 한국어 멀티모달 모델 평가에 큰 도움이 될 것이라고 생각합니다!🤗  

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
Document name: 인천 해양수질측정망 운영 결과(2024년 3분기).pdf

Question: 붙임 3'의 퇴적물 조사 결과에서 구리 농도가 가장 높은 정점과 아연 농도가 가장 높은 정점의 이름을 각각 찾고, 두 정점 중 총유기탄소(TOC) 함량이 더 낮은 정점의 이름과 그 TOC(%) 값은 무엇인가?

Answer: 구리는 '강화주문도 선착장 앞', 아연은 '영종도 동방' 입니다. TOC 함량이 낮은 것은 '강화주문도 선착장 앞' 이며, 0.458이다.

Keyword: ['강화주문도 선착장', '영종도 동방', 0.458]
```

```
Document name: 인사혁신처_국가공무원인재개발원 교육운영계획_20260310.pdf

Question: '영어권 장기국외훈련자과정' 및 '디지털역량교육과정 (3일)'을 수강하고 싶은데, 교육비는 얼마나 들까요? (숫자는 전부 적어주세요. 예시로, 100000원.) 그리고 주변에 국내 A회사에 다니는 공무원 친구가 집에서 재택근무를 하고 시간이 많다는데, 2개의 강좌를 동시에 들을 수 있을까요? ('가능' 또는 '불가능'이라고 답해주세요.)

Answer: 850000, 불가능

Keyword: [850000, '불가능']
```

**KOLongDoc 데이터셋**을 통해, 한국어 LLM 및 해외 LLM 등등 다양한 평가를 통해 **long multi-page QA에 대한 성능을 평가**할 수 있을 것이라 기대합니다🔥🔥.  
자세한 평가방식은 다음 섹션을 참고해주세요.

# Evaluation🤖
모델 평가는 `Accuracy`를 기반으로 구성됩니다.🔥   
모델 답변 안에서 `Keyword`에 해당하는 단어들이 얼마나 들어가 있는지 비율을 토대로 평가를 진행하게 됩니다.

예시는 다음과 같습니다🤗:  
```
Question: 붙임 3'의 퇴적물 조사 결과에서 구리 농도가 가장 높은 정점과 아연 농도가 가장 높은 정점의 이름을 각각 찾고, 두 정점 중 총유기탄소(TOC) 함량이 더 낮은 정점의 이름과 그 TOC(%) 값은 무엇인가?

Gemini Answer: 제공된 문서의 '붙임 3. 해양수질측정망 해저퇴적물 조사 결과(2024년 3분기)'(15~16페이지)를 바탕으로 분석한 결과는 다음과 같습니다.

1. **구리(Cu) 농도가 가장 높은 정점:**
   - 정점 21 (강화주문도 선착장 앞): 223.94 mg/kg으로 가장 높습니다.

2. **아연(Zn) 농도가 가장 높은 정점:**
   - 정점 17 (만석부두 앞): 91.99 mg/kg으로 가장 높습니다.

3. **총유기탄소(TOC) 함량 비교:**
   - 정점 21(강화주문도 선착장 앞)의 TOC: 0.458 %
   - 정점 17(만석부두 앞)의 TOC: 0.928 %

두 정점 중 TOC 함량이 더 낮은 곳은 **정점 21(강화주문도 선착장 앞)**이며, 해당 값은 **0.458 %**입니다.

Keyword: ['강화주문도 선착장', '영종도 동방', 0.458]

Accuracy: 약 66.6%
```

```
Question: '영어권 장기국외훈련자과정' 및 '디지털역량교육과정 (3일)'을 수강하고 싶은데, 교육비는 얼마나 들까요? (숫자는 전부 적어주세요. 예시로, 100000원.) 그리고 주변에 국내 A회사에 다니는 공무원 친구가 집에서 재택근무를 하고 시간이 많다는데, 2개의 강좌를 동시에 들을 수 있을까요? ('가능' 또는 '불가능'이라고 답해주세요.)

Gemini Answer: 질문에 대한 답변은 다음과 같습니다.

**1. 교육비**
*   **제공된 문서에서는 해당 내용을 찾을 수 없습니다.**
*   문서에 따르면 '영어권 장기국외훈련자과정'의 교육비는 14일 기준 **700000원**으로 명시되어 있으나, 3일만 수강할 경우의 비용 산정 기준은 나와있지 않습니다. 또한, '디지털역량교육과정'은 수십 개의 세부 과정(과정별 **100000원** 또는 **150000원**)으로 나뉘어 있어 어떤 과정을 수강하는지 특정할 수 없기 때문에 정확한 교육비 합산이 불가능합니다.

**2. 동시 수강 가능 여부**
*   **불가능**
*   해당 친구가 공무원 신분이라고 가정하더라도 두 과정을 동시에 수강하는 것은 불가능합니다.
    1.  '영어권 장기국외훈련자과정'의 교육대상은 일반 공무원이 아닌 **'영어권 장기국외훈련 파견 공무원'**으로 엄격히 제한되어 있습니다.
    2.  두 과정 모두 지정된 연수원 등에서 오프라인으로 참석해야 하는 **'집합'** 교육 방식으로 진행되므로, 집에서 재택근무를 하며 동시에 수강할 수 없습니다.

Keyword: [850000, '불가능']

Accuracy: 50%
```
  
위와 같은 평가 시스템을 기반으로 총 2가지 버전의 성능평가 테이블을 공유합니다:
- `Hard` Version: 0 or 1로 평가하는 방법. (100% 정확도만을 정답으로 인정)
- `Soft` Version: 0~1 사이로 평가하는 방법.

그리고 document input type에 따른 모델 능력을 비교하기 위해서 다음과 같이 평가를 진행됩니다:
- text: `pymuPDF` 모듈을 활용하여, 텍스트를 전부 추출한 후 모델에 전달
- image: PDF를 이미지 형식으로 모델에 전달

모든 평가는 `max_token: 4096 or 8192`와 한 개의 A100 80GB GPU를 활용해서 수행했습니다!  
자세한 평가는 코드를 참고해주세요!

# Results (Hard Ver.)🔥🤖🔥
## Input type: Image🖼️
| models (input_type) | L-Acc | SL-Acc | Avg. Acc |
| ------ | --- | --- | --- |
| gemini-3.5-flash (image) | **82.35** | **82.81** | **82.58** |
| gemini-3.1-pro (image) | 71.32 | 69.94 | 70.48 |
| gemini-3.1-flash (image) | 63.97 | 67.19 | 65.58 |
| gemini-2.5-pro (image) | 66.91 | 59.38 | 63.15 |
| `Open-Source` |
| Qwen3.6-27B (image) | 8.82 | `OOM` | `OOM` |
| Qwen3.5-9B (image) | 7.35 | 1.56 | 4.46 |
| gemma-4-31B-it (image) | - | - | - |
| gemma-4-E4B-it (image) | 19.11 | `OOM` | `OOM` |
| EXAONE-4.5-33B (image) | - | - | - |
| VARCO-VISION-2.0-14B-HF (image) | 0.74 | `timeout` | `timeout` |
| kanana-1.5-v-3b-instruct (image) | - | - | - |
| Bllossom-AICA-5B (image) | `timeout` | `timeout` | `timeout` |
> L-Acc: Long Document (`< 60 pages`)  
> SL-Acc: Super Long Document (`> 60 pages`)  
> timeout: It's too slow to test.

## Input type: Text📜
| models (input_type) | L-Acc | SL-Acc | Avg. Acc |
| ------ | --- | --- | --- |
| gemini-3.5-flash (text) | **69.85** | **67.19** | **68.52** |
| gemini-3.1-pro (text) | 58.82 | 64.06 | 61.44 |
| gemini-3.1-flash (text) | 55.15 | 53.13 | 54.14 |
| gemini-2.5-pro (text) | 64.71 | 60.94 | 62.83 |
| `Open-Source` |
| Qwen3.6-27B (text) | 65.44 | - | - |
| Qwen3.5-9B (text) | 60.29 | 48.44 | 54.37 |
| gemma-4-31B-it (text) | - | - | - |
| gemma-4-E4B-it (text) | 44.62 | `OOM` | `OOM` |
| EXAONE-4.5-33B (text) | - | - | - |
| VARCO-VISION-2.0-14B-HF (text) | 13.24 | `OOM` | `OOM` |
| kanana-1.5-v-3b-instruct (text) | - | - | - |
| Bllossom-AICA-5B (text) | 9.56 | - | - |
> L-Acc: Long Document (`< 60 pages`)  
> SL-Acc: Super Long Document (`> 60 pages`)  

# Results (Soft Ver.)🤖
## Input type: Image🖼️
| models (input_type) | L-Acc | SL-Acc | Avg. Acc |
| ------ | --- | --- | --- |
| gemini-3.5-flash (image) | **91.95** | **90.34** | **91.15** |
| gemini-3.1-pro  (image) | 85.34 | 81.51 | 83.43 |
| gemini-3.1-flash (image) | 79.63 | 80.86 | 80.23 |
| gemini-2.5-pro (image) | 82.39 | 78.91 | 80.65 |
| `Open-Source` |
| Qwen3.6-27B (image) | 19.98 | `OOM` | `OOM` |
| Qwen3.5-9B (image) | 18.44 | 14.86 | 16.65 |
| gemma-4-31B-it (image) | - | - | - |
| gemma-4-E4B-it (image) | 35.81 | `OOM` | `OOM` |
| EXAONE-4.5-33B (image) | - | - | - |
| VARCO-VISION-2.0-14B-HF (image) | 4.79 | `timeout` | `timeout` |
| kanana-1.5-v-3b-instruct (image) | - | - | - |
| Bllossom-AICA-5B (image) | `timeout` | `timeout` | `timeout` |
> L-Acc: Long Document (`< 60 pages`)  
> SL-Acc: Super Long Document (`> 60 pages`)  
> timeout: It's too slow to test.

## Input type: Text📜
| models (input_type) | L-Acc | SL-Acc | Avg. Acc |
| ------ | --- | --- | --- |
| gemini-3.5-flash (text) | **79.40** | 74.11 | **76.76** |
| gemini-3.1-pro (text) | 75.29 | 74.77 | 75.03 |
| gemini-3.1-flash (text) | 72.46 | 70.69 | 71.58 |
| gemini-2.5-pro (text) | 77.32 | **75.88** | 76.60 |
| `Open-Source` |
| Qwen3.6-27B (text) | 79.08 | - | - |
| Qwen3.5-9B (text) | 73.13 | 68.55 | 70.84 |
| gemma-4-31B-it (text) | - | - | - |
| gemma-4-E4B-it (text) | 62.88 | `OOM` | `OOM` |
| EXAONE-4.5-33B (text) | - | - | - |
| VARCO-VISION-2.0-14B-HF (text) | 18.96 | `OOM` | `OOM` |
| kanana-1.5-v-3b-instruct (text) | - | - | - |
| Bllossom-AICA-5B (text) | 18.01 | - | - |
> L-Acc: Long Document (`< 60 pages`)  
> SL-Acc: Super Long Document (`> 60 pages`)  

# To-Do list
- [x] Release dataset
- [ ] Release eval code

# References🌟
[LongDocURL](https://arxiv.org/abs/2412.18424)  
[공공데이터포털](https://www.data.go.kr/)
