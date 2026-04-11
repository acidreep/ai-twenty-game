
# 🤖 AI Twenty Questions Battle Arena (스무고개 배틀)

이 프로젝트는 다양한 **LLM(Large Language Models)** 간의 논리적 추론 능력과 지시 이행 능력을 비교하기 위한 **스무고개 배틀 프레임워크**입니다. 

로컬 모델과 클라우드 모델을 교차 매칭하여 어떤 모델이 가장 적은 질문으로 정답을 맞히는지, 그리고 그 과정에서의 비용 효율성을 측정합니다.

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

## 🤖 지원 모델

### 1. Cloud Models
* **Frontier Tier**
    * `openai/gpt-5.4`
    * `anthropic/claude-sonnet-4.6`
    * `x-ai/grok-4.20`
* **Value Tier**
    * `deepseek/deepseek-v3.2`
    * `google/gemini-3-flash-preview`
    * `google/gemini-2.5-flash-lite`
    * `x-ai/grok-4.1-fast`
    * `xiaomi/mimo-v2-flash`

### 2. Local Models
* **Mid-Range (10B+)**
    * `phi4:14b`, `gemma4:e4b`
* **Compact (Under 10B)**
    * `llama3.1:8b`, `exaone3.5:7.8b`, `qwen2.5:7b`, `mistral:7b`

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
