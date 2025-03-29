from ai.learn import review_unmatched_logs
from ai.ai_matcher import retrain_model

if __name__ == "__main__":
    print("📘 Reviewing unmatched logs...\n")
    review_unmatched_logs()
    print("\n🔁 Reloading AI model with new data...")
    retrain_model()
    print("✅ Healix AI ruleset updated!\n")
