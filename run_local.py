from ai_twenty_game import play_twenty_questions

# 호스트 모델
HOST_MODELS = [
    {"provider": "openrouter", "name": "google/gemini-3-flash-preview"}
]

# 테스트 모델 리스트
PLAYER_MODELS = [
    {"provider": "ollama", "name": "gemma4:e4b"},
    {"provider": "ollama", "name": "phi4:14b"},
    {"provider": "ollama", "name": "llama3.1:8b"},
    {"provider": "ollama", "name": "qwen2.5:7b"},
    {"provider": "ollama", "name": "mistral:7b"},
    {"provider": "ollama", "name": "exaone3.5:7.8b"},
]

if __name__ == "__main__":
    print("=== 로컬 모델(Host) vs Gemini(Player) 배틀 실행 ===")
    for host in HOST_MODELS:
        print(f"\n\n--- 새로운 배틀: 호스트 [{host['name']}] ---")
        try:
            play_twenty_questions(
                models_to_test=PLAYER_MODELS,
                host_model=host,
                env_name="local"
            )
        except KeyboardInterrupt:
            print("\n중단되었습니다.")
            break
        except Exception as e:
            print(f"호스트 {host['name']} 진행 중 오류: {e}")