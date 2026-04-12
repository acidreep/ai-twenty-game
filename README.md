
# 🤖 AI Twenty Questions Battle Arena (스무고개 배틀)

이 프로젝트는 다양한 **LLM(Large Language Models)** 간의 논리적 추론 능력과 지시 이행 능력을 비교하기 위한 **스무고개 배틀 프레임워크**입니다. 

로컬 모델과 클라우드 모델을 매칭하여 어떤 모델이 가장 적은 질문으로 정답을 맞히는지, 그리고 그 과정에서의 비용 효율성을 측정합니다.

---

## 🚀 주요 특징

* **멀티 프로바이더 지원**: Ollama(로컬) 및 OpenRouter(클라우드) API를 통한 다양한 모델 지원.
* **자동화된 배틀**: 호스트(문제 출제자)와 플레이어 역할을 할당하여 게임 진행.
* **비용 계산**: 최신 환율 및 OpenRouter 가격표를 반영하여 KRW/USD 비용 자동 산출.
* **파싱 로직**: 정규표현식 기반 데이터 추출로 모델의 불필요한 서술 필터링 및 JSON 안정성 확보.
* **리포트 생성**: 질문 내역, 소요 시간, 토큰 사용량, 비용이 포함된 Markdown 리포트 자동 생성.

---

## 🛠 설치 및 설정

1. **저장소 복제**
   ```bash
   git clone https://github.com/your-username/ai-twenty-game.git
   cd ai-twenty-game
   ```

2. **의존성 설치**
   ```bash
   pip install ollama openai python-dotenv requests
   ```

3. **환경 변수 설정**
   `.env` 파일을 생성하고 OpenRouter API 키를 입력합니다.
   ```env
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

4. **가격 정보 업데이트**
   ```bash
   python update_pricing.py
   ```

---

## 📂 파일별 기능 설명

| 파일명 | 역할 및 설명 |
| :--- | :--- |
| `ai_twenty_game.py` | **핵심 엔진**. 게임 로직, LLM 통신 인터페이스, 공통 단어 풀 관리. |
| `run_openrouter.py` | **클라우드 배틀**. OpenRouter 모델들 간의 스무고개 배틀 수행. |
| `run_local.py` | **로컬 배틀**. Ollama 모델들 간의 스무고개 배틀 수행. |
| `update_pricing.py` | **유지보수**. 실시간 환율 및 OpenRouter 단가를 `pricing_config.json`에 반영. |

---

## 🤖 참여자

### 1. 호스트 (문제 출제자)
* `google/gemini-3-flash-preview`

### 2. 플레이어
* **Cloud Models - Frontier Tier**
    * `openai/gpt-5.4`
    * `anthropic/claude-sonnet-4.6`
    * `x-ai/grok-4.20`
* **Cloud Models - Value Tier**
    * `deepseek/deepseek-v3.2`
    * `google/gemini-3-flash-preview`
    * `google/gemini-2.5-flash-lite`
    * `x-ai/grok-4.1-fast`
    * `xiaomi/mimo-v2-flash`
* **Local Models**
    * `phi4:14b`
    * `gemma4:e4b`
    * `llama3.1:8b`
    * `qwen2.5:7b`
    * `mistral:7b`
    * `exaone3.5:7.8b`
---

## 📋 LLM 플레이어 성능 평가 가이드라인

플레이어 AI의 논리적 추론, 정보 효율성, 지시 이행 능력을 정밀하게 판별하기 위한 기준입니다.

### 1. 정량적 지표 평가 (Quantitative)
* **추론 속도 (Efficiency)**: 10회 이하(탁월), 15회 이하(보통), 20회 초과(미흡).
* **시간당 생산성**: 질문 생성 평균 소요 시간(1초 미만 권장).
* **토큰 경제성**: 정답 범위가 좁아질수록 질문이 간결해지는지 측정.
* **비용 효율성**: 동일 정답 대비 클라우드 API 소모 비용 비교.

### 2. 정성적 논리 평가 (Qualitative)
* **계층적 탐색 전략**: 초반 5턴 이내 거대 카테고리(생물/무생물 등) 확정 여부.
* **정보 통합 및 기억력**: 호스트의 "아니오" 답변을 바탕으로 이후 질문에서 해당 범주 배제 여부.
* **시스템 적응력**: 지정된 JSON 형식 준수 및 불필요한 서술 배제 여부.

### 3. 종합 성능 등급
> **S (Expert)**: 8회 이하 성공. 이진 탐색 논리 완벽 구사.  
> **A (Advanced)**: 12회 내외 성공. 안정적이나 직관력이 다소 부족.  
> **B (Competent)**: 15~20회 성공. 단순 개별 단어 대입(선형 탐색) 경향.  
> **C/F (Suboptimal)**: 실패 혹은 이미 확인된 정보 반복 질문.

---

## 💡 주의사항
* **동일 조건 비교**: 모든 플레이어는 동일한 호스트 모델과 정답 단어로 평가되어야 합니다.
* **균형 잡힌 시각**: 질문 횟수뿐만 아니라 로컬 모델의 자원 점유, 클라우드의 비용 효율성을 함께 고려하세요.
* **데이터 중심**: 브랜드 인지도에 편향되지 않고 오직 로그의 논리적 연결성만을 기준으로 판별합니다.

---

## 🏆 전체 14개 모델 통합 성능 평가 성적표 (테스트 결과)

실제로 진행한 아래의 두 건의 배틀 리포트 로그를 기반으로, **LLM 플레이어 성능 평가 가이드라인**에 따라 모든 모델의 지표를 정량화한 결과입니다.

| 순위 | 모델명 | 구분 | 결과 | 질문 횟수 | 추론 등급 | 비고 |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | **google/gemini-3-flash-preview** | Cloud | ✅ | 8 | **S** | 최단 경로 추론 및 가설 검증 능력 탁월 |
| **2** | **anthropic/claude-sonnet-4.6** | Cloud | ✅ | 8 | **S** | 체계적인 계층적 탐색(생물→곤충) 수행 |
| **3** | **x-ai/grok-4.20** | Cloud | ✅ | 8 | **A+** | 매우 빠른 응답 속도와 효율적인 질문 구성 |
| **4** | **xiaomi/mimo-v2-flash** | Cloud | ✅ | 8 | **A+** | 최고 수준의 비용 대비 성능 효율성 기록 |
| **5** | **google/gemini-2.5-flash-lite** | Cloud | ✅ | 9 | **A** | 안정적인 논리 전개 및 낮은 토큰 소모 |
| **6** | **gemma4:e4b** | Local | ✅ | 10 | **A** | 로컬 모델 중 유일하게 클라우드급 추론력 보유 |
| **7** | **llama3.1:8b** | Local | ✅ | 10 | **A-** | 정석적인 이진 탐색 기법 구사 |
| **8** | **x-ai/grok-4.1-fast** | Cloud | ✅ | 10 | **A-** | 질문 생성 시간의 편차가 크나 정답 도달 성공 |
| **9** | **deepseek/deepseek-v3.2** | Cloud | ✅ | 12 | **B+** | 논리는 명확하나 초기 탐색 범위 설정이 다소 넓음 |
| **10** | **openai/gpt-5.4** | Cloud | ✅ | 15 | **B** | 불필요한 속성(빵 상자 크기 등) 질문으로 지연 발생 |
| **11** | **phi4:14b** | Local | ❌ | 20 | **C** | 중반 이후 질문 루프에 빠지며 범위 축소 실패 |
| **12** | **mistral:7b** | Local | ❌ | 20 | **D+** | 생물학적 특징에만 매몰되어 정답 유추 실패 |
| **13** | **qwen2.5:7b** | Local | ❌ | 20 | **D** | 개념 추론보다 언어적(글자 수 등) 단서에 집착 |
| **14** | **exaone3.5:7.8b** | Local | ❌ | 20 | **F** | 연관성 없는 단어들을 무작위로 나열하는 패턴 |

2. 세부 지표 분석 리포트
- 🅰️ 전략적 추론 (Strategic Thinking)
   - 상위 모델(S-Tier): Gemini 3, Claude 4.6 등은 첫 3턴 이내에 동물/곤충/날개 유무를 확정 지었습니다. 특히 Gemini 3는 7번 질문에서 "나비와 같은 무늬가 있나요?"라는 가설 검증형 질문을 던져 정답률을 극대화했습니다.

   - 하위 모델(C-F Tier): Exaone과 Qwen은 **개념적 계층(Taxonomy)**을 활용하지 못했습니다. 특히 Exaone은 자연물임을 인지했음에도 불구하고 '철자 질문'과 '고유 명사 무작위 대입'을 반복하며 논리적 파생에 실패했습니다.

- 🅱️ 기술적 효율성 및 비용 (Efficiency & Cost)
   - 비용 대비 성능: Mimo-v2-flash와 Gemini 2.5 Lite는 상위 모델 대비 약 1/10~1/20 수준의 비용으로 유사한 성능을 냈습니다. 반면 GPT-5.4는 질문 횟수도 많고 토큰당 단가도 높아 가장 낮은 경제성을 보였습니다.

   - 로컬 모델의 한계: 로컬 모델(Mistral, Phi4 등)은 질문 횟수가 많아질수록 호스트 토큰 누적량이 급증하여, 물리적 자원 점유율이 비효율적으로 상승하는 경향이 확인되었습니다.

- 🆂 특이 사항 (Edge Cases)
   - 모호한 답변 대응: Gemma 4는 호스트가 "모름(I don't know)"이라고 답변했음에도 불구하고, 당황하지 않고 바로 다음 논리 단계(정답 제출)로 이행하는 높은 위기 관리 능력을 보였습니다.

- 💡 추가 의견 및 제언
   - 로컬 모델의 프롬프트 튜닝 필요: Phi 4나 Mistral의 경우 논리 자체는 나쁘지 않으나, 정답을 확신하는 단계에서 "정답을 맞춰도 되는지" 주저하는 경향이 보입니다. 정답 후보가 3개 이하로 좁혀지면 과감히 제출하도록 하는 결정 로직(Decision Threshold) 강화가 필요해 보입니다.

   - 질문 가치 재산정: Deepseek처럼 "명사인가요?"와 같은 질문은 모든 단어에 해당하므로 변별력이 낮습니다. 향후 평가 시 **'정보 획득 가치가 낮은 질문'**에 대한 감점 항목을 가이드라인에 추가하면 더욱 정교한 판별이 가능할 것 같습니다.

---

# 🏆 클라우드 모델 스무고개 배틀 리포트 (20260411_220106)

**호스트 모델:** {'provider': 'openrouter', 'name': 'google/gemini-3-flash-preview'}

**전체 소요 시간:** 0:03:55 (235.27초)
- **호스트 준비 시간:** 10.96초 (단어 선정 및 초기화)
- **순수 게임 진행 시간:** 224.29초 (질문/답변 합계)

| 순위 | 모델명 | 정답 단어 | 결과 | 질문 횟수 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | google/gemini-3-flash-preview | Butterfly | ✅ 성공 | 8 |
| 2 | anthropic/claude-sonnet-4.6 | Butterfly | ✅ 성공 | 8 |
| 3 | x-ai/grok-4.20 | Butterfly | ✅ 성공 | 8 |
| 4 | xiaomi/mimo-v2-flash | Butterfly | ✅ 성공 | 8 |
| 5 | google/gemini-2.5-flash-lite | Butterfly | ✅ 성공 | 9 |
| 6 | x-ai/grok-4.1-fast | Butterfly | ✅ 성공 | 10 |
| 7 | deepseek/deepseek-v3.2 | Butterfly | ✅ 성공 | 12 |
| 8 | openai/gpt-5.4 | Butterfly | ✅ 성공 | 15 |

---

## 📝 상세 게임 기록

### 모델: google/gemini-3-flash-preview (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is it a living thing? | Yes | 1.61 | 1.22 | 144/17 | 128/11 |
| 2 | Is it an animal? | Yes | 1.36 | 1.41 | 193/16 | 142/11 |
| 3 | Is it a mammal? | No | 1.44 | 1.25 | 246/16 | 156/11 |
| 4 | Does it have wings? | Yes | 1.32 | 1.34 | 304/16 | 170/11 |
| 5 | Is it a bird? | No | 1.35 | 1.42 | 367/16 | 184/11 |
| 6 | Is it an insect? | Yes | 1.46 | 1.34 | 435/16 | 198/11 |
| 7 | Does it have a colorful or patterned appearance, like a butterfly? | Yes | 1.53 | 1.28 | 508/24 | 220/11 |
| 8 | Is it a butterfly? | Correct! | 1.42 | 1.31 | 602/16 | 234/11 |

### 모델: anthropic/claude-sonnet-4.6 (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is the secret word a living thing (animal, plant, person)? | Yes | 2.17 | 1.34 | 161/29 | 136/11 |
| 2 | Is the secret word a person? | No | 1.71 | 1.38 | 237/22 | 152/11 |
| 3 | Is the secret word an animal? | Yes | 1.53 | 1.41 | 314/22 | 168/11 |
| 4 | Is the secret word a mammal? | No | 1.66 | 1.31 | 398/23 | 184/11 |
| 5 | Is the secret word a bird? | No | 2.00 | 1.40 | 491/22 | 200/11 |
| 6 | Is the secret word an insect? | Yes | 0.78 | 1.36 | 590/23 | 216/11 |
| 7 | Does the secret word fly? | Yes | 1.64 | 1.35 | 698/21 | 231/11 |
| 8 | Is the secret word a butterfly? | Correct! | 1.95 | 1.49 | 810/22 | 247/11 |

### 모델: x-ai/grok-4.20 (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is it a living thing? | Yes | 0.60 | 1.37 | 276/16 | 128/11 |
| 2 | Is it an animal? | Yes | 0.61 | 1.47 | 331/15 | 142/11 |
| 3 | Is it a mammal? | No | 0.56 | 1.24 | 390/15 | 156/11 |
| 4 | Is it a bird? | No | 0.54 | 1.30 | 454/15 | 170/11 |
| 5 | Is it a fish? | No | 0.54 | 1.27 | 523/15 | 184/11 |
| 6 | Is it an insect? | Yes | 0.54 | 1.51 | 597/15 | 198/11 |
| 7 | Is it a bee? | No | 0.57 | 1.28 | 676/15 | 212/11 |
| 8 | Is it a butterfly? | Correct! | 0.75 | 1.41 | 760/15 | 226/11 |

### 모델: xiaomi/mimo-v2-flash (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is the secret word a living thing? | Yes | 0.71 | 1.31 | 153/19 | 130/11 |
| 2 | Is the secret word an animal? | Yes | 0.72 | 1.33 | 218/18 | 146/11 |
| 3 | Is the secret word a mammal? | No | 1.10 | 1.68 | 289/19 | 162/11 |
| 4 | Is the secret word a bird? | No | 0.55 | 2.17 | 369/18 | 178/11 |
| 5 | Is the secret word a fish? | No | 0.56 | 1.46 | 455/18 | 194/11 |
| 6 | Is the secret word an insect? | Yes | 1.24 | 1.50 | 548/18 | 210/11 |
| 7 | Is the secret word a beetle? | No | 0.80 | 1.40 | 648/18 | 226/11 |
| 8 | Is the secret word a butterfly? | Correct! | 0.86 | 1.33 | 755/18 | 242/11 |

### 모델: google/gemini-2.5-flash-lite (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is it an animal? | Yes | 0.64 | 1.46 | 144/16 | 127/11 |
| 2 | Is it a mammal? | No | 0.55 | 1.35 | 191/16 | 141/11 |
| 3 | Is it a bird? | No | 0.47 | 1.33 | 243/16 | 155/11 |
| 4 | Is it a fish? | No | 0.49 | 1.34 | 300/16 | 169/11 |
| 5 | Is it a reptile? | No | 0.65 | 1.40 | 362/16 | 183/11 |
| 6 | Is it an insect? | Yes | 0.50 | 1.27 | 429/16 | 197/11 |
| 7 | Does it have six legs? | Yes | 0.52 | 1.40 | 501/17 | 212/11 |
| 8 | Does it fly? | Yes | 0.54 | 1.35 | 580/15 | 225/11 |
| 9 | Is it a butterfly? | Correct! | 0.62 | 1.35 | 661/16 | 239/11 |

### 모델: x-ai/grok-4.1-fast (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is the secret word a living thing? | Yes | 2.70 | 1.38 | 295/301 | 130/11 |
| 2 | Is it an animal? | Yes | 2.03 | 1.36 | 353/223 | 144/11 |
| 3 | Is it a mammal? | No | 1.81 | 1.66 | 413/200 | 158/11 |
| 4 | Is it a bird? | No | 3.69 | 1.41 | 478/340 | 172/11 |
| 5 | Is it a reptile? | No | 3.28 | 1.31 | 548/354 | 186/11 |
| 6 | Is it a vertebrate? | No | 4.21 | 1.45 | 623/423 | 200/11 |
| 7 | Is it an insect? | Yes | 1.63 | 1.36 | 703/172 | 214/11 |
| 8 | Does it have wings? | Yes | 5.40 | 1.66 | 788/530 | 228/11 |
| 9 | Does it have wings covered in scales? | Yes | 12.10 | 1.52 | 878/1183 | 245/11 |
| 10 | Is it a butterfly? | Correct! | 6.63 | 1.40 | 979/757 | 259/11 |

### 모델: deepseek/deepseek-v3.2 (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is the secret word a noun? | Yes | 0.58 | 1.36 | 140/19 | 129/11 |
| 2 | Is it a living thing? | Yes | 1.22 | 1.43 | 201/18 | 144/11 |
| 3 | Is it an animal? | Yes | 1.21 | 1.36 | 265/17 | 158/11 |
| 4 | Is it a mammal? | No | 1.61 | 1.30 | 333/17 | 172/11 |
| 5 | Is it a bird? | No | 1.02 | 1.33 | 443/16 | 186/11 |
| 6 | Is it a reptile? | No | 6.24 | 1.34 | 484/16 | 200/11 |
| 7 | Is it an amphibian? | No | 0.37 | 1.49 | 547/18 | 215/11 |
| 8 | Is it a fish? | No | 0.35 | 1.47 | 634/17 | 229/11 |
| 9 | Is it an insect? | Yes | 0.33 | 1.28 | 725/17 | 243/11 |
| 10 | Does it have wings? | Yes | 0.33 | 1.51 | 821/17 | 257/11 |
| 11 | Is it commonly considered a pest? | No | 0.52 | 1.42 | 922/19 | 273/11 |
| 12 | Is it a butterfly? | Correct! | 0.38 | 1.38 | 1032/17 | 287/11 |

### 모델: openai/gpt-5.4 (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is it a physical object? | Yes | 1.11 | 1.42 | 147/22 | 128/11 |
| 2 | Is it larger than a breadbox? | No | 1.11 | 1.28 | 209/24 | 145/11 |
| 3 | Is it something commonly found inside a home? | No | 1.20 | 1.26 | 281/25 | 163/11 |
| 4 | Is it a living thing? | Yes | 1.16 | 1.36 | 363/22 | 178/11 |
| 5 | Is it an animal? | Yes | 1.37 | 1.31 | 448/21 | 192/11 |
| 6 | Is it a wild animal rather than a domesticated one? | Yes | 1.29 | 1.58 | 537/28 | 212/11 |
| 7 | Does it typically live on land? | Yes | 1.11 | 1.42 | 645/23 | 228/11 |
| 8 | Is it a mammal? | No | 1.05 | 1.26 | 755/22 | 242/11 |
| 9 | Is it a reptile? | No | 1.10 | 1.27 | 870/22 | 256/11 |
| 10 | Is it a bird? | No | 1.09 | 1.41 | 991/21 | 270/11 |
| 11 | Is it an amphibian? | No | 1.02 | 1.32 | 1116/22 | 285/11 |
| 12 | Is it an insect? | Yes | 1.06 | 1.27 | 1248/21 | 299/11 |
| 13 | Can it fly? | Yes | 1.05 | 1.42 | 1384/20 | 312/11 |
| 14 | Is it known for stinging? | No | 1.23 | 1.34 | 1523/23 | 327/11 |
| 15 | Is it a butterfly? | Correct! | 1.19 | 1.33 | 1672/22 | 341/11 |

---

## 📊 전체 누적 비용 및 성능 요약 (Grand Total)
| 모델명 | 단가 (1M 토큰 In/Out) | 플레이어 토큰 | 호스트 토큰 | 질문 시간(s) | 답변 시간(s) | 합계 비용 (USD) | 합계 비용 (KRW) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| google/gemini-3-flash-preview | $0.50 / $3.00 | 2936 | 1520 | 11.50s | 10.57s | $0.002791 | ₩4.14 |
| anthropic/claude-sonnet-4.6 | $3.00 / $15.00 | 3883 | 1622 | 13.43s | 11.05s | $0.014888 | ₩22.08 |
| x-ai/grok-4.20 | $2.00 / $6.00 | 4128 | 1504 | 4.71s | 10.84s | $0.003491 | ₩5.18 |
| xiaomi/mimo-v2-flash | $0.09 / $0.29 | 3581 | 1576 | 6.54s | 12.17s | $0.001140 | ₩1.69 |
| google/gemini-2.5-flash-lite | $0.10 / $0.40 | 3555 | 1747 | 4.97s | 12.26s | $0.001520 | ₩2.25 |
| x-ai/grok-4.1-fast | $0.20 / $0.50 | 10541 | 2046 | 43.48s | 14.51s | $0.004062 | ₩6.02 |
| deepseek/deepseek-v3.2 | $0.26 / $0.38 | 6755 | 2625 | 14.18s | 16.69s | $0.002555 | ₩3.79 |
| openai/gpt-5.4 | $2.50 / $15.00 | 12527 | 3743 | 17.15s | 20.25s | $0.026882 | ₩39.86 |
| **합계 (Total)** | - | **47906** | **16383** | **115.95s** | **108.34s** | **$0.057329** | **₩85.01** |

---

# 🏆 로컬 모델 스무고개 배틀 결과 (20260411_220804)

**호스트 모델:** {'provider': 'openrouter', 'name': 'google/gemini-3-flash-preview'}

**전체 소요 시간:** 0:03:25 (205.36초)
- **호스트 준비 시간:** 8.30초 (단어 선정 및 초기화)
- **순수 게임 진행 시간:** 197.04초 (질문/답변 합계)

| 순위 | 모델명 | 정답 단어 | 결과 | 질문 횟수 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | gemma4:e4b | Butterfly | ✅ 성공 | 10 |
| 2 | llama3.1:8b | Butterfly | ✅ 성공 | 10 |
| 3 | phi4:14b | Butterfly | ❌ 실패 | 20 |
| 4 | qwen2.5:7b | Butterfly | ❌ 실패 | 20 |
| 5 | mistral:7b | Butterfly | ❌ 실패 | 20 |
| 6 | exaone3.5:7.8b | Butterfly | ❌ 실패 | 20 |

---

## 📝 상세 게임 기록

### 모델: gemma4:e4b (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is it an animal? | Yes | 5.74 | 1.38 | 168/17 | 127/11 |
| 2 | Is it bigger than a dog? | No | 0.65 | 1.31 | 229/19 | 143/11 |
| 3 | Can it fly? | Yes | 0.29 | 1.34 | 294/16 | 156/11 |
| 4 | Does it live in the wild? | Yes | 0.35 | 1.82 | 365/19 | 172/11 |
| 5 | Is it a bird? | No | 0.29 | 1.38 | 446/17 | 186/11 |
| 6 | Is it a mammal? | No | 0.30 | 1.40 | 530/17 | 200/11 |
| 7 | Is it a reptile? | No | 0.30 | 1.48 | 619/17 | 214/11 |
| 8 | Is it an insect? | Yes | 0.30 | 1.43 | 713/17 | 228/11 |
| 9 | Is it poisonous? | I don't know | 0.29 | 1.24 | 812/16 | 241/15 |
| 10 | Is it a butterfly? | Correct! | 0.30 | 1.42 | 918/17 | 259/11 |

### 모델: llama3.1:8b (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is the secret word a living thing? | Yes | 2.44 | 1.30 | 150/19 | 130/11 |
| 2 | Is the living thing a mammal? | No | 0.46 | 1.53 | 212/19 | 146/11 |
| 3 | Is the living thing an animal? | Yes | 0.44 | 1.33 | 282/18 | 162/11 |
| 4 | Does the living thing typically live on land? | Yes | 0.48 | 1.23 | 358/20 | 180/11 |
| 5 | Does the living thing have four legs? | No | 0.46 | 1.49 | 445/19 | 197/11 |
| 6 | Is the secret word a bird? | No | 0.44 | 1.48 | 539/18 | 213/11 |
| 7 | Is the secret word a reptile? | No | 0.47 | 1.54 | 639/19 | 229/11 |
| 8 | Is the secret word an insect? | Yes | 0.44 | 1.53 | 748/18 | 245/11 |
| 9 | Is the secret word a bee? | No | 0.45 | 1.28 | 863/18 | 261/11 |
| 10 | Is the secret word a butterfly? | Correct! | 0.46 | 1.60 | 985/18 | 277/11 |

### 모델: phi4:14b (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is it an object? | No | 2.45 | 1.67 | 151/16 | 127/11 |
| 2 | Is it a concept or idea? | No | 0.47 | 1.30 | 213/18 | 143/11 |
| 3 | Is it something that can be perceived by the senses? | Yes | 0.57 | 1.29 | 284/22 | 163/11 |
| 4 | Can you see it? | Yes | 0.43 | 1.31 | 370/16 | 177/11 |
| 5 | Is it man-made? | No | 0.45 | 1.68 | 455/16 | 192/11 |
| 6 | Is it found in nature? | Yes | 0.46 | 1.24 | 545/17 | 207/11 |
| 7 | Is it living? | Yes | 0.40 | 1.42 | 642/15 | 220/11 |
| 8 | Is it an animal? | Yes | 0.44 | 1.25 | 741/16 | 234/11 |
| 9 | Is it a mammal? | No | 0.45 | 1.37 | 846/17 | 248/11 |
| 10 | Does it have feathers? | No | 0.43 | 1.31 | 958/16 | 262/11 |
| 11 | Does it live primarily in water? | No | 0.48 | 1.35 | 1074/18 | 278/11 |
| 12 | Does it lay eggs? | Yes | 0.43 | 1.33 | 1199/16 | 292/11 |
| 13 | Is it a bird? | No | 0.43 | 1.39 | 1327/16 | 306/11 |
| 14 | Is it an insect? | Yes | 0.43 | 1.41 | 1460/16 | 320/11 |
| 15 | Does it have six legs? | Yes | 0.45 | 1.51 | 1598/17 | 335/11 |
| 16 | Does it fly? | Yes | 0.42 | 1.65 | 1743/15 | 348/11 |
| 17 | Is it commonly found indoors? | No | 0.47 | 1.39 | 1890/17 | 363/11 |
| 18 | Is it known for pollinating plants? | Yes | 0.51 | 1.42 | 2045/19 | 380/11 |
| 19 | Is it a bee? | No | 0.44 | 1.34 | 2210/16 | 394/11 |
| 20 | Is it larger than a typical housefly? | Yes | 0.53 | 1.56 | 2377/20 | 412/11 |

### 모델: qwen2.5:7b (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is the secret word an English word? | Yes | 1.72 | 1.46 | 149/19 | 130/11 |
| 2 | Does the secret word have more than 5 letters? | Yes | 0.53 | 1.42 | 211/22 | 150/11 |
| 3 | Is the secret word a noun? | Yes | 0.45 | 1.27 | 287/18 | 166/11 |
| 4 | Is the secret word related to technology? | No | 0.47 | 1.41 | 366/19 | 183/11 |
| 5 | Is the secret word related to food? | No | 0.48 | 1.54 | 454/19 | 200/11 |
| 6 | Is the secret word related to nature? | Yes | 0.47 | 1.51 | 550/19 | 217/11 |
| 7 | Is the secret word a name of a plant? | No | 0.52 | 1.34 | 654/21 | 236/11 |
| 8 | Is the secret word a type of weather? | No | 0.50 | 1.28 | 770/20 | 254/11 |
| 9 | Is the secret word a geographical feature? | No | 0.48 | 1.29 | 894/19 | 271/11 |
| 10 | Is the secret word an animal? | Yes | 0.46 | 1.47 | 1025/18 | 287/11 |
| 11 | Is the secret word a mammal? | No | 0.48 | 1.29 | 1162/19 | 303/11 |
| 12 | Is the secret word a bird? | No | 0.46 | 1.54 | 1308/18 | 319/11 |
| 13 | Is the secret word a reptile? | No | 0.49 | 1.78 | 1460/19 | 335/11 |
| 14 | Is the secret word a fish? | No | 0.47 | 1.39 | 1621/18 | 351/11 |
| 15 | Is the secret word an insect? | Yes | 0.47 | 1.37 | 1788/18 | 367/11 |
| 16 | Is the secret word a type of spider? | No | 0.51 | 1.39 | 1962/20 | 385/11 |
| 17 | Is the secret word a type of bee? | No | 0.52 | 1.47 | 2147/20 | 403/11 |
| 18 | Is the secret word a type of worm? | No | 0.53 | 1.49 | 2341/20 | 421/11 |
| 19 | Is the secret word a type of beetle? | No | 0.54 | 1.58 | 2544/20 | 439/11 |
| 20 | Is the secret word a type of ant? | No | 0.53 | 1.33 | 2756/20 | 457/11 |

### 모델: mistral:7b (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is the secret word a living thing? | Yes | 1.99 | 1.63 | 161/14 | 130/11 |
| 2 | Does it have a heart? | Yes | 0.16 | 1.59 | 217/12 | 145/11 |
| 3 | Does it have lungs? | No | 0.15 | 1.54 | 277/11 | 159/11 |
| 4 | Does it have blood? | Yes | 0.15 | 1.71 | 341/11 | 173/11 |
| 5 | Does it have a brain? | Yes | 0.16 | 1.53 | 410/12 | 188/11 |
| 6 | Does it have a nervous system? | Yes | 0.17 | 1.28 | 486/13 | 204/11 |
| 7 | Is it warm-blooded? | No | 0.18 | 1.35 | 570/13 | 219/11 |
| 8 | Does it have feathers? | No | 0.17 | 1.42 | 661/12 | 233/11 |
| 9 | Does it lay eggs? | Yes | 0.17 | 1.23 | 757/11 | 247/11 |
| 10 | Is it a reptile? | No | 0.18 | 1.45 | 857/13 | 261/11 |
| 11 | Does it live in water? | No | 0.18 | 1.42 | 966/12 | 276/11 |
| 12 | Is it a bird? | No | 0.17 | 1.36 | 1080/11 | 290/11 |
| 13 | Does it have wings? | Yes | 0.17 | 1.45 | 1198/11 | 304/11 |
| 14 | Does it fly? | Yes | 0.16 | 1.35 | 1321/10 | 317/11 |
| 15 | Can it sing? | No | 0.16 | 1.22 | 1447/10 | 330/11 |
| 16 | Is it a mammal? | No | 0.19 | 1.74 | 1577/12 | 344/11 |
| 17 | Does it give milk? | No | 0.17 | 1.32 | 1715/11 | 358/11 |
| 18 | Is it an insect? | Yes | 0.18 | 1.35 | 1857/11 | 372/11 |
| 19 | Does it have six legs? | Yes | 0.19 | 1.38 | 2004/12 | 387/11 |
| 20 | Does it have antennae? | Yes | 0.21 | 1.43 | 2158/13 | 401/11 |

### 모델: exaone3.5:7.8b (정답: Butterfly)
| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Is the secret word related to technology? | No | 2.32 | 1.37 | 167/22 | 130/11 |
| 2 | Does the secret word start with the letter S? | No | 0.46 | 1.33 | 238/24 | 149/11 |
| 3 | Is the secret word a common name? | No | 0.44 | 1.32 | 322/22 | 166/11 |
| 4 | Does the secret word contain the letter 'R'? | Yes | 0.48 | 1.32 | 413/25 | 185/11 |
| 5 | Is the secret word 'Star'? | No | 0.43 | 1.45 | 519/22 | 201/11 |
| 6 | Does the secret word end with 'AR'? | No | 0.47 | 1.41 | 631/24 | 219/11 |
| 7 | Is the secret word 'Mountain'? | No | 0.45 | 1.42 | 756/23 | 235/11 |
| 8 | Does the secret word relate to nature? | Yes | 0.43 | 1.33 | 890/22 | 252/11 |
| 9 | Is the secret word 'Forest'? | No | 0.43 | 1.32 | 1032/22 | 268/11 |
| 10 | Does the secret word involve a natural feature like a tree or plant? | No | 0.53 | 1.56 | 1183/28 | 291/11 |
| 11 | Is the secret word 'River'? | No | 0.43 | 1.41 | 1355/22 | 307/11 |
| 12 | Does the secret word describe a geographical feature? | No | 0.45 | 1.41 | 1530/23 | 325/11 |
| 13 | Is the secret word 'Desert'? | No | 0.45 | 2.28 | 1716/23 | 341/11 |
| 14 | Does the secret word begin with 'G'? | No | 0.47 | 1.34 | 1912/24 | 359/11 |
| 15 | Is the secret word 'Glacier'? | No | 0.48 | 1.60 | 2120/24 | 376/11 |
| 16 | Does the secret word start with 'H'? | No | 0.47 | 1.36 | 2339/24 | 394/11 |
| 17 | Is the secret word 'Hill'? | No | 0.45 | 1.31 | 2569/22 | 410/11 |
| 18 | Does the secret word contain the letter 'L'? | Yes | 0.50 | 1.68 | 2806/25 | 429/11 |
| 19 | Is the secret word 'Lake'? | No | 0.44 | 1.42 | 3058/22 | 445/11 |
| 20 | Does the secret word start with 'C'? | No | 0.48 | 1.43 | 3316/24 | 463/11 |

---

## 📊 전체 누적 비용 및 성능 요약 (Grand Total)
| 모델명 | 플레이어 토큰 | 호스트 토큰 | 질문 시간(s) | 답변 시간(s) |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:e4b | 5266 | 2040 | 8.81s | 14.20s |
| llama3.1:8b | 5407 | 2150 | 6.54s | 14.32s |
| phi4:14b | 22467 | 5621 | 11.14s | 28.20s |
| qwen2.5:7b | 24835 | 6094 | 11.06s | 28.64s |
| mistral:7b | 20295 | 5558 | 5.27s | 28.75s |
| exaone3.5:7.8b | 29339 | 6165 | 11.06s | 29.06s |
| **합계 (Total)** | **107609** | **27628** | **53.87s** | **143.17s** |

