import ollama
from openai import OpenAI
import time
import datetime
import os
import re
import random
import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from dotenv import load_dotenv

# .env 파일로부터 환경 변수 로드
load_dotenv()

# ==========================================
# 게임 기본 설정 (수정 시 여기를 변경하세요)
# ==========================================
DEFAULT_MAX_TURNS = 20          # 기본 최대 질문 횟수
RESPONSE_TIMEOUT_SECONDS = 60   # 모델별 응답 제한 시간(초)
# ==========================================

# API 설정
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenRouter 클라이언트 초기화 (키가 있을 때만 진행)
or_client = None
if OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your_actual_openrouter_api_key_here":
    or_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

def load_pricing():
    """가격을 로드합니다."""
    # 현재 파일의 위치를 기준으로 절대 경로 생성
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pricing_path = os.path.join(base_dir, "pricing_config.json")
    try:
        with open(pricing_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if data else {"exchange_rate": 1400.0, "models": {}}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"exchange_rate": 1400.0, "models": {}}

PRICING_DATA = {"exchange_rate": 1400.0, "models": {}} # 초기화

def get_installed_models():
    """현재 설치된 Ollama 모델 리스트를 반환합니다."""
    try:
        models_info = ollama.list()
        return [m.model if hasattr(m, 'model') else m['name'] for m in models_info.models if m]
    except Exception as e:
        print(f"모델 목록을 가져오는 중 오류 발생: {e}")
        return []

def llm_chat(provider, model, messages, options=None, format=None):
    """통합 LLM 호출 인터페이스"""
    temp = options.get('temperature', 0) if options else 0
    
    if provider == "ollama":
        res = ollama.chat(model=model, messages=messages, options={'temperature': temp, 'num_predict': 200}, format=format)
        return {
            "message": res['message'],
            "prompt_tokens": res.get('prompt_eval_count', 0),
            "completion_tokens": res.get('eval_count', 0)
        }
    
    elif provider == "openrouter":
        if not or_client:
            raise ValueError("OpenRouter API 키가 설정되지 않았습니다. .env 파일을 확인해 주세요.")
            
        # OpenRouter/OpenAI 형식으로 변환
        response_format = {"type": "json_object"} if format == "json" else None

        # 재시도 로직 없이 단일 호출 진행
        response = or_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temp,
            response_format=response_format,
            max_tokens=200  # 토큰 낭비를 막기 위해 출력 길이를 엄격히 제한
        )
        
        if not response.choices or len(response.choices) == 0:
            raise ValueError(f"OpenRouter 모델({model})로부터 빈 응답을 받았습니다.")
            
        # OpenAI/OpenRouter API에서 캐시된 토큰 수 추출
        cached_tokens = getattr(response.usage.prompt_tokens_details, "cached_tokens", 0) if hasattr(response.usage, "prompt_tokens_details") else 0
        return {
            "message": {"content": response.choices[0].message.content or ""},
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "cached_tokens": cached_tokens
        }

# 문제 풀 리스트
# A unified pool of 40 common nouns (Animals & Objects) for standardized testing
COMMON_NOUNS = [
    "Lion", "Tiger", "Elephant", "Giraffe", "Zebra", "Kangaroo", "Panda", "Penguin", "Dolphin", "Shark",
    "Eagle", "Owl", "Cat", "Dog", "Rabbit", "Turtle", "Frog", "Snake", "Bee", "Butterfly",
    "Novel", "Computer", "Telephone", "Camera", "Clock", "Umbrella", "Bicycle", "Car", "Sofa", "Desk",
    "Bed", "Flashlight", "Wrench", "Scissors", "Backpack", "Guitar", "Piano", "Bottle", "Cup", "Spoon"
]

# 전역 실행기 생성 (함수 안에서 생성/소멸 시 대기 현상 방지)
executor = ThreadPoolExecutor(max_workers=5)

def chat_with_timeout(provider, model, messages, options=None, description="chat", format=None):
    """Ollama chat 호출을 지정된 시간 안에 완료하도록 제한합니다."""
    def _call():
        return llm_chat(provider, model, messages, options, format)

    future = executor.submit(_call)
    try:
        return future.result(timeout=RESPONSE_TIMEOUT_SECONDS)
    except FutureTimeout:
        # 주의: Python 쓰레드는 강제 종료가 어려우므로, 
        # 이 future는 백그라운드에서 계속 실행될 수 있으나 메인 흐름은 차단하지 않음
        raise TimeoutError(f"{model} {description} 응답이 {RESPONSE_TIMEOUT_SECONDS}초를 초과했습니다.")


def print_model_install_status(installed_models, models_to_test, host_model):
    """설치된 Ollama 모델 목록과 게임에 필요한 모델 상태를 출력합니다."""
    print("--- Ollama 설치된 모델 ---")
    if installed_models:
        for model in installed_models:
            print(f"  - {model}")
    else:
        print("  (설치된 모델이 없습니다.)")

    print("\n--- 게임 참가 모델 확인 ---")
    for m_cfg in models_to_test:
        p, name = m_cfg['provider'], m_cfg['name']
        if p == "ollama":
            status = "✔" if name in installed_models else "✘"
            print(f"  {status} [Local] {name}")
        else:
            print(f"  🌐 [Cloud] {name}")

    h_p, h_name = host_model['provider'], host_model['name']
    if h_p == "ollama" and h_name not in installed_models:
        print(f"\n중요: 호스트 모델 {h_name}이 설치되어 있지 않습니다.")


def clean_response(text):
    """모델 답변에서 생각 과정(<think>)이나 불필요한 태그를 제거합니다."""
    # <think>, <thought>, <reasoning> 등 다양한 형태의 생각 태그 제거
    text = re.sub(r'<(think|thought|reasoning)>.*?</\1>', '', text, flags=re.DOTALL | re.IGNORECASE).strip()
    text = re.sub(r'<.*?>', '', text) # 나머지 모든 XML 스타일 태그 제거
    return text.strip()

def extract_json(text):
    """텍스트에서 JSON 구조를 최대한 안전하게 추출합니다 (로컬 모델의 비정상 출력 대응 강화)."""
    if not text: return None
    text = clean_response(text)
    try:
        # 1. 마크다운 코드 블록 우선 탐색
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})', text, re.DOTALL | re.IGNORECASE)
        if json_match:
            text = json_match.group(1)

        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            json_str = text[start:end+1]
            try:
                # 2. 제어 문자 제거 및 표준 파싱
                json_str = "".join(ch for ch in json_str if ord(ch) >= 32 or ch in "\n\r\t").strip()
                return json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                try:
                    # 느슨한 파싱: 작은따옴표 교체 및 후행 쉼표(trailing comma) 제거 시도
                    fixed = json_str.replace("'", '"')
                    fixed = re.sub(r',\s*([\]}])', r'\1', fixed)
                    return json.loads(fixed)
                except:
                    return None
        return None
    except Exception:
        return None

def get_pure_text(text):
    """불필요한 접두어를 제거하고 순수 텍스트만 반환합니다. 질문이 포함되어 있다면 추출을 시도합니다."""
    text = re.sub(r'^(질문|답변|참가자|진행자|진행자 답변|Question|Answer|Host|Participant)\s*\d*[:：]\s*', '', text, flags=re.IGNORECASE)
    
    # JSON 파싱 실패 대비: 문장 중 '?'로 끝나는 첫 번째 질문 문장이 있다면 해당 부분만 추출
    question_match = re.search(r'([^.!?]+\?)', text)
    if question_match:
        return question_match.group(1).strip()
        
    return text.strip()

def calculate_cost(model_name, prompt_tokens, completion_tokens, cached_tokens=0):
    """토큰 사용량에 따른 비용을 계산합니다."""
    pricing = PRICING_DATA["models"].get(model_name, {"input_1m_usd": 0, "output_1m_usd": 0})
    # 모델별 특화된 캐시 할인율이 있으면 사용, 없으면 기본값 0.1 (10% 가격) 적용
    
    discount_factor = pricing.get("cache_discount_factor", 0.1)
    
    ex_rate = PRICING_DATA.get("exchange_rate", 1400.0)
    
    input_1m = pricing.get("input_1m_usd", 0)
    output_1m = pricing.get("output_1m_usd", 0)

    non_cached_tokens = prompt_tokens - cached_tokens
    input_cost = (non_cached_tokens * pricing["input_1m_usd"] / 1_000_000) + \
                 (cached_tokens * pricing["input_1m_usd"] * discount_factor / 1_000_000)
    input_cost = (non_cached_tokens * input_1m / 1_000_000) + \
                 (cached_tokens * input_1m * discount_factor / 1_000_000)
                 
    cost_usd = input_cost + (completion_tokens * pricing["output_1m_usd"] / 1_000_000)
    cost_usd = input_cost + (completion_tokens * output_1m / 1_000_000)
    cost_krw = cost_usd * ex_rate
    return cost_usd, cost_krw

def get_secret_word(host_provider, host_model):
    """정해진 단어 풀(COMMON_NOUNS)에서 무작위로 정답 단어를 선택합니다."""
    # 코드 내의 정의된 풀에서 파이썬 random 함수로 직접 선택합니다.
    return random.choice(COMMON_NOUNS)
    

def check_model_availability(provider, model, retries=1):
    """모델이 최소한 한 번 응답하는지 확인합니다."""
    for i in range(retries + 1):
        try:
            messages = [{'role': 'user', 'content': 'hi'}]
            response = chat_with_timeout(provider, model, messages, description='출석 체크')
            
            content = "응답 확인됨"
            if 'message' in response and 'content' in response['message']:
                content = clean_response(response['message']['content'])
                
            print(f"  [출석] {model} 응답 성공: {content}")
            return True
        except Exception as e:
            if i < retries:
                print(f"  [대기] {model} 응답이 늦습니다. 3초 후 다시 시도합니다... ({i+1}/{retries})")
                time.sleep(3)
            else:
                print(f"  [출석] {model} 최종 응답 실패: {e}")
                return False


def play_twenty_questions(models_to_test, host_model, env_name="default", max_turns=DEFAULT_MAX_TURNS):
    global PRICING_DATA
    # 게임 시작 전 최신 가격 정보를 다시 로드합니다.
    PRICING_DATA = load_pricing()

    installed_models = get_installed_models()
    print_model_install_status(installed_models, models_to_test, host_model)
    print(f"--- 응답 제한: {RESPONSE_TIMEOUT_SECONDS}초 ---")

    # 설치된 모델만 필터링
    available_players = []
    for m in models_to_test:
        if m['provider'] == 'ollama' and m['name'] not in installed_models:
            continue
        available_players.append(m)

    print("--- 모델 출석 체크 ---")
    host_ready = check_model_availability(host_model['provider'], host_model['name'], retries=3)
    if not host_ready:
        print(f"경고: 호스트 모델({host_model['name']})이 응답하지 않습니다.")

    ready_players = []
    failed_players = []
    for p_cfg in available_players:
        p_provider, p_name = p_cfg['provider'], p_cfg['name']
        print(f"출석 체크: {p_name} ({p_provider}) ...")
        if check_model_availability(p_provider, p_name, retries=3):
            ready_players.append(p_cfg)
        else:
            failed_players.append(p_name)
            print(f"  -> {p_name} 출석 실패")

    if not ready_players:
        print("오류: 응답 가능한 플레이어 모델이 없습니다.")
        return

    if not host_ready:
        print("오류: 호스트 모델이 준비되지 않아 배틀을 시작할 수 없습니다.")
        return

    # 일부 모델 실패 시 사용자 확인 로직
    if failed_players:
        print(f"\n⚠️ 다음 모델들이 출석에 실패했습니다: {', '.join(failed_players)}")
        user_choice = input(f"남은 {len(ready_players)}개의 모델로 배틀을 계속 진행할까요? (y/n): ").lower()
        if user_choice != 'y':
            print("사용자 요청에 의해 게임을 중단합니다.")
            return
        print("배틀을 계속 진행합니다.\n")

    available_players = ready_players # (이 줄은 이미 위에서 필터링되었으나 논리적 명시)

    results = []
    
    total_setup_duration = 0.0

    # 1. 모든 플레이어에게 공통으로 적용될 정답 단어 결정
    start_word_gen = time.time()
    target_word = get_secret_word(host_model['provider'], host_model['name'])
    total_setup_duration += (time.time() - start_word_gen)
    print(f"--- 스무고개 배틀 시작 (호스트: {host_model['name']}) ---")
    print(f"   [시스템] 이번 배틀의 공통 정답: {target_word}")

    # 실제 배틀 시작 시점부터 시간 측정
    start_time_all = time.time()

    for p_cfg in ready_players:
        p_provider, p_name = p_cfg['provider'], p_cfg['name']
        print(f"\n> 플레이어 [{p_name}] 차례 시작...")

        # 2. 호스트 설정
        host_system_prompt = (
            f"You are the host of a 20-questions game. The secret word is '{target_word}'.\n"
            "Rules:\n"
            f"1. If the participant guesses '{target_word}' correctly, answer 'Correct!'.\n"
            "2. Otherwise, answer ONLY with 'Yes', 'No', or 'I don't know'.\n"
            "3. Respond ONLY in JSON format:\n"
            "{\n"
            "  \"answer\": \"Yes\" | \"No\" | \"I don't know\" | \"Correct!\"\n"
            "}\n"
        )

        messages_host = [{'role': 'system', 'content': host_system_prompt}]
        start_host_init = time.time()
        host_init_res = chat_with_timeout(host_model['provider'], host_model['name'], messages_host, options={'temperature': 0}, description='호스트 초기화')
        # 초기화 시 발생하는 토큰은 기록에 포함하지 않거나 별도 처리 가능하지만 여기서는 본 게임에 집중합니다.
        messages_host.append({'role': 'assistant', 'content': host_init_res['message']['content']})
        total_setup_duration += (time.time() - start_host_init)

        # 3. 플레이어 설정
        player_system_prompt = (
            "You are a strategic player in a '20 Questions' game. Your goal is to find the secret word.\n"
            "Rules:\n"
            "1. Ask a single Yes/No question or make a guess.\n"
            "2. Respond ONLY with a valid JSON object. No introductory text or conversational filler.\n"
            "3. JSON structure: {\"question\": \"your question\", \"is_guess\": boolean}\n"
            "4. NEVER include phrases like 'Here is the JSON' or 'Sure' inside or outside the JSON.\n"
            "5. Always respond in English."
        )
        init_msg = "Let's start the game. Please ask your first question."

        messages_player = [
            {'role': 'system', 'content': player_system_prompt},
            {'role': 'user', 'content': init_msg}
        ]
        
        game_history = [] # 게임 기록 초기화
        success = False
        turns = max_turns
        asked_questions = [] # 중복 체크를 위한 질문 리스트

        for i in range(1, max_turns + 1):
            # 플레이어 질문
            current_player_prompt = f"Previous questions: {', '.join(asked_questions)}\nGenerate your next question/guess in JSON format. NO FILLER TEXT."
            messages_player.append({'role': 'user', 'content': current_player_prompt})
            
            start_p = time.time()
            res_p = chat_with_timeout(p_provider, p_name, messages_player, options={'temperature': 0.1}, description='플레이어 질문', format='json')
            p_json = extract_json(res_p['message']['content'])

            p_in = res_p.get('prompt_tokens', 0)
            p_out = res_p.get('completion_tokens', 0)
            p_cached = res_p.get('cached_tokens', 0)

            question = ""
            if p_json:
                # 키 값을 소문자로 변환하여 검색
                p_json_lower = {k.lower(): v for k, v in p_json.items()}
                question = p_json_lower.get('question', '').strip()
                # 모델이 서술형 문구를 질문 안에 포함시킨 경우 공격적으로 제거 (콜론 유무 상관없이 매칭)
                question = re.sub(r'^(Here is the JSON requested|Certainly|Sure|Based on the rules|I will ask|My question is).*?([:：\s]|$)', '', question, flags=re.IGNORECASE).strip()
            
            # JSON 파싱 실패, 질문이 비어있음, 혹은 "Here is the JSON..."만 남은 경우 fallback
            if not question or "JSON requested" in question:
                raw_content = res_p['message'].get('content', '')
                question = get_pure_text(clean_response(raw_content)) or "Failed to generate question"
            
            duration_p = time.time() - start_p
            
            print(f"    질문 {i}: {question} ({duration_p:.1f}s)")
            
            # 히스토리에 넣을 때 안전하게 json.dumps 사용
            player_response_obj = {"question": question}
            if p_json and 'is_guess' in p_json:
                player_response_obj["is_guess"] = p_json['is_guess']
            messages_player.append({'role': 'assistant', 'content': json.dumps(player_response_obj, ensure_ascii=False)})
            messages_host.append({'role': 'user', 'content': f"질문: {question}"})
            asked_questions.append(question)
            
            # 호스트 답변
            start_h = time.time()
            res_h = chat_with_timeout(host_model['provider'], host_model['name'], messages_host, options={'temperature': 0}, description='호스트 답변', format='json')
            h_json = extract_json(res_h['message']['content'])
            
            h_in = res_h.get('prompt_tokens', 0)
            h_out = res_h.get('completion_tokens', 0)
            h_cached = res_h.get('cached_tokens', 0)

            if not h_json:
                raw_h = clean_response(res_h['message']['content'])
                answer = get_pure_text(raw_h)
                if "correct" in answer.lower(): answer = "Correct!"
            else:
                answer = h_json.get('answer', '모르겠습니다')
                
            duration_h = time.time() - start_h
            print(f"    답변: {answer} ({duration_h:.1f}s)")
            
            messages_host.append({'role': 'assistant', 'content': f"{{\"answer\": \"{answer}\"}}"})
            messages_player.append({'role': 'user', 'content': f"진행자 답변: {answer}"})

            game_history.append((i, question, answer, duration_p, duration_h, p_in, p_out, h_in, h_out, p_cached, h_cached))

            # 호스트가 명확하게 정답임을 인정한 경우만 체크
            ans_normalized = answer.replace(" ", "").lower()
            if "정답입니다" in ans_normalized or "correct" in ans_normalized:
                success = True
                turns = i
                break
        
        results.append({
            'model': p_name,
            'target': target_word,
            'success': success,
            'turns': turns,
            'history': game_history
        })
        print(f"  - 결과: {'성공' if success else '실패'} ({turns}회)")

    # 결과 정렬 (성공 여부 우선, 그 다음 질문 횟수 적은 순)
    results.sort(key=lambda x: (not x['success'], x['turns']))

    # 결과 보고서 생성
    total_elapsed = time.time() - start_time_all
    # 시:분:초 형식으로 변환
    grand_p_dur = sum(sum(h[3] for h in res['history']) for res in results)
    grand_h_dur = sum(sum(h[4] for h in res['history']) for res in results)
    
    elapsed_str = str(datetime.timedelta(seconds=int(total_elapsed)))
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_content = f"# 🏆 스무고개 배틀 결과 리포트 ({now})\n\n"
    report_content += f"**호스트 모델:** {host_model}\n\n"
    report_content += f"**전체 소요 시간:** {elapsed_str} ({total_elapsed:.2f}초)\n"
    report_content += f"- **호스트 준비 시간:** {total_setup_duration:.2f}초 (단어 선정 및 초기화)\n"
    report_content += f"- **순수 게임 진행 시간:** {grand_p_dur + grand_h_dur:.2f}초 (질문/답변 합계)\n\n"
    report_content += "| 순위 | 모델명 | 정답 단어 | 결과 | 질문 횟수 |\n"
    report_content += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    grand_total_usd = 0.0
    grand_total_krw = 0.0
    grand_total_p_tokens = 0
    grand_total_h_tokens = 0
    grand_total_p_duration = 0.0
    grand_total_h_duration = 0.0

    for idx, res in enumerate(results, 1):
        status = "✅ 성공" if res['success'] else "❌ 실패"
        report_content += f"| {idx} | {res['model']} | {res['target']} | {status} | {res['turns']} |\n"

    report_content += "\n---\n\n## 📝 상세 게임 기록\n"
    for res in results:
        report_content += f"\n### 모델: {res['model']} (정답: {res['target']})\n"
        report_content += "| 턴 | 질문 | 답변 | 질문 시간(s) | 답변 시간(s) | 질문 토큰(I/O) | 답변 토큰(I/O) |\n"
        report_content += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        
        for i, q, a, dp, dh, pin, pout, hin, hout, pc, hc in res['history']:
            # 표 안의 줄바꿈 방지
            q_clean = q.replace('\n', ' ')
            a_clean = a.replace('\n', ' ')
            report_content += f"| {i} | {q_clean} | {a_clean} | {dp:.2f} | {dh:.2f} | {pin}/{pout} | {hin}/{hout} |\n"

    # 💰 통합 요약 통계 표 생성
    report_content += f"\n---\n\n## 📊 전체 누적 비용 및 성능 요약 (Grand Total)\n"
    is_local = (env_name == "local")

    if is_local:
        report_content += "| 모델명 | 플레이어 토큰 | 호스트 토큰 | 질문 시간(s) | 답변 시간(s) |\n"
        report_content += "| :--- | :---: | :---: | :---: | :---: |\n"
    else:
        report_content += "| 모델명 | 단가 (1M 토큰 In/Out) | 플레이어 토큰 | 호스트 토큰 | 질문 시간(s) | 답변 시간(s) | 합계 비용 (USD) | 합계 비용 (KRW) |\n"
        report_content += "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n"

    for res in results:
        p_tokens = sum(h[5] + h[6] for h in res['history'])
        h_tokens = sum(h[7] + h[8] for h in res['history'])
        p_cached_total = sum(h[9] for h in res['history'])
        h_cached_total = sum(h[10] for h in res['history'])
        p_duration = sum(h[3] for h in res['history'])
        h_duration = sum(h[4] for h in res['history'])

        if is_local:
            report_content += f"| {res['model']} | {p_tokens} | {h_tokens} | {p_duration:.2f}s | {h_duration:.2f}s |\n"
        else:
            p_usd, p_krw = calculate_cost(res['model'], sum(h[5] for h in res['history']), sum(h[6] for h in res['history']), p_cached_total)
            h_usd, h_krw = calculate_cost(host_model['name'], sum(h[7] for h in res['history']), sum(h[8] for h in res['history']), h_cached_total)
            
            model_total_usd = p_usd + h_usd
            model_total_krw = p_krw + h_krw
            
            # 모델별 단가 정보 (플레이어 모델 기준)
            p_pricing = PRICING_DATA["models"].get(res['model'], {"input_1m_usd": 0, "output_1m_usd": 0})
            p_unit_price = f"${p_pricing['input_1m_usd']:.2f} / ${p_pricing['output_1m_usd']:.2f}"
            
            report_content += f"| {res['model']} | {p_unit_price} | {p_tokens} | {h_tokens} | {p_duration:.2f}s | {h_duration:.2f}s | ${model_total_usd:.6f} | ₩{model_total_krw:.2f} |\n"
            
            grand_total_usd += model_total_usd
            grand_total_krw += model_total_krw

        # 총계 합산
        grand_total_p_tokens += p_tokens
        grand_total_h_tokens += h_tokens
        grand_total_p_duration += p_duration
        grand_total_h_duration += h_duration

    # 마지막 총합 행 추가
    if is_local:
        report_content += f"| **합계 (Total)** | **{grand_total_p_tokens}** | **{grand_total_h_tokens}** | **{grand_total_p_duration:.2f}s** | **{grand_total_h_duration:.2f}s** |\n"
    else:
        report_content += f"| **합계 (Total)** | - | **{grand_total_p_tokens}** | **{grand_total_h_tokens}** | **{grand_total_p_duration:.2f}s** | **{grand_total_h_duration:.2f}s** | **${grand_total_usd:.6f}** | **₩{grand_total_krw:.2f}** |\n"

    # 리포트 폴더 생성 및 저장 (reports/local 또는 reports/openrouter)
    report_dir = os.path.join("reports", env_name)
    os.makedirs(report_dir, exist_ok=True)
    
    filename = f"report_{now}.md"
    file_path = os.path.join(report_dir, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"\n\n[완료] 결과 리포트가 생성되었습니다: {file_path}")
    print(report_content)
