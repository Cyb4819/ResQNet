from app.aid import handle_aid_request, analyze_image_for_hazards
from models.gemma3n.pipeline import get_text_generation_pipeline

def main():
    print("==== ResQNet CLI ====")
    query = input("Enter aid topic (e.g., CPR, Burn): ")
    result = handle_aid_request(query)
    print("\n📘 AI First Aid Explanation:")
    print(result["ai_explanation"])
    print("\n🔢 Steps:")
    for i, step in enumerate(result["steps"], 1):
        print(f"{i}. {step}")

if __name__ == "__main__":
    main()