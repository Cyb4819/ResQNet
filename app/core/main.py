from app.aid import handle_aid_request, analyze_image_for_hazards, recognize_kit_item

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