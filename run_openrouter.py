from ai_twenty_game import play_twenty_questions

# 호스트 모델
HOST_MODELS = [
    {"provider": "openrouter", "name": "google/gemini-3-flash-preview"}
]

# 테스트 모델 리스트
PLAYER_MODELS = [
    {"provider": "openrouter", "name": "google/gemini-3-flash-preview"},
    {"provider": "openrouter", "name": "anthropic/claude-sonnet-4.6"},
    {"provider": "openrouter", "name": "openai/gpt-5.4"},
    {"provider": "openrouter", "name": "x-ai/grok-4.20"},
    {"provider": "openrouter", "name": "google/gemini-2.5-flash-lite"},
    {"provider": "openrouter", "name": "deepseek/deepseek-v3.2"},
    {"provider": "openrouter", "name": "x-ai/grok-4.1-fast"},
    {"provider": "openrouter", "name": "xiaomi/mimo-v2-flash"},
]

if __name__ == "__main__":
    print("=== OpenRouter 클라우드 모델 스무고개 배틀 실행 ===")
    try:
        for host in HOST_MODELS:
            print(f"\n\n--- 새로운 배틀: 호스트 [{host['name']}] ---")
            play_twenty_questions(
                models_to_test=PLAYER_MODELS,
                host_model=host,
                env_name="openrouter"
            )
    except KeyboardInterrupt:
        print("\n\n명령에 의해 게임이 중단되었습니다. (Ctrl+C)")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        print(".env 파일의 OPENROUTER_API_KEY 설정을 확인해 주세요.")