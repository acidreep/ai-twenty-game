import json
import os
import requests

# 스크립트 위치 기준 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRICING_FILE = os.path.join(BASE_DIR, "pricing_config.json")

# 추적할 OpenRouter 모델 목록 (JSON이 비어있을 때 참조)
TRACKED_MODELS = [
    "google/gemini-3-flash-preview",
    "anthropic/claude-sonnet-4.6",
    "google/gemini-3.1-pro-preview",
    "openai/gpt-5.4",
    "x-ai/grok-4.20",
    "z-ai/glm-5.1",
    "google/gemini-2.5-flash-lite",
    "deepseek/deepseek-v3.2",
    "x-ai/grok-4.1-fast",
    "openai/gpt-5-nano",
    "xiaomi/mimo-v2-flash"
]

def load_config():
    """기존 설정을 로드하거나 기본값을 반환합니다."""
    if os.path.exists(PRICING_FILE):
        try:
            with open(PRICING_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {"exchange_rate": 1400.0, "models": {}}

def save_config(data):
    """설정을 파일에 저장합니다."""
    with open(PRICING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def auto_update_from_apis():
    """외부 API를 통해 환율과 OpenRouter 모델 가격을 자동으로 업데이트합니다."""
    config = load_config()
    updated = False

    print("\n[1/2] 최신 환율 정보를 가져오는 중...")
    try:
        rate_res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        rate_res.raise_for_status()
        krw_rate = rate_res.json().get("rates", {}).get("KRW")
        if krw_rate:
            config["exchange_rate"] = krw_rate
            print(f"✔ 환율 업데이트 완료: 1 USD = {krw_rate} KRW")
            updated = True
    except Exception as e:
        print(f"✘ 환율 업데이트 실패: {e}")

    print("\n[2/2] OpenRouter 모델 가격 정보를 가져오는 중...")
    try:
        or_res = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        or_res.raise_for_status()
        models_data = or_res.json().get("data", [])

        # 기존 모델 키 + 우리가 추적하고자 하는 모델 목록 합치기
        target_models = set(list(config["models"].keys()) + TRACKED_MODELS)
        update_count = 0

        for model_info in models_data:
            m_id = model_info.get("id")
            if m_id in target_models:
                pricing = model_info.get("pricing", {})
                i_p = float(pricing.get("prompt", 0)) * 1_000_000
                o_p = float(pricing.get("completion", 0)) * 1_000_000

                if m_id not in config["models"]:
                    config["models"][m_id] = {}

                config["models"][m_id]["input_1m_usd"] = i_p
                config["models"][m_id]["output_1m_usd"] = o_p
                # 캐시 할인율은 API에서 일관되게 제공되지 않으므로, 기존에 수동으로 입력한 값이 있다면 유지합니다.
                if "cache_discount_factor" not in config["models"][m_id]:
                    config["models"][m_id]["cache_discount_factor"] = 0.5 if "gpt-4" in m_id else 0.1
                update_count += 1
        
        if update_count > 0:
            print(f"✔ {update_count}개 모델의 가격 정보 업데이트 완료")
            updated = True
    except Exception as e:
        print(f"✘ 모델 가격 업데이트 실패: {e}")

    if updated:
        save_config(config)

if __name__ == "__main__":
    print("=== 가격 정보 자동 업데이트 시작 ===")
    auto_update_from_apis()
    print("\n[완료] 모든 가격 정보가 최신 상태로 업데이트되었습니다.")